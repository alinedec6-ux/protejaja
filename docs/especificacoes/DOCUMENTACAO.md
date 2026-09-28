# ProtejaJA — Documentação Técnica

Projeto integrador de plataforma de denúncias. Este documento descreve a visão geral do sistema, a arquitetura utilizada, as funcionalidades implementadas, as medidas de segurança e a documentação relativa ao banco de dados e à infraestrutura.

---

## Resumo Executivo da Sprint

Na sprint atual, o ProtejaJA avançou em três frentes:

1. **Segurança**: o cadastro exige nome e sobrenome separados, e a exclusão de conta remove definitivamente cadastro, denúncias e provas.
2. **Moderação**: o painel do administrador permite aprovar ou rejeitar cada denúncia; somente as aprovadas são publicadas na página pública.
3. **Documentação**: requisitos funcionais (RF01–RF14) e não funcionais (RNF01–RNF09), casos de uso (UC01–UC08) e wireframes atualizados e entregues em PDF.

---

## 1. Visão Geral

**ProtejaJA** é uma aplicação web de denúncias. O usuário cria uma conta, realiza login e registra uma denúncia contra um estabelecimento, empresa ou pessoa, com a possibilidade de anexar uma prova (imagem, PDF ou vídeo). As denúncias passam por um processo de moderação do administrador antes de serem publicadas.

- **Autor da denúncia:** usuário autenticado.
- **Autor do fato denunciado:** estabelecimento, empresa ou pessoa.
- **Prova:** anexo opcional de imagem, PDF ou vídeo.
- **Exclusão de dados:** o usuário pode excluir a conta e todos os seus dados.

### Stack Tecnológica

| Camada | Tecnologia | Versão | Finalidade |
|---|---|---|---|
| Front-end | HTML + Tailwind CSS + CSS | Tailwind via CDN | Interface com tema unificado |
| Back-end | Python + Flask | Python 3.14 / Flask 3.1 | Lógica, validações e rotas |
| Banco de dados | SQLite | Nativo | Persistência de usuários e denúncias |
| Contêiner | Docker | Docker + Docker Compose | Portabilidade e execução |

---

## 2. Arquitetura: Front-end, Back-end e Banco de Dados

O sistema segue o modelo cliente-servidor com três camadas:

| Camada | Responsabilidade | Tecnologia |
|---|---|---|
| Front-end | Apresentação ao usuário (telas, formulários e navegação) | HTML + CSS + Tailwind |
| Back-end | Processamento das requisições, validações e regras de negócio | Python + Flask |
| Banco de dados | Persistência dos dados (usuários e denúncias) | SQLite |

### Fluxo de uma requisição

```
Usuário preenche o formulário (front-end)
        ↓ envia a requisição
Flask processa (back-end)
        ↓ grava/busca
SQLite armazena os dados (banco)
        ↑ retorna
A tela exibe o resultado (front-end)
```

### Organização do código

| Camada | Arquivos |
|---|---|
| Front-end | `backend/templates/*.html`, `home/css/styles.css` |
| Back-end | `backend/app.py`, `backend/database.py`, `backend/profanity.py` |
| Banco de dados | `db/app.db` (gerado por `backend/database.py`) |

---

## 3. Funcionalidades Implementadas

### 3.1 Home
- Página inicial com tema rosa, letras pretas e botões de destaque.
- Ações: **Criar conta** e **Entrar**.

### 3.2 Cadastro
- Campos obrigatórios: **nome**, **sobrenome** (separados), e-mail, data de nascimento, cidade, senha e endereço completo.
- Exige o preenchimento de nome e sobrenome.
- A senha é armazenada como hash (criptografia) antes da gravação.
- Após o cadastro, o usuário é direcionado para a tela de login.

### 3.3 Login
- Autenticação por e-mail e senha.
- Link de acesso à recuperação de senha.

### 3.4 Recuperação de senha
- Valida e-mail e data de nascimento.
- Em caso de correspondência, gera e exibe uma senha temporária.

### 3.5 Denúncias
O formulário de denúncia contém os seguintes campos:

| Campo | Descrição |
|---|---|
| Quem você está denunciando? | Estabelecimento, empresa ou pessoa |
| Sobre o quê? | Assunto do problema |
| Categoria | Tipo: produto, local, serviço, etc. |
| Descrição | Detalhamento do ocorrido |
| Prova (anexo) | Imagem, PDF ou vídeo |

Após o envio, a denúncia aparece em **"Minhas denúncias"**. A página **"Ver detalhes"** exibe a descrição completa e a prova anexada.

### 3.6 Exclusão de conta
- Acesso pelo ícone **🗑️** no menu.
- Exige confirmação com a senha.
- Remove definitivamente o cadastro, as denúncias e as provas armazenadas.

### 3.7 Painel do administrador (moderação)
- Conta de administrador criada automaticamente: `admin@protejaja.com`.
- O link **🛡️ Painel admin** é exibido apenas para usuários administradores.
- O administrador visualiza todas as denúncias e pode **aprovar** ou **rejeitar** cada uma.

### 3.8 Página pública de denúncias
- Acesso pelo link **"Ver denúncias"** no menu, sem necessidade de login.
- Exibe apenas as denúncias **aprovadas** pelo administrador.
- Ciclo de publicação: usuário denuncia → administrador aprova → conteúdo publicado.

---

## 4. Segurança

O sistema adota as seguintes medidas de segurança:

1. **Senha criptografada** — a senha é armazenada como hash (scrypt, via Werkzeug/Flask), nunca em texto puro.
2. **Filtro antiofensa** — bloqueia palavras ofensivas em nome, sobrenome, endereço, descrição, assunto e campo "quem está denunciando".
3. **Prevenção de SQL Injection** — todas as consultas utilizam parâmetros preparados (`?`).
4. **Autenticação obrigatória** — o envio de denúncia exige login; cada usuário visualiza apenas as próprias denúncias.
5. **Exclusão definitiva** — a exclusão da conta exige senha e remove os arquivos do disco.

---

## 5. Banco de Dados

O banco é composto por duas tabelas:

| Tabela | Conteúdo | Campos principais |
|---|---|---|
| `users` | Usuários | nome, email, data_nascimento, cidade, endereco, senha_hash |
| `reports` | Denúncias | denunciado, assunto, categoria, descricao, anexo, status |

- A tabela `reports` possui `user_id` como chave estrangeira para `users`.
- O arquivo do banco fica em `db/app.db`.

---

## 6. Estrutura de Arquivos

| Arquivo | Função |
|---|---|
| `run.py` | Inicializa o servidor Flask na porta 5000 |
| `backend/app.py` | Definição das rotas e regras de negócio |
| `backend/database.py` | Criação das tabelas e operações de persistência |
| `backend/profanity.py` | Filtro de palavras ofensivas |
| `backend/templates/` | Páginas HTML do sistema |
| `home/` | Estilos CSS e script da página inicial |
| `Dockerfile` | Definição da imagem do contêiner |
| `docker-compose.yml` | Orquestração do serviço e preservação dos dados |

---

## 7. Docker e Portabilidade

- O **Dockerfile** define a imagem com a aplicação e suas dependências.
- O **docker-compose.yml** expõe o serviço na porta 5000 e preserva banco de dados e uploads por meio de volumes.

Execução:

```powershell
docker compose up -d --build
```

---

## 8. Conformidade e Segurança de Dados

### 8.1 LGPD

O projeto aplica princípios da LGPD no contexto de um sistema de ensino:

| Princípio | Aplicação no ProtejaJA |
|---|---|
| Privacidade desde a concepção | Coleta somente dos dados necessários |
| Segurança dos dados | Senha criptografada e login obrigatório |
| Direito à exclusão | Exclusão da conta remove cadastro e denúncias |
| Controle de acesso | Cada usuário visualiza apenas os próprios registros |

Em um projeto de ensino não há empresa real, portanto não são exigidos instrumentos como DPO e termo de consentimento. Para uma implantação em produção, seriam necessários documento de política de privacidade e termo de consentimento.

### 8.2 Veracidade dos dados

O cadastro é autodeclarado, sem verificação externa da identidade. Em cenários de produção, a confirmação seria reforçada por mecanismos como:
- Confirmação por e-mail (link de verificação).
- Validação de CPF.

### 8.3 Criptografia

| Dado | Proteção |
|---|---|
| Senha | Hash com scrypt (Werkzeug) — não armazenada em texto puro |
| Transporte | HTTPS quando a aplicação estiver publicada na internet |
| Anexos | Armazenamento no disco do servidor, restrito a usuários autenticados |

---

## 9. Requisitos de Execução

Pré-requisitos: Docker e Docker Compose instalados.

```
docker compose up -d --build
```

Acesso: http://127.0.0.1:5000/home