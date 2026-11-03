# Consulta Renda — Mapa de ajustes da documentação

Data do levantamento: 29/10/2026. Atualizado após comparação das duas transcrições. Status: mapa para revisão, sem alterações no site.

## Objetivo e premissas

Reorganizar a proposta para conduzir uma pessoa sem conhecimento prévio da avaliação do produto até a consulta e a leitura dos dados. A documentação será lançada junto à atualização V2 do produto, conforme orientação de Hugo nesta conversa.

A transcrição disponível confirma que o funcionamento geral permanece igual e que mudam o payload e a saída. Isso não permite concluir, sem contrato técnico, que as rotas, os mecanismos de autenticação ou os endpoints terão uma versão nova.

## Fontes e limites de confirmação

- **T — Primeira transcrição:** arquivo `Transcrição.txt`. Contém o início até 0:59 e o final de 56:54 a 59:25.
- **T2 — Nova transcrição:** arquivo `Texto colado.txt`. Contém o início até 6:08 e o encerramento de 59:06 a 59:25. Complementa a primeira; não a substitui.
- **Lacuna conjunta:** entre 6:08 e 56:54. Orientações desse intervalo continuam apoiadas apenas no resumo, sem confirmação literal nas transcrições recebidas.
- **R — Resumo da IA:** arquivo `Markdown colado.md`. Usado como registro de trabalho para as decisões não presentes nos trechos transcritos; sujeito à conferência dos participantes.
- **H — Orientação de Hugo:** lançamento conjunto da documentação e do produto V2.
- **S — Site atual:** conteúdo HTML consultado em 29/10/2026 em https://crv2-rho.vercel.app/Consulta_Renda_Documentacao_Proposta.html. Foi inspecionado o conteúdo, sem teste visual ou funcional da interface.
- **O — Documentação oficial:** introdução e navegação consultadas em https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/. A navegação inclui Metadados, Versionamento e Versão 1.0. Este levantamento não é auditoria completa das páginas técnicas.

A página https://www.loja.serpro.gov.br/consultarenda bloqueou a consulta automatizada. Não foi possível conferir os títulos e a ordem dos seis passos citados na reunião. O plano de negócio, o documento V2 compartilhado por Vitor, o PDF de integração ativa e um contrato OpenAPI homologado V2 não integram os anexos recebidos.

## Mapa de alterações

P0 = iniciar pela estrutura. P1 = conteúdo necessário à jornada e ao lançamento. P2 = revisão final e manutenção. A prioridade é uma proposta de execução deste levantamento.

| ID | Prioridade | Situação atual | Alteração necessária | Critério de conclusão | Base |
| --- | --- | --- | --- | --- | --- |
| M01 | P0 | “Comece aqui” contém visão geral, produto, preparação, primeira consulta e simulação. | Manter visão geral e produto na abertura; apresentar os seis passos em “Entenda o produto antes de contratar”. | Jornada macro reproduz a sequência conferida na Loja e oferece links para o detalhamento. | T 0:10–0:59; R; S |
| M02 | P0 | “Entenda o funcionamento” e “Integre passo a passo” são grupos separados, com FAQ entre a abertura e o funcionamento. | Posicionar um grupo combinado de funcionamento e integração logo após a abertura. O nome mencionado na reunião é provisório. | Menu apresenta uma progressão legível do entendimento para a execução; o nome pode ser refinado depois de organizar o conteúdo. | T2 3:01–4:05; R; S |
| M03 | P0 | Preparação, primeira consulta e simulação aparecem na abertura. | Incorporar essas páginas ao grupo de integração, preservando a utilidade dos exemplos e da validação com payloads. | Todas permanecem acessíveis em contexto e sem duplicação de instruções. | T2 1:55–2:10 confirma a movimentação; manutenção de payloads conforme R; S |
| M04 | P0 | FAQ aparece próximo do início. | Mover o FAQ para o final da estrutura de menus. | Menu final contém o FAQ e os links internos continuam corretos. | T2 2:26–2:43; R; S |
| M05 | P0 | Há grupo “Para agentes” com “Configurar Codex e Claude Code”. | Retirar a configuração de agentes do escopo da entrega inicial; preservar o material de apoio para avaliação posterior. | Jornada pública inicial não depende da configuração de agentes; simulações e payloads continuam no escopo. | R; S |
| M06 | P1 | A página “O que são os tokens e o certificado” contém tabela de componentes, papéis e explicação. | Preservar e ajustar a explicação das peças da integração como glossário; mover a pergunta sobre tokens/certificado para o FAQ. A separação em uma página própria e os links entre conteúdos são uma proposta editorial, não uma decisão literal da reunião. | Bearer token, token de compartilhamento, certificado e chaves têm funções distintas e consistentes em todas as páginas. | T2 4:11–5:18 e 5:35–6:08; R; S |
| M07 | P1 | O site apresenta jornadas resumidas de três e quatro etapas, além de guias distribuídos. | Mapear cada um dos seis passos oficiais às páginas existentes e às lacunas. Reconciliar a visão macro com os detalhamentos e preservar a ordem das dependências técnicas. Explicitar obtenção das credenciais e acolhimento da chave pública no preparo, conforme sequência exemplificada por Henrique, validando o procedimento detalhado. | Nenhuma etapa oficial fica sem explicação, responsável, pré-requisitos, ação e resultado esperado; a preparação identifica credenciais e acolhimento da chave pública antes das etapas que dependem deles. | T 0:10–0:59; T2 1:16–1:39 e 3:17–3:35; R; S |
| M08 | P1 | “Obtenha e localize a autorização” reúne instruções ao titular e consulta técnica da autorização. | Tornar explícitos o ato do titular de autorizar e o procedimento da instituição para identificar essa autorização, posicionados na jornada correta. | Leitor entende quem age em cada momento e como a autorização permite continuar a consulta. | R; S |
| M09 | P1 | “Receba avisos de novas autorizações” remete ao manual/PDF e declara lacunas; o método de autorizações aparece em outro guia. | Explicar integrações ativa e passiva, como a instituição descobre a autorização e como prossegue em cada modalidade. Validar o detalhamento técnico das modalidades com a equipe e aplicar a restrição de escopo M17. | Os dois fluxos têm pré-requisitos, sequência, operação/notificação pertinente, exemplos e falhas documentados a partir de fontes validadas. | T2 1:16 confirma ativa/passiva e exclusão do envio manual; detalhes conforme R e fontes técnicas; S |
| M10 | P1 | A tabela diz que a chave pública protege valores destinados à instituição; outras páginas explicam chaves e descriptografia. | Revisar a redação para explicitar que as informações compartilhadas são criptografadas com a chave pública e descriptografadas pelo receptor com a chave privada correspondente. Revisar a consistência do glossário, guias, FAQ e simulação. | Equipe técnica aprova a explicação e os exemplos; não se inventa o momento ou o componente que realiza a criptografia. | T2 4:44–5:03; R; S |
| M11 | P1 | “Entenda os dados retornados” já tem estrutura de resposta e tabela de campos; “Entenda versões e mudanças” já discute versões. | Criar entrada explícita de metadados e reorganizar o conteúdo existente em subseções V1 e V2, cobrindo campos e agrupamentos aplicáveis. | Cada conjunto identifica a versão e explica código/nome, significado, tipo, formato, unidade e regras de ausência, conforme fonte técnica disponível. | R; S; O |
| M12 | P1 | O conjunto de campos usa a fonte pública V1; não há dicionário V2 identificado. | Preencher a seção V2 a partir do documento de referência de Vitor e validar payloads/saídas com a equipe. | Campos, agrupamentos e exemplos V2 são rastreáveis à referência aprovada. | T 58:25–58:57; R; S |
| M13 | P1 | “Entenda versões e mudanças”, histórico e pendências tratam V2 como planejamento; exemplos e bases observadas usam `/v1`. | Atualizar a narrativa para o lançamento conjunto e distinguir produto, contrato/rotas da API e versão do conjunto de metadados. Separar conteúdo específico sem reescrever o fluxo comum como se fosse outra jornada. | Textos refletem o estado aprovado do lançamento; nenhuma URL `/v2`, compatibilidade ou descontinuação é presumida. | T 58:25–58:57; H; S |
| M14 | P1 | O botão OpenAPI disponibiliza, segundo o contexto do projeto, um contrato ilustrativo; exemplos e simulação também precisam de alinhamento por versão. | Revisar referência, exemplos, códigos de resposta, download e simulação frente ao contrato da entrega V2. Para publicação oficial, disponibilizar contrato homologado e exemplos coerentes. | Materiais ilustrativos estão identificados durante revisão; referência produtiva corresponde ao contrato homologado. | H; S; dependência técnica do lançamento identificada neste mapa |
| M15 | P2 | Busca, navegação entre páginas, destaques, FAQ, índice e referências dependem da organização atual. | Após reorganizar, atualizar índice de busca, breadcrumbs, anterior/próxima, links, âncoras e títulos. Na implementação, manter gerador, estilos e comportamento sincronizados com o HTML principal. | Todas as páginas são localizáveis, sequência faz sentido e não há links internos quebrados. | S; consequência da reorganização |
| M16 | P2 | Existem páginas internas de padrão editorial, validações e fontes. | Atualizar a matriz de pendências com decisões da reunião, fontes e responsáveis. Decidir o destino das páginas internas antes da publicação ao cliente. | Pendências técnicas têm fonte e responsável; a versão publicada possui conteúdo aprovado para o público definido. | R; S; recomendação editorial |
| M17 | P1 | A exclusão do envio manual não estava registrada na primeira edição deste mapa. | Restringir a jornada desta entrega às integrações ativa e passiva. Não incluir o envio manual como procedimento ou alternativa do passo a passo; revisar instruções e exemplos para respeitar esse recorte. | O tutorial apresenta apenas os dois caminhos definidos. A exclusão é de escopo documental desta entrega e não afirma inexistência ou desativação de uma funcionalidade do produto. | T2 1:16; complementar a M09 |

## Destino proposto para os conteúdos atuais

Esta distribuição é proposta de implementação do mapa. Não representa um menu integralmente aprovado na reunião.

| Conteúdo atual | Destino proposto | Tratamento |
| --- | --- | --- |
| Visão geral | Comece aqui | Manter como porta de entrada; alinhar com a jornada de seis passos. |
| Entenda o produto antes de contratar | Comece aqui | Acrescentar jornada macro de seis passos, após conferir a fonte. |
| Prepare a integração | Funcionamento e integração | Mover e relacionar ao preparo necessário na jornada oficial. |
| Faça sua primeira consulta | Funcionamento e integração | Manter tutorial guiado, distinguindo demonstração e produção. |
| Explore a jornada com dados fictícios | Funcionamento e integração | Manter validação didática e revisar exemplos por versão aplicável. |
| O que são os tokens e o certificado | FAQ + glossário de integração | Resposta curta no FAQ; explicações de referência no glossário. |
| Obtenha o token de acesso | Funcionamento e integração | Posicionar conforme dependências técnicas, sem equiparar bearer à autorização. |
| Obtenha e localize a autorização | Funcionamento e integração | Distinguir ação do titular e identificação pela instituição; considerar ligação com as duas modalidades de integração. |
| Receba avisos de novas autorizações | Funcionamento e integração | Reorganizar como parte da integração ativa e criar explicação correspondente da passiva. |
| Descriptografe os valores recebidos | Funcionamento e integração | Posicionar após consulta/recebimento e revisar a explicação de chaves. |
| Entenda os dados retornados | Metadados → V1 e V2 | Reaproveitar o conteúdo V1; incluir V2 conforme referência técnica. |
| Entenda versões e mudanças | Metadados/versionamento + referência técnica quando aplicável | Distinguir os diferentes controles de versão e atualizar o contexto do lançamento. |
| Ambientes e cobrança; Referência das operações; Resolva o problema pela etapa; Peça ajuda com o contexto certo | Referência e operação | Preservar como consulta rápida; alinhar com o contrato e regras vigentes. |
| Configurar Codex e Claude Code | Apoio para etapa futura | Retirar da entrega inicial conforme resumo, preservando o material. |
| Dúvidas frequentes | Final da navegação | Mover e incorporar pergunta sobre tokens/certificado. |
| Padrão proposto; Validações; Fontes e manutenção | Material de revisão interna, com destino editorial a decidir | Atualizar pendências e separar o que serve ao cliente do que serve à revisão. |

## Estrutura de navegação para discutir

1. **Comece aqui:** Visão geral; Entenda o produto antes de contratar, com os seis passos.
2. **Funcionamento e integração** — título final a definir: preparação; glossário; jornada técnica detalhada; primeira consulta; simulação. A ordem definitiva das etapas depende do mapeamento dos seis passos e das dependências de cada modalidade.
3. **Metadados:** explicação do versionamento; versão 1.0; versão 2.0.
4. **Referência e operação:** operações, ambientes/cobrança, diagnóstico e suporte.
5. **FAQ:** último bloco da navegação.

A posição relativa entre Metadados e Referência e operação é uma proposta deste levantamento. O resumo não comprova que essa ordem tenha sido fechada na reunião. O material de gestão deve ter destino decidido antes da publicação.

## Mapeamento dos seis passos: o que já sabemos

| Etapa citada | Evidência | Material que pode ser aproveitado | Informação necessária |
| --- | --- | --- | --- |
| Contratação do serviço | T e T2, 0:59 | Produto, preparação, credenciais, ambientes/cobrança | Título e escopo exatos do passo na Loja; alinhamento com plano de negócio. |
| Autorização do titular | T e T2, 0:59 | Guia de autorização/compartilhamento; instruções ao titular | Texto oficial do passo e fluxo vigente de autorização. |
| Geração dos tokens de autorização e integrações ativa/passiva | T2, 1:16 | Guias de autorização e notificações; excluir envio manual conforme M17 | Confirmar a divisão nos passos oficiais e os procedimentos técnicos. Não confundir esses tokens com o bearer token. |
| Consulta na API | T2, 1:16 | Referência de consulta e tutorial | Confirmar posição e título na jornada oficial. |
| Disponibilização das chaves para descriptografia na ponta | T2, 1:33–1:39 | Preparação e guia de descriptografia | Esclarecer procedimento, papéis e proteção das chaves com a equipe técnica; a menção na fala não define distribuição da chave privada. |

As falas mencionam esses assuntos, mas não enumeram claramente os seis títulos oficiais. Não se deve converter as cinco linhas acima em uma jornada oficial nem inventar um sexto passo. O exemplo técnico de Henrique sobre credenciais e acolhimento da chave pública (T2, 3:17) orienta o detalhamento, sem estabelecer por si só um dos seis títulos da Loja.

Para cada passo confirmado, registrar: objetivo; quem executa; requisitos; ação; resultado esperado; página de destino; fonte; lacuna; responsável pela validação.

## Dependências e perguntas objetivas

| Dependência | O que obter ou confirmar | Responsável sugerido |
| --- | --- | --- |
| Jornada oficial | Quais são os seis títulos e sua ordem? Qual versão da página da Loja foi usada na reunião? | Hugo, com Vitor |
| Plano de negócio | Qual revisão deve fundamentar escopo, condições e descrição do produto? | Vitor/Henrique |
| Documento V2 | Quais campos, agrupamentos, exemplos, formatos e regras mudam na saída? | Vitor + equipe técnica |
| Contrato técnico | Mudam rotas/base, parâmetros, autenticação, erros ou apenas o conteúdo retornado? | Equipe técnica |
| Integrações ativa e passiva | Quais os procedimentos de cada modalidade citada na reunião? Como se identifica a autorização em cada uma? Quais payloads e requisitos do receptor estão aprovados? Aplicar a exclusão do envio manual da entrega inicial. | Henrique/equipe técnica |
| Versionamento | V1/V2 se referem a produto, conjunto de metadados e/ou contrato da API em cada página? Como a autorização determina o conjunto retornado? | Equipe técnica + gestão |
| Convivência com V1 | Há datas aprovadas de convivência, migração e descontinuação? | Gestão + equipe técnica |
| Agenda | Qual o mês/ano do dia 21 e a data exata da quarta-feira mencionada? | Hugo/Vitor |
| Validação do registro | Os participantes confirmam os itens que só constam no resumo da IA? | Hugo, Vitor e Henrique |

## Ordem de execução

**Entrega 1 — Estrutura revisável.** Ajustar grupos de menu, mover páginas, posicionar FAQ no final e retirar agentes da entrega inicial. Criar destinos de metadados V1/V2 com pendências identificadas. Preservar o conteúdo existente enquanto se organiza.

**Entrega 2 — Matriz da jornada.** Conferir os seis passos e relacionar Loja, plano de negócio, documentação oficial e proposta. Identificar o que reaproveitar, reescrever e criar; explicitar o preparo de credenciais e acolhimento da chave pública, além da restrição a integrações ativa/passiva, sem envio manual.

**Entrega 3 — Conteúdo técnico.** Completar autorização, modalidades ativa/passiva, criptografia, metadados e saída V2 com as fontes técnicas. Alinhar exemplos, contrato OpenAPI e regras por versão.

**Entrega 4 — Revisão para publicação.** Resolver pendências com responsáveis, conferir links/busca/navegação e validar a jornada com alguém sem conhecimento prévio do produto. Registrar a versão técnica e as fontes aprovadas.

## Prazos e assuntos paralelos

A transcrição confirma homologação no **dia 21**, com material pronto aproximadamente **cinco dias a uma semana antes** (57:53–57:59). O mês e o ano não estão explícitos; não é possível transformar isso em data de entrega confirmada. O resumo menciona quarta-feira, das 15h30 às 16h, mas esse agendamento não está no trecho transcrito disponibilizado.

Segundo o resumo, contrato deve manter visão macro e pode apontar para a documentação técnica. Isso é uma frente de gestão/contrato, não um requisito para acrescentar detalhes contratuais ao tutorial. O trecho final confirma que o plano de negócio ainda estava em revisão (57:09), sem confirmar a decisão do link no contrato.

## Critérios gerais de aceite

- Uma pessoa sem familiaridade com o produto entende a jornada completa e sabe o que deve fazer em seguida.
- Os seis passos apresentados são os confirmados na fonte e têm correspondência com os guias técnicos.
- Autorização do titular, bearer token, token de compartilhamento e leitura dos dados não se confundem.
- Integrações ativa e passiva explicam como a instituição identifica a autorização e continua o processo. O envio manual fica fora do passo a passo desta entrega.
- O preparo identifica obtenção das credenciais e acolhimento da chave pública, com ordem e procedimento validados tecnicamente.
- Metadados V1 e V2 são identificados e exemplos não misturam conjuntos de campos.
- O conteúdo V2 deriva de documentação técnica aprovada, sem supor uma rota `/v2`.
- Contrato OpenAPI, exemplos e explicações são coerentes com a entrega homologada.
- Menu, busca, links, índice e navegação refletem a nova estrutura.
- O FAQ está no final e agentes de programação ficam fora da entrega inicial.
- Pendências de publicação possuem decisão ou responsável e não são apresentadas como funcionalidades confirmadas.


## Registro da atualização após a nova transcrição

- **Tarefa nova M17:** excluir envio manual do passo a passo desta entrega, mantendo integrações ativa e passiva (T2, 1:16).
- **M07 detalhada:** explicitar credenciais e acolhimento da chave pública na preparação e preservar a ordem das dependências (T2, 3:17–3:35). É detalhamento de tarefa existente, sem criar uma jornada oficial de seis passos por dedução.
- **Confirmações acrescentadas:** M02 (grupo combinado e nome provisório), M03 (movimentação das três páginas), M04 (FAQ no final), M06 (FAQ e preservação do glossário), M09 (modalidades de integração) e M10 (criptografia) passam a ter evidência direta na T2, nos limites indicados em cada linha.
- **M06 esclarecida:** preservar a explicação como glossário é orientação direta; uma página independente de glossário é solução editorial proposta.
- **Evidências preservadas da primeira transcrição:** prazo de homologação e mudanças de payload/saída da V2.
- **Ainda dependentes do resumo:** separação dos metadados V1/V2, retirada de agentes da entrega inicial, decisão de link no contrato e horário do ponto de controle, entre outros assuntos do intervalo ausente.
