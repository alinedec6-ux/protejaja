# CASOS DE USO — ProtejaJA

**Projeto Integrador · Flask + SQLite + Tailwind CSS**

## 1. Diagrama (visão geral)

```
            ┌──────────────────┐
            │    VISITANTE     │   (não logado)
            └──────────────────┘
                 │
                 │  UC01 Cadastrar-se
                 │  UC02 Entrar (login)
                 ▼
        ┌──────────────────────┐
        │       ProtejaJA      │
        │  Sistema de Denúncias │
        └──────────────────────┘
                 ▲
                 │
            ┌──────────────────┐
            │     USUÁRIO      │   (logado)
            └──────────────────┘
                 │
                 │  UC03 Enviar denúncia
                 │  UC04 Anexar prova
                 │  UC05 Ver minhas denúncias
                 │  UC06 Ver detalhes de uma denúncia
                 │  UC07 Sair
                 ▼
```

O participante sem conta (Visitante) pode passar pelo UC01 e UC02 para se tornar Usuário. Somente o Usuário logado acessa as denúncias.

## 2. Tabela dos casos de uso

| Código | Caso de uso | Ator principal | Objetivo |
|---|---|---|---|
| UC01 | Cadastrar-se | Visitante | Criar conta com nome, e-mail, data de nascimento, cidade, endereço e senha |
| UC02 | Entrar | Visitante | Acessar a conta com e-mail e senha |
| UC03 | Recuperar senha | Visitante | Receber senha temporária informando e-mail + data de nascimento |
| UC04 | Enviar denúncia | Usuário | Registrar quem está denunciando, o quê, categoria e descrição |
| UC05 | Anexar prova | Usuário | Enviar imagem/PDF/vídeo (máx. 5 MB) junto à denúncia |
| UC06 | Ver minhas denúncias | Usuário | Listar apenas as denúncias da própria conta |
| UC07 | Ver detalhes de uma denúncia | Usuário | Abrir uma denúncia e ver a prova anexada |
| UC08 | Sair | Usuário | Encerrar a sessão com segurança |

## 3. Casos de uso em detalhe (alguns exemplos)

### UC04 — Enviar denúncia

1. Usuário entra em **Minhas denúncias**.
2. Informa **quem está denunciando** (ex.: Hipermercado).
3. Informa **sobre o quê** (ex.: produto vencido).
4. Escolhe a **categoria** (produto, serviço, local...).
5. Escreve a **descrição** (filtro antiofensa valida o texto).
6. (Opcional) **anexa a prova**.
7. Clica em **Enviar denúncia**.
8. Sistema salva e mostra a denúncia na lista.

**Exceções:** se a descrição tiver ofensa, o sistema bloqueia e pede outro texto.

### UC05 — Anexar prova

1. Usuário clica em **Escolher arquivo**.
2. Seleciona imagem/PDF/vídeo.
3. Se o arquivo passar de 5 MB, o sistema avisa e não envia.

### UC08 — Sair

1. Usuário clica em **Sair** no menu.
2. Sistema encerra a sessão e volta para a Home.

## 4. Fontes dos casos de uso

Esses casos de uso foram tirados do que o site já faz (rotas em `backend/app.py`):
- `/cadastro`, `/login`, `/recuperar`, `/denuncias`, `/logout`.