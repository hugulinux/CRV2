# Documentação Consulta Renda — proposta

Arquivo principal: `../Consulta_Renda_Documentacao_Proposta.html`.

Proposta local de documentação, com revisão editorial em 22/10/2026. Não é uma publicação oficial nem homologação da API. O HTML é independente, sem bibliotecas remotas, e funciona offline; links para fontes requerem internet.

A arquitetura combina Diátaxis, descrição técnica OpenAPI e princípios de redação do Google. Stripe é uma referência de organização por jornada, não um padrão normativo.

A proposta descreve o produto com base nas páginas públicas da Consulta Renda e na referência Swagger renderizada. A documentação acompanha a atualização V2 do produto, com mudanças informadas no payload e na saída. As decisões e validações pendentes estão em `STATUS_AJUSTES_DOCUMENTACAO.md`.

A simulação é didática, com dados inventados. Nenhum botão executa chamadas à API. Os exemplos de integração devem ser homologados com a equipe técnica antes da publicação oficial.

O arquivo preexistente `ConsultaRenda-Doc 3.html` foi lido como contexto e preservado.

## Registros da versão anterior

- 21 páginas. A versão anterior passou por conferência de estrutura e links; esta revisão acrescenta uma página de dúvidas e deve ser reaberta no navegador antes de compartilhar.
- HTML sem dependências remotas de scripts, fontes ou imagens.
- Sintaxe do JavaScript conferida pelo Node.js.
- Exemplo de descriptografia executado com chave PKCS#12 e resposta inteiramente sintéticas, em memória.
- Nenhuma chamada à API real foi executada.

A conferência visual da versão anterior ficou pendente: o navegador da sessão bloqueou o protocolo `file:`. Abra o HTML no navegador do computador para revisar a apresentação antes de compartilhar.

Para regenerar o HTML após alterações, execute `apoio/gerar_documentacao.py` com Python. O gerador incorpora `portal.css` e `portal.js` no arquivo final. `apoio/verificar_modelo.py` verifica a estrutura e o exemplo sintético (requer o pacote cryptography).

## Configuração de agentes para uma aplicação cliente

Em `apoio/modelos-agentes/` estão modelos reutilizáveis para copiar à raiz do repositório da aplicação que integrará o produto:

- `AGENTS.md`: instruções comuns para agentes de código e reconhecidas pelo Codex.
- `CLAUDE.md`: importa `AGENTS.md` e acrescenta orientações de início para Claude Code.
- `PROMPT_integracao_consulta_renda.md`: tarefa inicial com campos para adaptar ao repositório e ao escopo.

Os modelos não são instruções para este projeto de documentação, nem instalam credenciais, ferramentas ou cliente HTTP. A página sobre agentes foi retirada da jornada inicial e permanece na fonte para avaliação posterior.
