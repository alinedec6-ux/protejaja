"""
Suíte de Testes de Segurança e Controle de Acesso (Auditoria ProtejaJá).
Verifica a correção de falhas de controle de acesso (OWASP Top 10 - Broken Access Control).
"""
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

import database as db
from app import create_app


class SecurityAuditTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_01_usuario_comum_bloqueado_no_admin(self):
        """Usuário comum NÃO pode acessar /admin nem rotas de moderação."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2  # Cidadão comum (não admin)

        res = self.client.get("/admin")
        self.assertEqual(res.status_code, 302, "Usuário comum não deve acessar /admin!")
        self.assertIn("/home", res.headers.get("Location", ""))

    def test_02_idor_detalhes_denuncia_outro_usuario(self):
        """Usuário comum não pode ver denúncia alheia via /denuncias/<id>."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2  # Cidadão comum

        # Denúncia 999999 não pertence ao usuário 2
        res = self.client.get("/denuncias/999999")
        self.assertEqual(res.status_code, 302)

    def test_03_admin_consegue_inspecionar_qualquer_denuncia(self):
        """Administrador tem permissão para auditar detalhes de qualquer denúncia."""
        conn = db.get_connection()
        cur = conn.execute(
            "INSERT INTO reports (user_id, denunciado, assunto, categoria, descricao, anexo, status) "
            "VALUES (2, 'Empresa X', 'Auditoria Admin', 'Geral', 'Descricao', NULL, 'EM_ANALISE_IA')"
        )
        conn.commit()
        rep_id = cur.lastrowid

        with self.client.session_transaction() as sess:
            sess["user_id"] = 1  # Admin

        res = self.client.get(f"/denuncias/{rep_id}")
        self.assertEqual(res.status_code, 200, "Admin deve conseguir auditar a denúncia!")

    def test_04_anexos_privados_bloqueados_para_deslogados_e_terceiros(self):
        """Provas confidenciais (não aprovadas) NÃO podem ser acessadas por visitantes ou terceiros (403 Forbidden)."""
        conn = db.get_connection()
        conn.execute(
            "INSERT INTO reports (user_id, denunciado, assunto, categoria, descricao, anexo, status) "
            "VALUES (2, 'Alvo Privado', 'Assunto Privado', 'Geral', 'Descricao', 'privado_teste.pdf', 'EM_ANALISE_IA')"
        )
        conn.commit()

        # Cria o arquivo físico na pasta de uploads
        upload_path = os.path.join(db.UPLOAD_DIR, "privado_teste.pdf")
        with open(upload_path, "w") as f:
            f.write("PROVA CONFIDENCIAL")

        # 1. Visitante deslogado deve receber 403 Forbidden
        with self.client.session_transaction() as sess:
            sess.clear()
        res_deslogado = self.client.get("/uploads/privado_teste.pdf")
        self.assertEqual(res_deslogado.status_code, 403, "Visitante não pode acessar anexo privado!")

        # 2. Outro usuário comum (que não é o autor) também deve receber 403 Forbidden
        with self.client.session_transaction() as sess:
            sess["user_id"] = 99999  # Outro usuário qualquer
        res_terceiro = self.client.get("/uploads/privado_teste.pdf")
        self.assertEqual(res_terceiro.status_code, 403, "Terceiro não pode acessar anexo privado de outro usuário!")

    def test_05_anexo_privado_acessivel_por_autor_e_admin(self):
        """O próprio autor da denúncia e o administrador conseguem visualizar o anexo."""
        # Autor (user_id = 2)
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
        res_autor = self.client.get("/uploads/privado_teste.pdf")
        self.assertEqual(res_autor.status_code, 200, "O próprio autor deve acessar sua prova!")

        # Administrador (user_id = 1)
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
        res_admin = self.client.get("/uploads/privado_teste.pdf")
        self.assertEqual(res_admin.status_code, 200, "O Administrador deve poder auditar a prova!")

    def test_06_anexo_aprovado_publico(self):
        """Anexos de denúncias APROVADAS são acessíveis publicamente no feed comunitário."""
        conn = db.get_connection()
        conn.execute(
            "INSERT INTO reports (user_id, denunciado, assunto, categoria, descricao, anexo, status) "
            "VALUES (2, 'Alvo Publico', 'Assunto Publico', 'Geral', 'Descricao', 'publico_teste.png', 'APROVADO')"
        )
        conn.commit()

        upload_path = os.path.join(db.UPLOAD_DIR, "publico_teste.png")
        with open(upload_path, "w") as f:
            f.write("PROVA PUBLICA")

        with self.client.session_transaction() as sess:
            sess.clear()

        res = self.client.get("/uploads/publico_teste.png")
        self.assertEqual(res.status_code, 200, "Provas de denúncias aprovadas devem ser públicas no feed!")

    def test_07_bloqueio_reset_senha_admin_portal_publico(self):
        """Tentativa de redefinir senha do Admin via formulário público deve ser BLOQUEADA."""
        res = self.client.post("/recuperar", data={
            "email": "admin@protejaja.com",
            "data_nascimento": "01/01/2000"
        })
        self.assertNotIn("NOVA SENHA GERADA", res.get_data(as_text=True))
        self.assertIn("Contas administrativas possuem proteção", res.get_data(as_text=True))

    def test_08_moderacao_bloqueia_metodo_get_anti_csrf(self):
        """Rotas de aprovação e rejeição no painel administrativo devem rejeitar GET (Anti-CSRF)."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1  # Admin

        res_get = self.client.get("/admin/aprovar/1")
        self.assertEqual(res_get.status_code, 405, "Moderação via GET deve ser bloqueada com 405 Method Not Allowed!")

        res_rejeitar_get = self.client.get("/admin/rejeitar/1")
        self.assertEqual(res_rejeitar_get.status_code, 405, "Rejeição via GET deve ser bloqueada com 405 Method Not Allowed!")

    def test_09_bloqueio_exclusao_conta_admin(self):
        """Conta mestre de administrador não pode ser expurgada via web."""
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1  # Admin

        res = self.client.get("/excluir-conta")
        self.assertEqual(res.status_code, 302, "Admin não deve poder excluir a conta mestre!")
        self.assertIn("/home", res.headers.get("Location", ""))

    def test_10_seguranca_cookies_sessao(self):
        """Cookies de sessão devem conter flags HTTPOnly e SameSite=Lax para mitigar XSS e CSRF."""
        self.assertTrue(self.app.config.get("SESSION_COOKIE_HTTPONLY"))
        self.assertEqual(self.app.config.get("SESSION_COOKIE_SAMESITE"), "Lax")


if __name__ == "__main__":
    unittest.main()
