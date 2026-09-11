# ProtejaJA — Requisitos Funcionais e Não Funcionais

> Trabalho para apresentar para a sala. Explicação simples, no ritmo de quem
> aprende devagar e sem enrolação.

---

## 1. Primeiro, a diferença (do jeito fácil)

Pense no **celular**:

| | Exemplo |
|---|---|
| **Funcional** = O QUE o sistema FAZ | "Ligar", "tirar foto", "enviar mensagem" |
| **Não funcional** = COMO ele faz isso | "a bateria dura o dia", "a câmera é rápida", "o celular é leve" |

**Agora no ProtejaJA:**

| Tipo | Pergunta que responde | Exemplo aqui |
|---|---|---|
| **Funcional** | O QUE o site faz? | O usuário pode **cadastrar**, **entrar**, **denunciar** |
| **Não funcional** | COMO ele faz? | Senha **criptografada**, site **rápido**, fácil de usar |

> REGRA DE OURO PARA NÃO CONFUNDIR:
> - Se você consegue **VER/CLICAR** a ação → é funcional.
> - Se é uma **qualidade/escondido** (segurança, velocidade, cor) → é não funcional.

**QUE DIZER:**
> "Requisito funcional é o que o sistema faz — cadastrar, logar, denunciar.
> Requisito não funcional é como ele faz bem — senha criptografada,
> carregamento rápido e aparência agradável."

---

## 2. Requisitos Funcionais (O QUE o ProtejaJA faz)

Cada item é uma **ação** que o usuário pode realizar.

| Código | Requisito Funcional | Onde acontece |
|---|---|---|
| RF01 | O sistema deve permitir **cadastrar usuário** (nome completo, e-mail, data de nascimento, cidade, endereço completo e senha). | Tela Cadastro |
| RF02 | O sistema deve **criptografar a senha** antes de guardar no banco. | Cadastro |
| RF03 | O sistema deve permitir **login** com e-mail e senha. | Tela Login |
| RF04 | O sistema deve permitir **sair da conta** (logout). | Menu |
| RF05 | O sistema deve permitir **recuperar a senha** conferindo e-mail + data de nascimento e gerando senha temporária. | Tela Recuperar |
| RF06 | O sistema deve permitir registrar **denúncia** com os campos: quem está denunciando, sobre o que é, categoria e descrição. | Tela Denúncias |
| RF07 | O sistema deve permitir **anexar prova** (imagem, PDF ou vídeo) à denúncia. | Tela Denúncias |
| RF08 | O sistema deve **listar as denúncias** de cada usuário. | Tela Denúncias |
| RF09 | O sistema deve **bloquear palavras ofensivas** (nome, endereço, denunciado, assunto e descrição). | Todas as telas |
| RF10 | O sistema deve **exigir login** para enviar denúncia. | Tela Denúncias |

**QUE DIZER (leia a RF06 como exemplo):**
> "Exemplo de requisito funcional: RF06 — o usuário pode registrar uma denúncia.
> Ele informa quem ele está denunciando — por exemplo, o Savegnago —, sobre o que é,
> a categoria e a descrição, e ainda pode anexar uma prova."

---

## 3. Requisitos Não Funcionais (COMO o ProtejaJA faz)

São as **qualidades** e **regras escondidas** do sistema. Não dá para "clicar" nelas.

| Código | Requisito Não Funcional | Tipo |
|---|---|---|
| RNF01 | As páginas devem carregar em poucos segundos. | Desempenho |
| RNF02 | A senha DEVE ficar criptografada (nunca em texto puro). | Segurança |
| RNF03 | O sistema deve resistir a **SQL Injection** (consultas com parâmetros). | Segurança |
| RNF04 | Anexos: no máximo **5 MB** e só imagens, PDF ou vídeo. | Segurança |
| RNF05 | Aparência: **telas centralizadas, fundo rosa, letras pretas, botões rosa escuro**. | Usabilidade / Design |
| RNF06 | Deve funcionar em navegadores modernos (usando Tailwind via CDN). | Compatibilidade |
| RNF07 | Deve rodar em qualquer máquina com **Docker** (portabilidade). | Portabilidade |
| RNF08 | Os dados (banco e uploads) devem **sobreviver ao reinício** do sistema. | Confiabilidade |
| RNF09 | Código organizado em partes (templates, banco, filtro) para fácil manutenção. | Manutenibilidade |

**QUE DIZER:**
> "Nos requisitos não funcionais estão a segurança e a qualidade: a senha nunca
> fica em texto puro, os anexos têm limite de 5 MB, as telas são rosas e
> centralizadas, e o projeto roda em qualquer lugar com Docker."

---

## 4. Tabela-resumo (para fixar)

| Pergunta | Resposta |
|---|---|
| Funcional responde qual pergunta? | O que o sistema FAZ |
| Não funcional responde qual pergunta? | COMO o sistema faz |
| Funcional vira verbo? | Sim: cadastrar, logar, denunciar |
| Não funcional é qualidade? | Sim: segurança, velocidade, cor |
| Exemplo funcional | RF06 — registrar denúncia |
| Exemplo não funcional | RNF02 — senha criptografada |

---

## 5. Roteiro da apresentação (passo a passo)

1. "Boa noite. Eu vim explicar os requisitos do site ProtejaJA, um site de denúncias."
2. **Mostrar a diferença:** "Funcional é o que faz; não funcional é como faz."
3. **Ler 2 funcionais:** RF01 (cadastro) e RF06 (denúncia com o exemplo do Savegnago).
4. **Ler 2 não funcionais:** RNF02 (senha criptografada) e RNF05 (tema rosa centralizado).
5. **Fechar:** "Os funcionais descrevem as telas e ações; os não funcionais garantem segurança, desempenho e boa aparência."

> Dica para treinar: leia este PDF **em voz alta** uma vez por dia até o dia da apresentação.