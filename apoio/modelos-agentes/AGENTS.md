# Instruções de projeto para agentes de código

> Modelo para copiar para a raiz do repositório da aplicação que integrará a Consulta Renda. Não é configuração do portal SERPRO. Ajuste-o às convenções reais do repositório.

## Objetivo

Integrar a API Consulta Renda ao software existente. Siga a arquitetura, a linguagem, as ferramentas e as convenções já adotadas pelo projeto. Não crie serviços, dependências ou estruturas paralelas sem necessidade demonstrada.

## Antes de implementar

1. Leia as instruções do repositório, o código relacionado à integração e os testes existentes.
2. Consulte a documentação oficial atual em <https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/> e o contrato OpenAPI/Swagger publicado por ela.
3. Explique o fluxo que pretende implementar: credenciais → bearer token → autorização do titular → consulta → descriptografia → tratamento do resultado.
4. Compare as operações e erros com estas divergências já observadas: `/Consultar` aparece com parâmetros diferentes entre páginas; `/Status` e `/status` têm grafias diferentes; 404 e 503 têm descrições divergentes; o momento do cadastro da chave pública não está descrito da mesma forma em todas as páginas.
5. Não apresente um detalhe divergente como confirmado. Se o contrato vigente não resolver a divergência, pare essa parte e informe qual decisão precisa vir da equipe técnica. Continue as etapas independentes e sem ambiguidade.

## Segurança e limites

- Nunca faça requisições ao ambiente de produção, consuma uma autorização real, solicite credenciais ao usuário nem altere configurações de contrato.
- Não gere, grave, mostre, registre, teste nem inclua em exemplos reais Consumer Key, Consumer Secret, bearer token, token de compartilhamento, CPF, CNPJ de cliente ou chave privada.
- Leia segredos por um mecanismo já existente no projeto. Se não houver um, proponha uma interface segura e documente como configurá-la; use valores fictícios nos exemplos e testes.
- Proteja tokens e dados de renda contra logs, rastreamento, mensagens de erro, capturas de tela, fixtures versionadas e respostas de ferramentas.
- Use somente respostas, certificados e identificadores sintéticos nos testes locais. Não use renda para gerar score, recomendação ou decisão sobre uma pessoa.
- Não mude vigência ou revogação de autorização, destinatário, contrato, cobrança, ambiente produtivo ou publicação sem solicitação explícita do usuário.

## Integração e verificação

- Trate bearer token e token de compartilhamento como valores distintos, cada qual no ponto indicado pelo contrato confirmado.
- Separe autenticação, busca de autorização, consulta, descriptografia, mapeamento de campos e erros; valide a operação antes de interpretar valores.
- Não interprete ausência de declaração, valor ausente, falha de descriptografia ou erro HTTP como renda zero.
- Use os nomes, tipos, formatos, política de cobrança e comportamento de repetição publicados no contrato atual. Não adivinhe formatos de valores depois da descriptografia.
- Siga as práticas de testes já existentes. Prefira provas unitárias offline com dados sintéticos. Não chame o gateway durante uma verificação local.
- Ao concluir, informe arquivos alterados, verificações executadas e resultado, configurações que o usuário ainda precisa fornecer e toda decisão técnica pendente. Não imprima segredos.

## Referências

- Documentação oficial: <https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/>
- Prompt de trabalho reutilizável: `apoio/modelos-agentes/PROMPT_integracao_consulta_renda.md` (copie-o para o repositório ou use-o como tarefa inicial).
