# ProtejaJA — Documentação para Explicar (formato fácil, passo a passo)

> Objetivo deste documento: você conseguir **explicar** o projeto na apresentação,
> entendendo cada parte sem se perder. Vá com calma, uma seção por vez.
> Cada seção tem um quadro **"O QUE DIZER"** com a frase pronta para a banca.

---

## 1. VISÃO GERAL — O que é o ProtejaJA?

**ProtejaJA** é um site de **denúncias**. A pessoa cria uma conta, entra, e faz uma
denúncia (ex.: comprar produto vencido no Savegnago e não quererem trocar).

- **Quem denuncia** → qualquer usuário cadastrado.
- **Quem é denunciado** → estabelecimento / empresa / pessoa (ex.: **Savegnago**).
- **Prova** → o usuário pode anexar imagem, PDF ou vídeo.

**As 3 tecnologias (salve isso):**
| Parte | Ferramenta | Para que serve |
|---|---|---|
| Tela (front-end) | HTML + **Tailwind** + CSS | Aparência rosa, botões, centralizar |
| Servidor (back-end) | **Python + Flask** | Lógica, validações, rotas |
| Banco de dados | **SQLite** | Guardar os dados (usuários e denúncias) |

**QUE DIZER:**
> "O ProtejaJA é um site de denúncias. O usuário se cadastra, faz login e denuncia
> alguém ou alguma empresa, podendo anexar uma prova. O sistema bloqueia ofensas
> e guarda a senha de forma criptografada."

---

## 2. O CAMINHO DOS DADOS (como as 3 partes se falam)

```
     1) Você digita na TELA
    2) A TELA envia para o SERVIDOR (Flask)
    3) O SERVIDOR valida e grava no BANCO (SQLite)
    4) O SERVIDOR devolve a resposta para a TELA
```

**QUE DIZER:**
> "O fluxo é: o usuário preenche o formulário, o Flask recebe, valida os dados,
> grava no SQLite e responde com a página. É um serviço cliente-servidor
> com banco de dados."

---

## 3. AS TELAS (uma por uma)

### 3.1 Home (página inicial)
- Título grande **ProtejaJA**, cor rosa, letras pretas.
- Botões: **Criar conta** e **Entrar**.

### 3.2 Cadastro
- Campos: **nome completo, e-mail, data de nascimento, cidade, senha, endereço completo**.
- Senha transformada em **hash** (criptografia) antes de gravar.
- Depois de salvar → **vai para a tela de login**.

### 3.3 Login
- E-mail + senha.
- Link visível: **"Recuperar senha"**.

### 3.4 Recuperar senha
- Pede e-mail + data de nascimento.
- Se bater, gera **senha temporária** e mostra na tela.

### 3.5 Denúncias (a tela mais importante)
O formulário tem **5 campos** (a banca vai adorar isso):

| Campo | O que é | Exemplo |
|---|---|---|
| **Quem você está denunciando?** | O estabelecimento/empresa | Savegnago |
| **Sobre o que?** | O problema | Produto vencido |
| **Categoria** | Tipo | Produto / Local / Serviço |
| **Descrição** | Detalhe do acontecido | Comprei vencido e não trocam |
| **Prova (anexo)** | Imagem/PDF/vídeo | Foto do produto |

Depois de enviada, aparece em **"Minhas denúncias"** com quem, o quê e a foto.

**QUE DIZER (da tela de denúncia):**
> "Aqui o usuário informa quem está sendo denunciado e o que aconteceu.
> Por exemplo: comprou um produto vencido no Savegnago e não quiseram trocar.
> Ele digita Savegnago, anexa a foto do produto vencido e envia."

---

## 4. A SEGURANÇA (4 pontos que a banca adora)

1. **Senha criptografada** — o banco guarda só um hash, nunca a senha.
2. **Filtro antiofensa** — bloqueia palavras ofensivas no nome, endereço, descrição e em "quem está denunciando".
3. **Sem SQL Injection** — as consultas usam `?` (parâmetros), nunca texto colado.
4. **Login obrigatório** — só dá para denunciar logado; cada usuário só vê as próprias denúncias.

**QUE DIZER:**
> "Senhas nunca ficam em texto puro: viram um hash. O texto digitado passa
> pelo filtro antiofensa, que bloqueia xingamentos. As consultas ao banco
> usam parâmetros, evitando SQL Injection, e só usuários logados podem denunciar."

---

## 5. O BANCO DE DADOS (2 tabelas)

| Tabela | Guarda | Campos principais |
|---|---|---|
| `users` | Usuários | nome, email, data_nascimento, cidade, endereco, **senha_hash** |
| `reports` | Denúncias | **denunciado**, **assunto**, categoria, descricao, anexo |

- Cada denúncia tem `user_id` que liga ao dono da conta (chave estrangeira).
- O banco fica no arquivo `db/app.db`.

**QUE DIZER:**
> "São duas tabelas: users e reports. A denúncia guarda quem foi denunciado
> (denunciado), sobre o que (assunto), a descrição e o anexo, além do usuário
> que fez a denúncia."

---

## 6. OS ARQUIVOS (o que cada um faz, sem decoreba)

| Arquivo | Papel | O que ele faz no meu projeto |
|---|---|---|
| `run.py` | Liga o servidor | Inicia o Flask na porta 5000 |
| `backend/app.py` | Cérebro | Todas as rotas: cadastro, login, recuperar, denúncias |
| `backend/database.py` | Banco | Cria tabelas, salva e busca usuários/denúncias |
| `backend/profanity.py` | Filtro | Lista de ofensas + normalização (pega até "c@r@lho") |
| `backend/templates/` | Telas | HTML de cada página |
| `home/` | Visual | CSS rosa e o JS da home |
| `Dockerfile` | Container | Empacota o projeto para rodar em qualquer máquina |

**Sugestão para a banca:** abra só 2 arquivos e aponte:
- `app.py` → onde a senha é criptografada (`generate_password_hash`).
- `profanity.py` → a lista de palavras bloqueadas.

---

## 7. DOCKER (se perguntarem "como roda em qualquer lugar?")

- **Dockerfile** → a "receita" da imagem (Python + código).
- **docker-compose.yml** → sobe o site na porta 5000 e preserva banco + uploads.

Rode com:
```powershell
docker compose up -d --build
```

**QUE DIZER:**
> "Com o Docker, qualquer pessoa roda o projeto com um único comando,
> sem precisar instalar nada manualmente. Os dados ficam em volumes,
> então não se perdem quando o container reinicia."

---

## 8. PLANO DA APRESENTAÇÃO (6 passos, com o que falar)

1. **Abrir** a Home → "Este é o ProtejaJA, site de denúncias."
2. **Cadastrar** um usuário → "Preencho nome, data de nascimento, cidade e endereço." (mostrar que foi para o login)
3. **Entrar** → "E-mail e senha; aqui tem o link de recuperar senha."
4. **Denunciar** → "Vou denunciar o Savegnago por produto vencido" → preencher os campos + anexar foto → enviar.
5. **Mostrar a denúncia** listada com "Savegnago" e a foto.
6. **Segurança** → "Senha fica só como hash; e as ofensas são bloqueadas" (se possível, digite um xingamento e mostre o bloqueio).

---

## 9. COMO RODAR (se precisar demonstrar)

```powershell
docker compose up -d --build
```
Abrir: http://127.0.0.1:5000/home

---

## 10. DICAS PARA QUEM TEM TDAH (para você)

- Explique a **ordem da história**: cadastro → login → denúncia → segurança.
- Não decore código: decore os **4 cartões** (o que é, como fala com o banco, as telas, a segurança).
- Se esquecer uma palavra, está tudo aqui em **"QUE DIZER"**.
- Treine 2 vezes na frente do espelho/imprimindo este PDF e lendo em voz alta.