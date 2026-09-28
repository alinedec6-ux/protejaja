import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

import database as db
from app import create_app


class ProtejaJaTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar ambiente de teste
        os.environ["BOT_API_KEY"] = "teste-bot-key-123"
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_01_schema_e_migracao(self):
        """Valida se o schema do banco possui todas as colunas de IA e do Termo Legal."""
        conn = db.get_connection()
        cols = {r[1] for r in conn.execute("PRAGMA table_info(reports)").fetchall()}
        obrigatorias = {
            "score_confianca",
            "justificativa_ia",
            "data_analise_ia",
            "analisado_por_admin_id",
            "termo_aceito",
            "data_aceite_termo",
            "status",
        }
        for col in obrigatorias:
            self.assertIn(col, cols, f"Coluna '{col}' ausente no schema de reports!")

    def test_02_endpoints_seo_geo(self):
        """Valida robots.txt e sitemap.xml."""
        res_robots = self.client.get("/robots.txt")
        self.assertEqual(res_robots.status_code, 200)
        self.assertIn(b"User-agent", res_robots.data)
        self.assertIn(b"sitemap.xml", res_robots.data)

        res_sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(res_sitemap.status_code, 200)
        self.assertIn(b"<urlset", res_sitemap.data)
        self.assertIn(b"/home", res_sitemap.data)

    def test_03_ticker_noticias_api(self):
        """Valida o endpoint dinâmico do Ticker de Notícias."""
        res = self.client.get("/api/v1/noticias")
        self.assertEqual(res.status_code, 200)
        dados = res.get_json()
        self.assertTrue(dados.get("sucesso"))
        self.assertIn("noticias", dados)
        self.assertGreaterEqual(len(dados["noticias"]), 1)

    def test_04_criacao_denuncia_e_termo_responsabilidade(self):
        """Valida que uma denúncia exige login e termo de responsabilidade aceito."""
        # Cria usuário de teste
        email = "cidadao.teste@protejaja.com"
        if not db.email_cadastrado(email):
            user_id = db.criar_usuario(
                "Cidadão Teste",
                email,
                "15/05/1990",
                "São Paulo",
                "Av Paulista, 1000",
                "hash_fake",
            )
        else:
            user_id = db.usuario_por_email(email)["id"]

        with self.client.session_transaction() as sess:
            sess["user_id"] = user_id

        # Tentativa de envio SEM aceitar o termo
        res_sem_termo = self.client.post(
            "/denuncias",
            data={
                "denunciado": "Supermercado X",
                "assunto": "Produto com data vencida",
                "categoria": "Produto",
                "descricao": "Encontrei lote de laticínios fora do prazo de validade.",
            },
            follow_redirects=True,
        )
        self.assertIn("Termo de Declaração e Responsabilidade Legal".encode("utf-8"), res_sem_termo.data)

        # Envio COM o termo aceito
        res_com_termo = self.client.post(
            "/denuncias",
            data={
                "denunciado": "Supermercado Savegnago",
                "cidade": "Araraquara",
                "bairro": "Vila Xavier",
                "assunto": "Produto com data vencida",
                "categoria": "Produto",
                "descricao": "Encontrei lote de laticínios fora do prazo de validade nas gôndolas da filial.",
                "termo_responsabilidade": "1",
            },
            follow_redirects=True,
        )
        self.assertEqual(res_com_termo.status_code, 200)

        # Verifica se foi gravado no status EM_ANALISE_IA com cidade e bairro
        denuncias = db.denuncias_do_usuario(user_id)
        self.assertGreater(len(denuncias), 0)
        ultima = denuncias[0]
        self.assertEqual(ultima["status"], db.STATUS_EM_ANALISE_IA)
        self.assertEqual(ultima["cidade"], "Araraquara")
        self.assertEqual(ultima["bairro"], "Vila Xavier")

        ProtejaJaTestSuite.denuncia_teste_id = ultima["id"]

    def test_05_api_bot_triagem_pendentes(self):
        """Valida autenticação e listagem de pendentes para o Bot de IA."""
        # Sem token -> 401
        res_sem_auth = self.client.get("/api/v1/denuncias/pendentes")
        self.assertEqual(res_sem_auth.status_code, 401)

        # Com token correto -> 200
        headers = {"X-API-Key": "teste-bot-key-123"}
        res_auth = self.client.get("/api/v1/denuncias/pendentes", headers=headers)
        self.assertEqual(res_auth.status_code, 200)
        dados = res_auth.get_json()
        self.assertTrue(dados.get("sucesso"))
        self.assertIn("denuncias", dados)

    def test_06_api_bot_triagem_patch(self):
        """Valida que o bot atualiza com status ALERTA_REVISAO_MANUAL, score e justificativa."""
        denuncia_id = getattr(self, "denuncia_teste_id", None)
        self.assertIsNotNone(denuncia_id, "ID da denúncia de teste não encontrado!")

        headers = {"X-API-Key": "teste-bot-key-123", "Content-Type": "application/json"}
        payload = {
            "status": "ALERTA_REVISAO_MANUAL",
            "score_confianca": 0.65,
            "justificativa_ia": "Linguagem respeitosa, mas requer validação da prova documental pelo administrador.",
        }
        res = self.client.patch(
            f"/api/v1/denuncias/{denuncia_id}/triagem",
            json=payload,
            headers=headers,
        )
        self.assertEqual(res.status_code, 200)
        dados = res.get_json()
        self.assertTrue(dados["sucesso"])
        self.assertEqual(dados["status_atual"], "ALERTA_REVISAO_MANUAL")
        self.assertEqual(dados["score_confianca"], 0.65)

        # Valida no banco
        denuncia = db.denuncia_por_id_geral(denuncia_id)
        self.assertEqual(denuncia["status"], db.STATUS_ALERTA_REVISAO)
        self.assertEqual(denuncia["score_confianca"], 0.65)
        self.assertIn("Linguagem respeitosa", denuncia["justificativa_ia"])

    def test_07_moderar_admin_e_publicacao(self):
        """Valida moderação pelo administrador e publicação no feed comunitário."""
        denuncia_id = getattr(self, "denuncia_teste_id", None)

        admin = db.usuario_por_email(db.ADMIN_EMAIL)
        self.assertIsNotNone(admin)

        with self.client.session_transaction() as sess:
            sess["user_id"] = admin["id"]

        # Admin acessa painel com filtro de alerta
        res_painel = self.client.get("/admin?status=ALERTA_REVISAO_MANUAL")
        self.assertEqual(res_painel.status_code, 200)
        self.assertIn(b"ALERTA // REQUER", res_painel.data)

        # Admin aprova a denúncia
        res_moderar = self.client.post(
            f"/admin/moderar/{denuncia_id}",
            data={"status": "APROVADO"},
            follow_redirects=True,
        )
        self.assertEqual(res_moderar.status_code, 200)

        # Valida que agora aparece nas denúncias públicas
        res_publicas = self.client.get("/denuncias-publicas")
        self.assertEqual(res_publicas.status_code, 200)
        self.assertIn(b"Supermercado X", res_publicas.data)

    def test_08_pagina_home_telefones_uteis_e_ctas(self):
        """Valida que a home exibe a central de telefones úteis e removeu jargões antigos."""
        # Limpa sessão para testar como visitante
        with self.client.session_transaction() as sess:
            sess.clear()

        res_home = self.client.get("/home")
        self.assertEqual(res_home.status_code, 200)
        html = res_home.data.decode("utf-8")

        # Telefones de emergência com discagem direta tel:
        self.assertIn("190", html)
        self.assertIn("Polícia Militar", html)
        self.assertIn("tel:190", html)

        self.assertIn("193", html)
        self.assertIn("Corpo de Bombeiros", html)
        self.assertIn("tel:193", html)

        self.assertIn("192", html)
        self.assertIn("SAMU", html)
        self.assertIn("tel:192", html)

        self.assertIn("151", html)
        self.assertIn("Procon SP", html)

        # Valida que CTAs foram simplificados e antigos jargões foram removidos
        self.assertNotIn("Criar Conta Protegida", html)
        self.assertNotIn("Filtro Imediato de Baixo Calão", html)
        self.assertIn("Fazer Denúncia", html)


if __name__ == "__main__":
    unittest.main()
