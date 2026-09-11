# ProtejaJA — Wireframe das Telas e Manipulação de Imagem

> Trabalho para apresentar para a sala. Primeiro vem o **wireframe** (o esboço
> de cada tela) e depois a parte de **imagem** (visual, cores e como o sistema
> trata as imagens/provas).

---

## PARTE 1 — WIREFRAME (o esboço das telas)

**O que é um wireframe?**
É o **rascunho** da tela: mostra onde ficam os botões, campos e textos, antes
de "colorir". É a planta baixa do site.

> Idem celular: o wireframe é como a planta da casa; depois vem a pintura.

---

### 1.1 Wireframe — Tela Home

```
+----------------------------------------------------------+
| Logo ProtejaJA      Home   Entrar   [Cadastrar]   (menu) |
+----------------------------------------------------------+
|                                                          |
|                 (etiqueta) Projeto Integrador            |
|                                                          |
|                ## ProtejaJA  ##                          |
|                                                          |
|          "Plataforma para registrar denúncias            |
|           com segurança..."                              |
|                                                          |
|   [ SENHAS ]      [ FILTRO ]       [ ANEXO ]             |
|   criptografadas  antiofensa        de prova             |
|      (card)          (card)           (card)             |
|                                                          |
|        [ Criar conta ]        [ Entrar ]                 |
|                                                          |
+----------------------------------------------------------+
```

**Características:** título centralizado, 3 cards explicativos, botão rosa.

---

### 1.2 Wireframe — Tela Cadastro (card central)

```
+----------------------------------------------------------+
| Logo ProtejaJA      Home   Entrar   [Cadastrar]   (menu) |
+----------------------------------------------------------+
|              +-----------------------------+              |
|              |     Criar conta             |              |
|              |  Preencha seus dados...     |              |
|              |-----------------------------|              |
|              | Nome completo  [________]   |              |
|              | E-mail         [________]   |              |
|              | Data nasc.     [________]   |              |
|              | Cidade  [___] | Senha [___] |              |
|              | Endereço completo [_______] |              |
|              | [    CADASTRAR    ] (rosa)  |              |
|              | Já tem conta? Entrar        |              |
|              +-----------------------------+              |
+----------------------------------------------------------+
```

**Só 6 campos:** nome, e-mail, data de nascimento, cidade, senha e endereço.

---

### 1.3 Wireframe — Tela Login (card central)

```
+----------------------------------------------------------+
| Logo ProtejaJA      Home   Entrar   [Cadastrar]   (menu) |
+----------------------------------------------------------+
|              +-----------------------------+              |
|              |        Entrar               |              |
|              |  Acesse sua conta...        |              |
|              |-----------------------------|              |
|              | E-mail  [________]          |              |
|              | Senha   [________]          |              |
|              | [    ENTRAR    ] (rosa)     |              |
|              |                             |              |
|              | Esqueceu a senha?           |              |
|              |  > Recuperar senha (link)   |              |
|              +-----------------------------+              |
+----------------------------------------------------------+
```

**Destaque:** link **Recuperar senha** bem visível (pedido do professor).

---

### 1.4 Wireframe — Tela Denúncias (a principal)

```
+----------------------------------------------------------+
| Logo ProtejaJA   Home  Denúncias  Olá, X    [Sair] (menu)|
+----------------------------------------------------------+
|  Enviar denúncia                                          |
| --------------------------------------------------------- |
| | Quem você está denunciando? *  [ Savegnago      ]   |   |
| | Sobre o que? *                [ Produto vencido ]   |   |
| | Categoria [ Produto  v ]                             |  |
| | Descrição [______________________]                   |  |
| | Prova (anexo) [ Escolher arquivo ] faixa de 5MB      |  |
| | [     ENVIAR DENÚNCIA    ] (rosa)                    |  |
| --------------------------------------------------------- |
|                                                          |
|  Minhas denúncias                                        |
| --------------------------------------------------------- |
| | (Produto) 12/09/2026                                  |  |
| | **Savegnago**  Produto vencido                        |  |
| | Comprei e não quiseram trocar...  📎 Ver anexo        |  |
| --------------------------------------------------------- |
+----------------------------------------------------------+
```

**Esta tela tem os campos pedidos pelo professor:**
1. Quem você está denunciando? (ex.: **Savegnago**)
2. Sobre o que? (ex.: produto vencido)
3. Categoria
4. Descrição
5. Anexo de prova (imagem/PDF/vídeo)

---

### 1.5 Wireframe — Tela Recuperar Senha

```
+----------------------------------------------------------+
| Logo ProtejaJA          (menu)                            |
+----------------------------------------------------------+
|              +-----------------------------+              |
|              |     Recuperar senha         |              |
|              |  e-mail + data de nascimento|              |
|              |-----------------------------|              |
|              | E-mail  [________]          |              |
|              | Data nasc. [________]       |              |
|              | [ GERAR SENHA TEMPORÁRIA ]  |              |
|              +-----------------------------+              |
+----------------------------------------------------------+
```

**Resultado:** se os dados batem, o sistema **mostra a senha temporária** na tela.

---

## PARTE 2 — MANIPULAÇÃO DE IMAGEM

### 2.1 A identidade visual (cores do projeto)

O tema é **rosa** com **letras pretas** e **botões rosa escuro** (decisão de design).

| Elemento | Cor | Código (hex) |
|---|---|---|
| Fundo da página (gradiente) | Rosa claro | #ffe4e6 → #fecdd3 |
| Botão principal | **Rosa escuro** | #be123c |
| Botão ao passar o mouse | Rosa escuro mais forte | #9f1239 |
| Letras (texto) | **Preto/** | #0f172a |
| Fundo dos cards | Branco | #ffffff |
| Borda dos cards | Rosa claro | #fecdd3 |
| Etiqueta/categoria | Rosa claro | #ffe4e6 |

**QUE DIZER:**
> "A identidade visual usa o rosa: fundo rosa claro, botões rosa escuro e letras
> pretas. As telas são centralizadas para facilitar a leitura."

### 2.2 Como o site "manipula" as imagens (provas de denúncia)

O site recebe a imagem e faz um tratamento antes de guardar:

1. **Verifica o tipo** — só aceita: `png, jpg, jpeg, gif, webp, heic/heif, pdf, mp4, mov`.
2. **Limita o tamanho** — máximo de **5 MB** (evita travar o site).
3. **Renomeia com nome seguro** — função `secure_filename` remove caracteres perigosos do nome do arquivo.
4. **Salva em pasta separada** — `backend/uploads/`, fora das denúncias.
5. **Gera pré-visualização** — o JavaScript lê o arquivo e mostra uma **miniatura** com redimensionamento via CSS (`object-fit`, bordas arredondadas) antes de enviar.

Fluxo da imagem:

```
Usuário escolhe a foto
      |
      v
Navegador mostra miniatura (pré-visualização)
      |
      v
Servidor verifica tipo + tamanho (máx 5MB)
      |
      v
Salva com nome seguro em /uploads
      |
      v
Denúncia lista o anexo com link "Ver anexo"
```

**QUE DIZER:**
> "A imagem passa por um tratamento: o navegador mostra uma prévia, o servidor
> confere o tipo e o tamanho (5 MB no máximo), salva com nome seguro e a denúncia
> exibe o anexo com um botão 'Ver anexo'."

### 2.3 Manipulação visual no front-end (CSS)

Elementos de imagem tratados pelo `home/css/styles.css`:

| Recurso | Para que serve |
|---|---|
| Gradiente rosa (`.pagina-rosa`) | Fundo suave da página |
| Cards `border-radius` e sombra rosa | Efeito "caixa branca" sobre o rosa |
| Botão `.btn-rosa` com hover | Feedback visual ao passar o mouse |
| Miniatura do anexo | `object-cover`, bordas arredondadas (na prévia) |
| Telas centralizadas | Facilita o foco e a leitura |

**QUE DIZER (para encerrar):**
> "O wireframe mostra onde fica cada elemento; a manipulação de imagem garante
> que as provas entrem com segurança, com prévia, tamanho controlado e
> visual rosa padronizado."

---

## Roteiro da apresentação (passo a passo)

1. "Bom dia! Este é o wireframe do ProtejaJA, o site de denúncias."
2. **Mostrar o wireframe da Home** → "Aqui está o menu e os botões."
3. **Mostrar Cadastro/Login** → "Formulários simples e centralizados."
4. **Mostrar a tela de Denúncias** → "Aqui o usuário denuncia quem, sobre o quê, e anexa a prova." (exemplo: **Savegnago**)
5. **Falar das cores** → "Rosa claro no fundo, botão rosa escuro, letras pretas."
6. **Falar da manipulação de imagem** → "A imagem é validada (tipo e 5 MB), vira prévia e é salva com segurança."

> Dica: imprima/leia este PDF em voz alta uma vez por dia até a apresentação.