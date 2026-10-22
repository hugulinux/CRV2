# Tarefa para o agente: integrar a Consulta Renda

Adapte os campos entre colchetes antes de iniciar.

```text
Leia AGENTS.md e as instruções aplicáveis no repositório antes de alterar arquivos.

Objetivo de negócio: [descreva o fluxo do produto que precisa consultar renda].
Repositório/componente: [caminho ou nome, se não for óbvio].
Linguagem e convenções: [deixe em branco para seguir o que já existe].
Escopo deste trabalho: [especifique o que entra nesta tarefa].

Comece pelo fluxo técnico e pelas instruções oficiais atuais:
https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/

Antes de codificar, localize no contrato Swagger/OpenAPI publicado as operações,
parâmetros, respostas, códigos HTTP e formatos necessários. A documentação
consultada contém divergências sobre a rota de consulta, a grafia de /status,
o significado de alguns retornos e o momento do cadastro da chave pública.
Liste o que confirmou e o que permanece contraditório. Não invente a resposta;
peça a decisão da equipe técnica para o trecho bloqueado e avance nas partes
independentes.

Implemente a jornada que couber ao escopo: obter bearer token, localizar a
autorização do titular, consultar com o token de compartilhamento, descriptografar
conforme o contrato e certificado confirmados, e tratar erros sem transformar
ausência ou falha em renda zero. Reutilize arquitetura e componentes existentes.

Limites obrigatórios: não chame o ambiente de produção; não use nem solicite
credenciais, CPFs, CNPJs de cliente ou tokens reais; não registre valores ou
dados pessoais em logs, mensagens, fixtures ou capturas de tela; não altere
contrato, autorização, destinatário, cobrança ou configuração de produção. Use
somente dados sintéticos em testes locais. Não tome decisões ou gere score sobre
pessoas com base nos dados consultados.

Verificação: siga o fluxo de testes existente, use dados sintéticos e não
conecte os testes ao gateway. Documente passos de configuração sem incluir
segredos e confirme o comportamento esperado para sucesso, autorização ausente,
declaração ausente, erro de acesso, indisponibilidade e falha de descriptografia,
conforme os retornos que o contrato vigente realmente documentar.

Ao terminar, relate arquivos alterados, verificações e resultados, configuração
que o operador ainda precisa fazer e divergências que aguardam decisão técnica.
Nunca mostre valores de credenciais, tokens ou dados de renda.
```

Antes de reutilizar este prompt, confira se o escopo se aplica ao repositório e
substitua os campos entre colchetes. O prompt orienta o agente; não provisiona
credenciais nem substitui a aprovação da equipe para qualquer operação real.
