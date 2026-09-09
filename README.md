# ProtejaJA — Projeto Integrador

Plataforma de denúncias com **Python + Flask + SQLite + Tailwind CSS**. Páginas centralizadas com tema rosa, letras pretas e botões rosa escuro.

## Funcionalidades

- **Cadastro** — nome completo, e-mail, data de nascimento, cidade, endereço completo e senha.
- **Login** — com link visível para **recuperação de senha**.
- **Recuperação de senha** — gera senha temporária validando e-mail + data de nascimento.
- **Denúncias** — envio de descrição com **anexo de prova** (imagem, PDF ou vídeo do lugar/produto) e listagem das denúncias do usuário.
- **Segurança**:
  - Senhas **criptografadas** (hash `scrypt` via Werkzeug) — nunca armazenadas em texto puro (ver `backend/app.py`).
  - **Filtro antiofensa** que bloqueia e sanitiza palavras de baixo calão e ofensas, inclusive variações com acentos e "leet speak" (`backend/profanity.py`).
  - Consultas parametrizadas, sessão com login obrigatório para denúncias, upload validado por extensão (máx. 5 MB) com nome seguro.

## Estrutura

```
.
├── home/                  # PASTA HOME — front-end (página inicial, CSS e JS)
│   ├── index.html         # versão estática da home
│   ├── css/styles.css     # tema rosa centralizado
│   └── js/home.js         # alertas automáticos e preview de anexo
├── backend/
│   ├── app.py             # rotas: cadastro, login, logout, recuperar, denúncias
│   ├── database.py        # SQLite: tabelas users e reports
│   ├── profanity.py       # filtro antiofensa + sanitização
│   ├── requirements.txt
│   ├── uploads/           # provas anexadas (criada automaticamente)
│   └── templates/         # base, home, cadastro, login, recuperar, denuncias
├── db/app.db              # banco SQLite (criado automaticamente)
├── run.py                 # ponto de entrada
└── README.md
```

## Como rodar

```powershell
cd "C:\Users\aline\OneDrive\Documentos\Default Project"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python run.py
```

Abrir no navegador: <http://127.0.0.1:5000/home>

## Fluxo

1. `/cadastro` — cria a conta (valida e-mail, senha mínima, endereço, cidade e nome sem ofensas).
2. Botão de envio leva ao `/login`.
3. `/login` — acesso com link visível para `/recuperar`.
4. `/denuncias` — requer login; envia descrição + anexo e lista suas denúncias.

> Nota: troque `SECRET_KEY` por um valor aleatório ao publicar (ver `backend/app.py`).