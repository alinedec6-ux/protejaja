# ProtejaJA — Requisitos Funcionais e Não Funcionais

Este documento especifica os requisitos do sistema ProtejaJA, organizados em requisitos funcionais (o que o sistema faz) e requisitos não funcionais (como o sistema se comporta e suas qualidade).

---

## 1. Conceitos

| Tipo | Pergunta que responde | Exemplo |
|---|---|---|
| **Funcional** | O que o sistema faz? | Cadastrar, entrar, registrar denúncia |
| **Não funcional** | Como o sistema executa? | Senha criptografada, carregamento rápido |

---

## 2. Requisitos Funcionais

| Código | Requisito Funcional | Local |
|---|---|---|
| RF01 | O sistema deve permitir cadastrar usuário com nome e sobrenome separados (ambos obrigatórios), e-mail, data de nascimento, cidade, endereço completo e senha. | Tela Cadastro |
| RF02 | O sistema deve criptografar a senha antes de armazená-la no banco. | Cadastro |
| RF03 | O sistema deve permitir o login com e-mail e senha. | Tela Login |
| RF04 | O sistema deve permitir sair da conta (logout). | Menu |
| RF05 | O sistema deve permitir recuperar a senha mediante e-mail e data de nascimento, gerando senha temporária. | Tela Recuperar |
| RF06 | O sistema deve permitir registrar denúncia com os campos: quem está denunciando, sobre o quê, categoria e descrição. | Tela Denúncias |
| RF07 | O sistema deve permitir anexar prova (imagem, PDF ou vídeo) à denúncia. | Tela Denúncias |
| RF08 | O sistema deve listar as denúncias de cada usuário. | Tela Denúncias |
| RF09 | O sistema deve bloquear palavras ofensivas (nome, endereço, denunciado, assunto e descrição). | Todas as telas |
| RF10 | O sistema deve exigir login para enviar denúncia. | Tela Denúncias |
| RF11 | O sistema deve exibir os detalhes de uma denúncia (descrição completa e prova). | Ver detalhes |
| RF12 | O sistema deve permitir excluir a conta definitivamente (cadastro, denúncias e provas), com confirmação por senha. | Menu |
| RF13 | O sistema deve dispor de um painel do administrador para visualizar as denúncias e aprovar ou rejeitar cada uma. | Painel admin |
| RF14 | O sistema deve exibir publicamente apenas as denúncias aprovadas, sem exigir login. | Página pública |

---

## 3. Requisitos Não Funcionais

| Código | Requisito Não Funcional | Tipo |
|---|---|---|
| RNF01 | As páginas devem carregar em poucos segundos. | Desempenho |
| RNF02 | A senha deve ser armazenada criptografada, nunca em texto puro. | Segurança |
| RNF03 | O sistema deve resistir a SQL Injection mediante consultas com parâmetros. | Segurança |
| RNF04 | Os anexos devem ter no máximo 5 MB e aceitar apenas imagens, PDF ou vídeo. | Segurança |
| RNF05 | A interface deve apresentar telas centralizadas, fundo rosa, letras pretas e botões rosa escuro. | Usabilidade / Design |
| RNF06 | O sistema deve funcionar em navegadores modernos (Tailwind via CDN). | Compatibilidade |
| RNF07 | O sistema deve executar em qualquer máquina com Docker. | Portabilidade |
| RNF08 | Os dados (banco e uploads) devem persistir após o reinício do sistema. | Confiabilidade |
| RNF09 | O código deve ser organizado em camadas (templates, banco, filtro) para facilitar a manutenção. | Manutenibilidade |

---

## 4. Resumo

| Pergunta | Resposta |
|---|---|
| Funcional responde a qual pergunta? | O que o sistema faz |
| Não funcional responde a qual pergunta? | Como o sistema faz |
| Exemplo de funcional | RF06 — registrar denúncia |
| Exemplo de não funcional | RNF02 — senha criptografada |