# ProtejaJá 2.0 — Plataforma Inteligente de Cidadania e Denúncias

Ecossistema digital de registro seguro de denúncias comunitárias com **Python 3 + Flask + SQLite + Tailwind CSS**, interface futurista **Cyber-Pink**, triagem automatizada com **Inteligência Artificial**, **Termo Legal de Responsabilidade (Scroll-to-Agree)**, **Sticky News Ticker** e otimização avançada para motores de busca e LLMs (**SEO & GEO / IAO**).

---

## 🌟 Principais Inovações (Versão 2.0)

1. **Design Futurista Cyber-Pink & Glassmorphism:**
   - Dark mode elegante com paleta Cyber Slate e Neon Magenta / Electric Pink (`#ff007f`).
   - Cards com glassmorphism aeroespacial, bordas com cyber-glow e tipografia moderna (*Plus Jakarta Sans* e *JetBrains Mono*).
2. **Rodapé de Notícias Fixo (Sticky Persistent Footer Ticker):**
   - Barra fixa no rodapé que acompanha o scroll em tempo real.
   - Comportamento adaptativo: exibição estática limpa (1-2 itens) e transição contínua infinita *marquee* com pausa no hover (3+ itens), alimentado via API `/api/v1/noticias`.
3. **Termo de Declaração e Responsabilidade Civil/Penal (Scroll-to-Agree):**
   - Baseado no Código Penal Brasileiro (Arts. 299 e 340) e Marco Civil da Internet (Lei 12.965/2014).
   - Caixa com rolagem obrigatória: o botão de envio só é desbloqueado após o usuário rolar o contrato até o fim e marcar a confirmação.
4. **Pipeline de Moderação Neural & API Restrita para Bots:**
   - Status formais: `EM_ANALISE_IA`, `APROVADO`, `REPROVADO`, `ALERTA_REVISAO_MANUAL`.
   - Telemetria de IA: score de confiança, justificativa técnica e carimbo de data/hora.
   - Endpoints REST protegidos via `BOT_API_KEY`:
     - `GET /api/v1/denuncias/pendentes` — consome ocorrências não processadas.
     - `PATCH /api/v1/denuncias/:id/triagem` — registra parecer e veredito da IA.
5. **Dashboard Administrativo com Telemetria IA:**
   - HUD de métricas com contadores em tempo real.
   - Aba prioritária para **🚨 Alertas de Revisão Manual** e auditoria rápida com aprovação em 1 clique.
6. **Otimização Avançada para SEO & GEO / IAO (Generative Engine Optimization):**
   - Metadados completos OpenGraph e Twitter Cards.
   - Marcação Schema.org JSON-LD (`Organization`, `WebSite`, `FAQPage`).
   - Rotas técnicas automáticas: `/robots.txt` e `/sitemap.xml`.
   - Conteúdo em micro-resumos otimizado para citação por Perplexity, ChatGPT, Gemini e Copilot.

---

## 🏗️ Estrutura do Projeto

```
.
├── home/                         # Frontend estático e assets
│   ├── index.html                # Versão estática da home
│   ├── css/styles.css            # Design System Cyber-Pink, glassmorphism & ticker
│   └── js/home.js                # Ticker dinâmico, preview de anexo e Scroll-to-Agree
├── backend/
│   ├── app.py                    # Rotas web, APIs REST v1, SEO e segurança
│   ├── database.py               # SQLite com schema de IA, migrações e telemetria
│   ├── profanity.py              # Filtro antiofensa heurístico e sanitização
│   ├── uploads/                  # Provas anexadas com IDs criptográficos
│   └── templates/                # Templates Jinja2 com semântica HTML5
│       ├── base.html             # Base com SEO, JSON-LD e Sticky Ticker
│       ├── home.html             # Hero cyber, micro-resumos e FAQ GEO
│       ├── admin.html            # Dashboard com HUD e telemetria da IA
│       ├── denuncias.html        # Formulário com contrato Scroll-to-Agree
│       ├── denuncias_publicas.html# Feed público com provas auditadas
│       ├── diferencial.html      # Comparativo institucional
│       ├── cadastro.html         # Cadastro protegido
│       ├── login.html            # Autenticação segura
│       ├── recuperar.html        # Recuperação de credenciais
│       ├── ver_denuncia.html     # Detalhamento de protocolo
│       └── excluir_conta.html    # Direito ao esquecimento (LGPD)
├── docs/                         # Documentação técnica, acadêmica e especificações
│   ├── especificacoes/           # Requisitos, Casos de Uso, Wireframes e Doc em Markdown
│   ├── pdf/                      # Documentação compilada em PDF para entrega
│   ├── wireframes/               # Visualização dos wireframes interativos (HTML)
│   └── diagramas/                # Diagramas complementares UML (ex: Diagrama de Classes)
├── db/app.db                     # Banco SQLite (gerado/migrado automaticamente)
├── test_suite.py                 # Suíte de testes automatizados completa
├── run.py                        # Ponto de entrada do servidor
├── Dockerfile                    # Container Docker
├── docker-compose.yml            # Orquestração do container
└── requirements.txt              # Dependências Python
```

---

## 🚀 Como Executar

### 1. Ambiente Local com Python

```bash
# Clone o repositório ou acesse a pasta
cd protejaja

# Crie e ative o ambiente virtual (opcional)
python -m venv .venv
source .venv/bin/activate  # No Windows: .\.venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

# Inicialize o servidor
python run.py
```

Acesse em seu navegador: **<http://127.0.0.1:5000/home>**

### 2. Executando os Testes Automatizados

```bash
python test_suite.py
```

### 3. Execução com Docker

```bash
docker compose up -d --build
```

---

## 🤖 Integração com o Bot Local de IA

Para conectar um bot local ou modelo de linguagem (LLM) ao pipeline:

1. Defina a variável de ambiente:
   ```bash
   export BOT_API_KEY="sua-chave-secreta-aqui"
   ```
2. O bot consome as denúncias pendentes:
   ```http
   GET /api/v1/denuncias/pendentes
   Header: X-API-Key: sua-chave-secreta-aqui
   ```
3. O bot devolve o veredito da triagem:
   ```http
   PATCH /api/v1/denuncias/{id}/triagem
   Header: X-API-Key: sua-chave-secreta-aqui
   Content-Type: application/json

   {
     "status": "ALERTA_REVISAO_MANUAL",
     "score_confianca": 0.82,
     "justificativa_ia": "Linguagem adequada. Detectada duplicidade de ocorrência no mesmo endereço."
   }
   ```