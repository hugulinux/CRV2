from pathlib import Path
from html import escape
import json
import base64

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/'
PAGES = []

def link(path, label):
    url = path if path.startswith('https://') else BASE + path
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label} <span aria-label="abre em outra aba">↗</span></a>'

def refs(*items):
    return '<div class="sources"><strong>Fontes desta página</strong><p>' + ' · '.join(link(p, t) for p,t in items) + '</p></div>'

def table(headers, rows):
    return '<div class="table-scroll"><table><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def note(title, body, kind='info'):
    return f'<aside class="callout {kind}"><strong>{title}</strong><p>{body}</p></aside>'

def code(text, lang='Bash / cURL'):
    return f'<div class="codebox"><div class="codebar"><span>{lang}</span><button class="copy" type="button">Copiar código</button></div><pre><code>{escape(text.strip())}</code></pre></div>'

def page(id, group, title, lead, body, kind='Guia prático'):
    PAGES.append(dict(id=id,group=group,title=title,lead=lead,body=body,kind=kind))

AUTH = r'''curl --request POST \
  --url 'https://gateway.apiserpro.serpro.gov.br/token' \
  --user "${CONSUMER_KEY}:${CONSUMER_SECRET}" \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data 'grant_type=client_credentials'
'''
QUERY = r'''curl --request GET \
  --url "https://gateway.apiserpro.serpro.gov.br/renda-pf/v1/Consultar/${TOKEN_COMPARTILHAMENTO}" \
  --header "Authorization: Bearer ${ACCESS_TOKEN}" \
  --header 'Accept: application/json' \
  --output resposta.json \
  --write-out 'HTTP %{http_code}\n'
'''
AUTHORIZATIONS = r'''curl --request GET \
  --url "https://gateway.apiserpro.serpro.gov.br/renda-pf/v1/Autorizacoes/${CNPJ_CONTRATANTE}/${CPF_TITULAR}" \
  --header "Authorization: Bearer ${ACCESS_TOKEN}" \
  --header 'Accept: application/json'
'''
STATUS = r'''curl --request GET \
  --url 'https://gateway.apiserpro.serpro.gov.br/renda-pf/v1/status' \
  --header "Authorization: Bearer ${ACCESS_TOKEN}" \
  --header 'Accept: application/json'
'''
DECRYPT = '''# Exemplo proposto: Python + pacote cryptography.
# Entrada: resposta.json de uma consulta HTTP 200 e certificado PKCS#12.
# Use o certificado correspondente à chave pública usada na resposta.
import base64
import json
from getpass import getpass
from pathlib import Path
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import rsa, padding

arquivo = Path(input("Caminho do certificado .p12/.pfx: ").strip())
senha = getpass("Senha do certificado (vazia se não houver): ")
chave, certificado, cadeia = pkcs12.load_key_and_certificates(
    arquivo.read_bytes(), senha.encode("utf-8") if senha else None
)
if not isinstance(chave, rsa.RSAPrivateKey):
    raise ValueError("É necessária uma chave privada RSA compatível.")

resposta = json.loads(Path("resposta.json").read_text(encoding="utf-8"))
if not isinstance(resposta.get("dados"), list):
    raise ValueError("Resposta sem lista dados. Confira o HTTP da consulta.")

dados_legiveis = []
for item in resposta["dados"]:
    cifrado = base64.b64decode(item["valor"], validate=True)
    claro = chave.decrypt(cifrado, padding.PKCS1v15())
    dados_legiveis.append({
        "codigo": item["codigo"],
        "texto": item["texto"],
        "valor": claro.decode("utf-8")
    })

# Integre dados_legiveis ao processo autorizado da sua aplicação.
# Evite registrar o conteúdo em logs de diagnóstico.
print(f"{len(dados_legiveis)} campos descriptografados em memória.")
'''

page('inicio','Comece aqui','Consulta Renda: como consultar os dados',
     'Entenda o que a API entrega e siga as etapas para integrar.',
'''<div class="hero-grid"><div><h2 class="hero-title">Dados da declaração de IRPF, com autorização do titular.</h2><p>A instituição contratante consulta as informações pela API. Os valores chegam criptografados e precisam ser descriptografados pela própria instituição.</p><div class="actions"><a class="button primary" href="#primeira-consulta">Testar na demonstração</a><a class="button" href="#produto">Ver o que é fornecido</a></div></div><div class="journey-mini" aria-label="Etapas da consulta"><div><b>1</b><span><strong>O titular autoriza</strong><small>Compartilha os dados com a instituição</small></span></div><div><b>2</b><span><strong>A instituição consulta</strong><small>A aplicação usa a API e o token da autorização</small></span></div><div><b>3</b><span><strong>A instituição lê a resposta</strong><small>Descriptografa e interpreta os campos</small></span></div></div></div>
<h2>Por onde começar</h2><nav class="start-links" aria-label="Escolha por onde começar"><a href="#produto"><strong>Estou avaliando o produto</strong><span>Consulte os dados disponíveis, os limites de uso e os requisitos de contratação.</span><b>O que a API fornece →</b></a><a href="#primeira-consulta"><strong>Vou integrar a API</strong><span>Comece pela demonstração e avance para a configuração de produção.</span><b>Testar uma consulta →</b></a><a href="#erros"><strong>Encontrei um problema</strong><span>Identifique a operação e o código HTTP para decidir o próximo passo.</span><b>Consultar erros →</b></a></nav>
<h2>Antes de abrir o código</h2><p>Você encontrará dois tokens com funções diferentes: um permite acessar a API; o outro identifica a autorização do titular. O certificado e sua chave privada permitem ler os valores recebidos. <a href="#conceitos">Veja como essas peças se relacionam.</a></p><p>Se já conhece a API e precisa consultar endpoints, parâmetros e formatos, vá direto à <a href="#referencia">referência técnica</a>. Se está começando, siga primeiro o guia de integração.</p>
<div class="strip"><div><strong>Exemplo sem chamadas reais</strong><p>Explore a jornada com dados fictícios no próprio arquivo.</p></div><a class="button" href="#simulacao">Explorar exemplo →</a></div>
''' + note('Sobre este documento','Esta é uma proposta para revisão. A página <a href="#gestao">Validações antes da publicação</a> lista divergências que precisam de confirmação técnica.','quiet') + refs(('', 'Documentação oficial'),('chamadas/api_reference/','Referência da API')), 'Visão geral')

page('produto','Comece aqui','Entenda o produto antes de contratar',
     'Saiba o que a Consulta Renda entrega e quais recursos sua instituição precisa ter.',
'''<h2>O que você recebe</h2><p>A Consulta Renda fornece informações de renda e patrimônio presentes na última declaração de IRPF transmitida pelo titular à Receita Federal. A instituição destinatária acessa esse conjunto por API, após o compartilhamento autorizado.</p><p>O retorno inclui valores consolidados, ano-calendário e informações de ocupação. Consulte o <a href="#dados">dicionário de dados</a> para avaliar a adequação ao seu processo.</p>
<h2>Em poucas palavras</h2><p>O titular autoriza o compartilhamento com a instituição que contratou o serviço. A instituição usa a API para consultar os dados da declaração. Os valores chegam protegidos e precisam ser lidos pela aplicação usando a chave privada correspondente ao certificado cadastrado.</p>
<h2>Como interpretar o alcance do produto</h2><ul><li>Os dados refletem o que foi declarado pelo contribuinte. Considere a referência temporal ao utilizá-los.</li><li>A declaração pode conter rendimentos de diferentes origens. A API não fornece, por si só, uma decisão de crédito ou um cálculo de salário mensal atual.</li><li>A autorização é concedida a um destinatário. A contratação e o acesso técnico precisam estar preparados para utilizá-la.</li></ul>
<h2>O que o produto não decide por você</h2><p>A API entrega informações da declaração; a avaliação de elegibilidade, risco, renda mensal ou concessão de crédito continua sendo responsabilidade da instituição e das regras do seu processo. Não interprete ausência de declaração ou ausência de um campo como renda igual a zero.</p>
<h2>O que sua instituição precisa preparar</h2>''' + table(['Responsável sugerido','Preparação','Como saber que está pronto'],[
('Negócio / contratação','Definir finalidade, volume esperado e condições comerciais.','Caso de uso definido e contrato ativo.'),
('Responsável pelo certificado','Disponibilizar e-CNPJ e organizar o uso da chave privada.','Equipe sabe qual certificado corresponde à integração.'),
('Desenvolvimento','Implementar autenticação, consulta e leitura do retorno.','Consegue percorrer a demonstração e tratar falhas.'),
('Operação / atendimento','Preparar orientação ao titular e tratamento de incidentes.','Sabe localizar a etapa da falha e acionar suporte.')]) +
'''<h2>Contratação e custos</h2><p>O FAQ informa contratação por empresas brasileiras públicas ou privadas com e-CNPJ. A página comercial contém a tabela de preços; consulte-a no momento da contratação. As regras por operação estão em <a href="#ambientes">Ambientes e cobrança</a>.</p><div class="actions">''' + link('https://www.loja.serpro.gov.br/consultarenda','Consultar condições na Loja Serpro') + '''<a class="button primary" href="#preparacao">Preparar a integração →</a></div>''' + refs(('','Introdução'),('faq/','FAQ'),('como_contratar/','Como contratar')), 'Explicação')

page('preparacao','Comece aqui','Prepare a integração',
     'Organize os acessos antes de pedir à sua equipe que faça a primeira consulta.',
'''<h2>O que você precisa ter antes de começar</h2><p>Este preparo é para a instituição contratante e sua equipe técnica. Você não precisa ter dados do titular para explorar a demonstração. Para produção, a instituição precisa ter contrato ativo, credenciais e certificado preparados, além de um fluxo para obter autorização do titular e localizar o compartilhamento.</p><h2>Escolha seu caminho</h2><div class="card-grid two"><a class="card" href="#primeira-consulta"><h3>Quero aprender sem dados reais</h3><p>Use a demonstração oficial com dados fixos para conhecer as chamadas e o formato da resposta.</p><strong>Ir para a demonstração →</strong></a><a class="card" href="#conceitos"><h3>Preciso planejar o trabalho técnico</h3><p>Conheça os papéis, os dois tokens e a função do certificado antes de definir a implementação.</p><strong>Entender os componentes →</strong></a></div><h2>Checklist de produção</h2><p class="muted">Marque os itens para acompanhar sua preparação. As marcações ficam apenas neste navegador, quando o armazenamento local estiver disponível.</p><div class="checklist" data-checklist="preparacao">''' + ''.join(f'<label><input type="checkbox" data-key="p{i}"><span><strong>{a}</strong><small>{b}</small></span></label>' for i,(a,b) in enumerate([
('Contrato ativo','Confira a situação na Área do Cliente.'),
('Consumer Key e Consumer Secret disponíveis','A equipe responsável consegue obtê-las e protegê-las.'),
('Chave pública cadastrada','Siga o processo de visualização de chaves com o certificado na Área do Cliente, descrito na página de criptografia.'),
('Chave privada correspondente acessível à aplicação','Defina com sua equipe como o certificado será utilizado para descriptografar.'),
('Fluxo de autorização definido','Escolha como localizar a autorização concedida pelo titular.'),
('Tratamento de respostas e cobrança previsto','Leia os retornos por operação e prepare o acompanhamento de consumo.'),
('Responsável por suporte definido','Registre quem acompanha erros e encaminha evidências.')] )) + '''</div><p id="check-progress" class="progress-label" aria-live="polite"></p>
<h2>Como obter suas credenciais</h2><ol><li>Conclua a contratação e a assinatura exigida no fluxo comercial.</li><li>Acesse a Área do Cliente e confirme a ativação do serviço.</li><li>Siga a orientação oficial para visualizar as chaves do produto.</li><li>Associe o certificado utilizado ao processo da aplicação responsável por ler o retorno.</li></ol><p>O cadastro da chave pública é chamado de <strong>acolhimento</strong> na documentação. A página de criptografia o associa à consulta ou geração das credenciais. A área de gestão registra uma descrição divergente em metadados.</p>''' + refs(('como_contratar/','Contratação'),('criptografia/','Acolhimento'),('https://centraldeajuda.serpro.gov.br/duvidas/pt/area-do-cliente/chaves/','Obter chaves'),('https://cliente.serpro.gov.br/','Área do Cliente')))

page('duvidas','Ajuda e dúvidas','Dúvidas frequentes',
     'Respostas diretas sobre o produto, contratação, compartilhamento e integração.',
'''<p>As respostas abaixo foram escritas para esta proposta a partir das dúvidas que aparecem no FAQ oficial e nas páginas do produto. Quando as fontes públicas divergem, a resposta aponta a pendência em vez de escolher uma versão sem validação.</p>
<h2>Produto e contratação</h2><div class="faq-list">
<details><summary>O que a Consulta Renda entrega?</summary><p>A API consulta informações presentes na declaração de Imposto de Renda da Pessoa Física que o titular autorizou compartilhar com a instituição. Veja a <a href="#produto">descrição do produto</a> e a <a href="#dados">lista de campos</a>.</p></details>
<details><summary>Os dados representam a renda atual da pessoa?</summary><p>Não necessariamente. O retorno está ligado às informações e ao ano-calendário da declaração. Não trate o resultado como salário mensal atual nem como decisão de crédito. Consulte <a href="#dados">Entenda os dados retornados</a>.</p></details>
<details><summary>Quem pode contratar?</summary><p>O FAQ oficial informa que empresas brasileiras, públicas ou privadas, podem contratar, desde que tenham certificado e-CNPJ padrão ICP-Brasil. Confira as <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/como_contratar/" target="_blank" rel="noopener noreferrer">instruções oficiais de contratação</a> e os requisitos comerciais vigentes.</p></details>
<details><summary>Onde vejo preço e condições comerciais?</summary><p>Consulte a <a href="https://www.loja.serpro.gov.br/consultarenda" target="_blank" rel="noopener noreferrer">página do produto na Loja Serpro</a>. Preços e condições podem mudar; confirme-os antes de dimensionar o consumo.</p></details>
<details><summary>Onde encontro as credenciais depois de contratar?</summary><p>A página oficial direciona o cliente à <a href="https://cliente.serpro.gov.br/" target="_blank" rel="noopener noreferrer">Área do Cliente</a>, onde ficam informações do contrato e credenciais. O guia <a href="#autenticacao">Obtenha o token de acesso</a> explica como usá-las sem expô-las.</p></details>
</div>
<h2>Dados e compartilhamento</h2><div class="faq-list">
<details><summary>Os dados são conferidos ou corrigidos pela API?</summary><p>Segundo o FAQ oficial, os dados correspondem ao que o contribuinte declarou à Receita Federal. A API não deve ser entendida como validação de renda. A página oficial também informa que o processamento da declaração, como a malha fina, não altera o conteúdo consultado. Leia <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/faq/" target="_blank" rel="noopener noreferrer">Dúvidas/FAQ oficial</a>.</p></details>
<details><summary>Posso consultar dados de cônjuge ou dependente?</summary><p>O FAQ oficial informa que a autorização é individual e que não é possível consultar dados de pessoas listadas como dependentes, cônjuge ou procurador por meio da declaração de outra pessoa. A consulta exige compartilhamento do próprio titular.</p></details>
<details><summary>O que é o token de compartilhamento?</summary><p>É o identificador da autorização criada pelo titular no serviço de compartilhamento. Ele é diferente do bearer token: o bearer autentica a aplicação; o token de compartilhamento identifica a autorização usada na consulta. Veja <a href="#conceitos">Tokens, certificado e responsabilidades</a>.</p></details>
<details><summary>Como o titular autoriza o acesso?</summary><p>O titular cria o compartilhamento no serviço da Receita Federal e escolhe a instituição destinatária. O passo a passo e os cuidados para orientar o titular estão em <a href="#autorizacao">Obtenha e localize a autorização</a>. As telas do serviço podem mudar; confira as instruções oficiais antes de orientar um cliente.</p></details>
<details><summary>É possível cancelar ou alterar uma autorização?</summary><p>O titular pode cancelar o compartilhamento no serviço em que o criou. Para mudar destinatário ou vigência, a orientação oficial é cancelar a autorização e criar outra com os parâmetros desejados. Consulte <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/como_compartilhar/" target="_blank" rel="noopener noreferrer">Como compartilhar</a>.</p></details>
<details><summary>O CNPJ alfanumérico é aceito?</summary><p>O FAQ oficial responde que o CNPJ alfanumérico não tem impacto. Porém, a referência técnica observada descreve o parâmetro como numérico. Essa diferença ainda precisa de confirmação técnica; veja <a href="#gestao">Validações antes da publicação</a> antes de implementar essa regra.</p></details>
</div>
<h2>Integração e operação</h2><div class="faq-list">
<details><summary>Posso testar antes de usar produção?</summary><p>Sim. A demonstração oficial usa dados de teste, não retorna dados reais e não gera cobrança. Os valores retornados também são criptografados. Comece por <a href="#primeira-consulta">Faça sua primeira consulta</a>.</p></details>
<details><summary>Por que os valores chegam criptografados?</summary><p>Para que apenas a instituição destinatária, com a chave privada correspondente à chave pública cadastrada, possa ler os valores. Não compartilhe a chave privada. Siga <a href="#descriptografia">Descriptografe os valores recebidos</a>.</p></details>
<details><summary>Quais chamadas são cobradas?</summary><p>A página <a href="#ambientes">Ambientes e cobrança</a> resume as regras publicadas para cada operação. Em caso de divergência, consulte as páginas de <a href="#erros">códigos de retorno</a> e confirme as condições do seu contrato antes de executar chamadas em produção.</p></details>
<details><summary>O que significa HTTP 404?</summary><p>Depende da operação: a documentação associa 404 em <code>/Autorizacoes</code> à ausência de compartilhamento e, em <code>/Consultar</code>, à ausência de declaração. Confira a operação e siga <a href="#erros">Resolva o problema pela etapa</a>.</p></details>
<details><summary>Recebi HTTP 200, mas não consigo ler os valores. O que verifico?</summary><p>HTTP 200 indica que a consulta foi concluída; os valores ainda podem estar criptografados. Confira se a chave privada corresponde ao certificado cadastrado e ao ambiente usado. Veja <a href="#descriptografia">Descriptografe os valores recebidos</a>.</p></details>
<details><summary>Onde peço ajuda?</summary><p>Registre ambiente, operação, horário e código HTTP, sem incluir credenciais, tokens completos ou chave privada. Use <a href="#suporte">Peça ajuda com o contexto certo</a> para escolher o canal e preparar o chamado.</p></details>
</div>
<h2>Links oficiais consultados</h2><p>Para conferir respostas comerciais e operacionais na fonte, consulte o <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/faq/" target="_blank" rel="noopener noreferrer">FAQ oficial</a>, <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/chamadas/demonstracao/" target="_blank" rel="noopener noreferrer">Demonstração</a> e <a href="https://apicenter.estaleiro.serpro.gov.br/documentacao/api-renda/pt/chamadas/api_reference/" target="_blank" rel="noopener noreferrer">Referência técnica</a>.</p>''' + note('Atenção às diferenças entre fontes','As dúvidas sobre CNPJ alfanumérico, códigos HTTP, chaves e cobrança dependem de informações técnicas e comerciais que precisam permanecer alinhadas. As divergências conhecidas estão listadas em <a href="#gestao">Validações antes da publicação</a>.','warning') + refs(('faq/','FAQ oficial'),('como_compartilhar/','Compartilhamento'),('chamadas/demonstracao/','Demonstração'),('chamadas/api_reference/','Referência da API')), 'Perguntas e respostas')

page('conceitos','Entenda o funcionamento','O que são os tokens e o certificado',
     'Saiba qual credencial autentica a aplicação e qual identifica a autorização do titular.',
'''<h2>As peças da integração</h2>''' + table(['Elemento','Para que serve','Onde você o usa'],[
('Consumer Key + Consumer Secret','Identificar a aplicação contratante ao pedir acesso.','Requisição ao serviço de autenticação.'),
('Token de acesso — bearer token','Permitir chamadas autenticadas à API.','Cabeçalho <code>Authorization: Bearer …</code>.'),
('Token de compartilhamento','Identificar o compartilhamento autorizado pelo titular.','Parâmetro de <code>/Consultar/{token}</code>.'),
('Chave pública do certificado','Proteger os valores destinados à instituição.','Cadastro associado ao destinatário.'),
('Chave privada correspondente','Descriptografar os valores recebidos.','Ambiente da instituição destinatária.')]) +
'''<h2>Quem faz o quê</h2><div class="flow-list"><div><b>Titular</b><p>Autoriza o compartilhamento no serviço da Receita Federal e pode cancelá-lo.</p></div><div><b>Compartilha Receita</b><p>Registra e gerencia a autorização e sua identificação.</p></div><div><b>Instituição contratante</b><p>Prepara a aplicação, localiza a autorização, consulta e lê os valores.</p></div><div><b>Consulta Renda / Serpro</b><p>Disponibiliza a consulta por API e entrega a resposta protegida.</p></div></div>
<h2>Por que são etapas separadas?</h2><p>O bearer token autentica a aplicação. O token de compartilhamento identifica a autorização do titular. Depois da consulta, a chave privada da instituição permite ler os valores. Ter acesso à API não substitui a autorização, e receber HTTP 200 não significa que os valores já estejam legíveis.</p>''' + refs(('quick_start/','Autenticação e consulta'),('como_compartilhar/','Compartilhamento'),('criptografia/','Criptografia')), 'Explicação')

page('primeira-consulta','Comece aqui','Faça sua primeira consulta',
     'Aprenda com a demonstração oficial e avance para produção quando os pré-requisitos estiverem concluídos.',
'''<h2>1. Explore a demonstração</h2><p>Abra a página oficial de demonstração. Ela disponibiliza dados de teste fixos e um bearer token próprio. Copie o token apresentado ali e utilize a opção <strong>Authorize</strong> da interface.</p><div class="actions">''' + link('chamadas/demonstracao/','Abrir demonstração oficial — sem cobrança') + '''</div>
<h2>O caminho completo, em quatro etapas</h2><div class="flow-list"><div><b>1. Obter acesso</b><p>A aplicação troca as credenciais por um bearer token.</p></div><div><b>2. Confirmar autorização</b><p>O titular compartilha os dados com sua instituição; sua aplicação localiza esse compartilhamento.</p></div><div><b>3. Consultar os dados</b><p>A aplicação usa o identificador do compartilhamento na operação de consulta.</p></div><div><b>4. Ler o retorno</b><p>Os valores protegidos são descriptografados e interpretados com os metadados correspondentes.</p></div></div>
<h2>2. Selecione um cenário</h2><p>Expanda <code>GET /Consultar/{token}</code>, use <strong>Try it out</strong> e informe um dos tokens públicos de demonstração abaixo.</p>''' + table(['Cenário','Token de compartilhamento de demonstração'],[
('Titular com declaração','<code class="wrap">dUMZ7AZvTnhFjhPZOJTMfm0pb2jLu9s2PzYfndPMc4tl</code>'),
('Titular sem declaração no exercício','<code class="wrap">ISoHYEiHK7P4zWXVO9yIpTGzo7J8aimo9ugwqRGoJYn4</code>')]) +
'''<p>Execute o cenário e observe o código HTTP. No cenário com declaração, examine a lista <code>dados</code>. O conteúdo de <code>valor</code> permanece criptografado.</p>
<h2>3. Leia os valores da demonstração</h2><p>Obtenha o certificado de teste no link indicado na página oficial de criptografia. Use sua chave privada com a resposta recebida, conforme o <a href="#descriptografia">guia de descriptografia</a>.</p>
<h2>4. Confira o que aprendeu</h2><ul><li>Você sabe distinguir o bearer token do token de compartilhamento.</li><li>Identificou o HTTP e a estrutura do retorno.</li><li>Entendeu que o valor deve ser descriptografado antes da interpretação.</li><li>Consegue explicar a diferença entre demonstração e produção.</li></ul>
<h2>5. Avance para uma consulta em produção</h2><ol><li>Conclua o <a href="#preparacao">checklist de preparação</a>.</li><li>Obtenha seu <a href="#autenticacao">token de acesso</a>.</li><li>Oriente o titular a autorizar e <a href="#autorizacao">localize o compartilhamento</a>.</li><li>Use a rota de <a href="#referencia">consulta</a> com o token recebido.</li><li>Confira o HTTP, descriptografe o retorno e interprete os campos pelo <a href="#dados">dicionário</a>.</li></ol>''' + note('Consulta em produção','O retorno 200 da operação de consulta é bilhetado segundo a página de códigos de retorno. Confira as condições comerciais antes de executar.') +
refs(('uso_via_documentacao/','Procedimento e tokens de teste'),('chamadas/demonstracao/','Demonstração'),('criptografia/','Certificado de demonstração'),('codigos_retorno_consultar/','Cobrança da consulta')), 'Tutorial')

page('simulacao','Comece aqui','Explore a jornada com dados fictícios',
     'Uma demonstração didática local para entender a ordem das etapas. Nenhuma chamada é feita ao Serpro.',
'''<div class="simulation"><div class="sim-controls"><label for="scenario">Cenário</label><select id="scenario"><option value="ok">Autorização disponível e declaração encontrada</option><option value="none">Autorização não encontrada</option><option value="noirpf">Autorização disponível, sem declaração</option></select><button id="sim-reset" class="button" type="button">Reiniciar</button></div><ol class="sim-steps"><li data-stage="1">1. Autenticar</li><li data-stage="2">2. Localizar autorização</li><li data-stage="3">3. Consultar</li><li data-stage="4">4. Ler os dados</li></ol><div class="sim-panel"><span class="badge">SIMULAÇÃO LOCAL</span><h2 id="sim-title">Comece pelo acesso à API</h2><p id="sim-text">A aplicação solicita um token de acesso com suas credenciais. Aqui usaremos apenas identificadores fictícios.</p><pre id="sim-output" aria-live="polite">Nenhuma etapa executada.</pre><button id="sim-next" class="button primary" type="button">Simular autenticação →</button></div></div>
<h2>O que este exemplo ensina</h2><p>A autenticação abre o acesso técnico. A autorização vincula o titular ao destinatário. A consulta retorna uma estrutura de dados. A descriptografia transforma os valores para leitura. O código exibido aqui é ilustrativo; os textos de status e o conteúdo fictício não representam um contrato de resposta da API.</p><p>Para aprender com a interface real e a massa pública de teste, siga <a href="#primeira-consulta">Faça sua primeira consulta</a>.</p>''', 'Tutorial interativo')

page('autenticacao','Integre passo a passo','Obtenha o token de acesso',
     'Use as credenciais da instituição para autenticar sua aplicação no gateway.',
'''<h2>Antes de começar</h2><p>Tenha a Consumer Key e a Consumer Secret do contrato ativo. Nos exemplos Bash, as variáveis devem ser fornecidas pelo ambiente da sua aplicação. Os nomes em maiúsculas são campos a preencher, não credenciais reais.</p>
<h2>Solicite o acesso</h2><p>Envie uma requisição POST ao serviço de token com autenticação Basic e <code>grant_type=client_credentials</code>. O cURL faz a codificação Basic ao receber <code>--user</code>.</p>''' + code(AUTH) +
'''<h2>Interprete o resultado</h2><p>Leia <code>access_token</code> e utilize-o nas chamadas seguintes. <code>expires_in</code> informa a duração em segundos: use o valor da resposta para controlar a renovação.</p>''' + code('''{
  "token_type": "Bearer",
  "expires_in": 3295,
  "access_token": "EXEMPLO_FICTICIO"
}''','JSON ilustrativo · campos selecionados') +
'''<h2>Use o token no cabeçalho</h2>''' + code('Authorization: Bearer SEU_ACCESS_TOKEN','HTTP') +
'''<p>Na expiração, solicite um novo acesso. Ao investigar um 401, identifique se a resposta veio do gateway ou da operação de negócio; veja <a href="#erros">Resolver erros</a>. Para erro 415 na autenticação, confira <code>Content-Type: application/x-www-form-urlencoded</code>.</p>''' + refs(('quick_start/','Autenticação oficial')))

page('autorizacao','Integre passo a passo','Obtenha e localize a autorização',
     'A autorização conecta o titular dos dados à sua instituição destinatária.',
'''<h2>O que o titular precisa fazer</h2><ol><li>Acessar o serviço de compartilhamento da Receita Federal.</li><li>Escolher os dados de renda de pessoa física.</li><li>Definir a vigência ou modalidade disponibilizada no serviço.</li><li>Selecionar sua instituição como destinatária e concluir a autorização.</li></ol><p>Oriente o titular a conferir o destinatário antes de autorizar. O guia oficial descreve acesso por gov.br prata ou ouro e por certificado. Consulte as instruções vigentes do portal no momento do uso.</p>
<h2>Como sua aplicação localiza o compartilhamento</h2><p>A referência oferece uma operação que consulta autorizações por contratante e titular. Execute-a com o bearer token da sua aplicação:</p>''' + code(AUTHORIZATIONS) +
table(['Parâmetro','Identificação'],[('<code>niContratante</code>','CNPJ da empresa contratante.'),('<code>niTitularDados</code>','CPF do titular dos dados.')]) +
'''<p>O retorno descrito na referência contém uma lista <code>autorizacoes</code>, com <code>token</code>, <code>status</code>, vigências, serviço e versão. Sua aplicação deve conferir a compatibilidade da autorização antes da consulta. Os valores possíveis de status precisam ser homologados com a equipe técnica; este modelo não inventa essa enumeração.</p>
<h2>Se a autorização não for encontrada</h2><p>Confira as identificações informadas e peça ao titular que verifique o destinatário e a conclusão do compartilhamento. A página de retornos associa 404 à ausência de autorização para os parâmetros enviados.</p>
<h2>Cancelamento e mudança</h2><p>O titular cancela no serviço de compartilhamento. Para alterar os parâmetros, a documentação orienta criar uma nova autorização após cancelar a anterior. Ajuste o atendimento e a aplicação para esse fluxo.</p>''' + refs(('como_compartilhar/','Orientação ao titular'),('chamadas/api_reference/','Operação de autorizações'),('codigos_retorno_autorizacoes/','Retornos de autorizações')))

page('notificacoes','Integre passo a passo','Receba avisos de novas autorizações',
     'A integração ativa notifica sua instituição quando um cidadão cria um compartilhamento com ela.',
'''<h2>Quando utilizar</h2><p>Esse recurso pode ajudar a iniciar o processamento a partir de um aviso de novo compartilhamento. A página oficial disponibiliza um manual próprio de configuração.</p><div class="actions">''' + link('integracao_ativa/','Abrir orientação oficial de integração ativa') + link('arquivo/ConsultaRenda-IntegracaoAtiva.pdf','Abrir manual de configuração em PDF') +
'''</div><h2>Como planejar a integração</h2><p>Antes de implementar o receptor, confira no manual os requisitos de cadastro e o contrato de notificação. A equipe deve obter respostas para estas perguntas:</p><ul><li>Como registrar o endereço que receberá os avisos?</li><li>Como identificar a origem de uma notificação?</li><li>Qual é o formato exato do conteúdo recebido?</li><li>Como confirmar o recebimento e tratar falhas?</li><li>Existe reenvio, ordenação garantida ou possibilidade de duplicidade?</li></ul>
<h2>Como isso se conecta à jornada</h2><p>Depois de receber o aviso, a instituição precisa relacioná-lo à autorização e seguir o fluxo de consulta documentado. A consulta por <code>/Autorizacoes/{niContratante}/{niTitularDados}</code> é descrita em <a href="#autorizacao">Localizar a autorização</a>.</p>''' + note('Detalhamento a homologar','O corpo do PDF não foi validado nesta revisão. O formato da notificação, o mecanismo de autenticação e a política de reenvio devem ser incorporados ao portal após revisão técnica.','warning') + refs(('integracao_ativa/','Integração ativa')), 'Guia prático')

page('descriptografia','Integre passo a passo','Descriptografe os valores recebidos',
     'A resposta pode chegar corretamente e ainda conter valores criptografados.',
'''<h2>O que é protegido</h2><p>A estrutura JSON identifica os campos. Os valores em <code>dados[].valor</code> usam RSA com a chave pública do destinatário. A documentação indica a configuração <code>RSA/ECB/PKCS1Padding</code>. A leitura exige a chave privada correspondente.</p>
<h2>Prepare a entrada</h2><ol><li>Confirme o HTTP 200 da consulta e salve a resposta em <code>resposta.json</code>.</li><li>Na demonstração, use o certificado disponibilizado para teste. Em produção, use o material correspondente à chave pública cadastrada.</li><li>Confira com a equipe como a aplicação acessará a chave privada.</li></ol>
<h2>Exemplo proposto em Python</h2><p>O exemplo abaixo usa um arquivo PKCS#12 (<code>.p12</code> ou <code>.pfx</code>) e o pacote <code>cryptography</code>. Pressupõe uma chave exportável, disponível conforme as regras da instituição. Certificados em dispositivos ou HSM exigem adaptação ao provedor de chaves.</p>''' + code('python -m pip install cryptography','Preparação do ambiente Python') + code(DECRYPT,'Python · exemplo a homologar com a API') +
'''<h2>Resultado esperado</h2><p>O programa mantém em memória uma lista com código, descrição e valor legível, e informa quantos campos foram processados. A interpretação comercial deve considerar o dicionário e o ano-calendário.</p>''' + note('Validação do exemplo','Este código foi elaborado para o modelo e não foi executado contra o Serpro. O tratamento Base64 → RSA PKCS#1 v1.5 → UTF-8 deve ser homologado com respostas de demonstração. A sequência foi verificada somente com um caso sintético local.','warning') +
'''<h2>Se a leitura falhar</h2><p>Confira se o retorno pertence ao mesmo ambiente e certificado utilizados. Verifique senha, acesso à chave, formato do conteúdo e configuração criptográfica. Não trate uma falha de descriptografia como valor zero.</p>''' + refs(('criptografia/','Criptografia e certificado de teste'),('https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/','Biblioteca cryptography: RSA'),('https://docs.python.org/3/library/base64.html','Python: Base64')))

page('ambientes','Referência e operação','Ambientes e cobrança',
     'Escolha o ambiente de acordo com a etapa da sua integração.',
table(['','Demonstração','Produção'],[
('Objetivo','Aprender com cenários fixos.','Consultar dados compartilhados com sua instituição.'),
('Origem dos dados','Massa de teste.','Dados autorizados do titular.'),
('Autenticação','Bearer token disponibilizado na página de demonstração.','Bearer token obtido com as credenciais do contrato.'),
('Chave para leitura','Material de teste indicado na documentação.','Chave privada do destinatário correspondente ao cadastro.'),
('Cobrança','Gratuita, segundo a página oficial.','Conforme operação, retorno e condições comerciais.')]) +
'''<h2>Endereços publicados</h2>''' + code('https://gateway.apiserpro.serpro.gov.br/renda-pf-trial/v1','Base da demonstração') + code('https://gateway.apiserpro.serpro.gov.br/renda-pf/v1','Base de produção') +
'''<h2>Regras de bilhetagem descritas</h2>''' + table(['Operação','Regra publicada'],[
('Consultar','A página de retornos afirma que apenas HTTP 200 é bilhetado.'),
('Autorizacoes','A página de retornos informa que nenhum código é bilhetado.'),
('status','A página de retornos informa que nenhum código é bilhetado.')]) +
'''<p>Bilhetagem é o registro de consumo usado na cobrança. Para preços, faixas e demais condições, consulte a proposta comercial ou a Loja Serpro.</p>
<h2>Disponibilidade e limites</h2><p>Use <code>GET /status</code> para consultar a disponibilidade descrita na referência. Limites de requisição, tempo máximo de resposta e compromissos de disponibilidade não foram confirmados nas fontes desta revisão. Alinhe-os com o contrato e o suporte antes de dimensionar a operação.</p>''' + refs(('chamadas/demonstracao/','Demonstração'),('chamadas/api_reference/','Produção'),('codigos_retorno_consultar/','Bilhetagem da consulta'),('codigos_retorno_autorizacoes/','Bilhetagem de autorizações'),('codigos_retorno_status/','Bilhetagem do status')))

page('referencia','Referência e operação','Referência das operações',
     'Rotas observadas na referência interativa de produção em 19/10/2026. Preserve letras maiúsculas e minúsculas.',
'''<p class="muted">Base de produção: <code class="wrap">https://gateway.apiserpro.serpro.gov.br/renda-pf/v1</code></p>
<h2>Consultar renda</h2><div class="endpoint"><span>GET</span><code>/Consultar/{token}</code></div><p>Informe o token de compartilhamento no caminho e o bearer token no cabeçalho. A consulta bem-sucedida retorna a autorização, a identificação do serviço e uma lista de dados.</p>''' + code(QUERY) +
'''<p>O comando grava o corpo em <code>resposta.json</code> e mostra o HTTP. Em caso de erro, o arquivo conterá a resposta de erro; use a <a href="#erros">orientação correspondente</a> antes de tentar descriptografar.</p>
<h2>Listar autorizações do titular</h2><div class="endpoint"><span>GET</span><code>/Autorizacoes/{niContratante}/{niTitularDados}</code></div><p>Informe o CNPJ contratante e o CPF titular. A referência os descreve como identificadores de 14 e 11 dígitos. Preserve zeros iniciais na representação dos identificadores; a tipagem e a compatibilidade alfanumérica estão na lista de validação editorial.</p>''' + code(AUTHORIZATIONS) +
'''<h2>Consultar disponibilidade</h2><div class="endpoint"><span>GET</span><code>/status</code></div><p>A referência associa HTTP 200 à disponibilidade. Respostas diferentes exigem investigação; o corpo completo não foi especificado neste modelo.</p>''' + code(STATUS) +
'''<h2>Contrato técnico completo</h2><p>A publicação definitiva deve gerar parâmetros, tipos, obrigatoriedade e respostas a partir do arquivo OpenAPI homologado. Esta página resume as operações observadas; use a referência oficial para consultar os esquemas completos.</p>''' + note('Divergências de documentação','A página de retornos usa um parâmetro adicional em /Consultar e a grafia /Status. Os exemplos deste modelo seguem o Swagger renderizado. A conciliação das fontes está registrada em <a href="#gestao">Para a gestão</a>.','warning') + refs(('chamadas/api_reference/','Swagger de produção'),('quick_start/','Exemplo de autenticação e consulta')), 'Referência técnica')

page('dados','Referência e operação','Entenda os dados retornados',
     'Leia a identificação do retorno e depois interprete os valores pelo código de cada campo.',
'''<h2>Como a resposta é organizada</h2><p>A resposta de consulta reúne <code>autorizacao</code>, identificação do serviço, <code>versao</code> e a lista <code>dados</code>. Cada item de dados tem <code>codigo</code>, <code>texto</code> e <code>valor</code>.</p>''' + code('''{
  "autorizacao": {
    "token": "TOKEN_FICTICIO",
    "dataHoraRegistro": "DATA_DO_REGISTRO",
    "titular": "IDENTIFICACAO_DO_TITULAR",
    "destinatario": "IDENTIFICACAO_DO_DESTINATARIO",
    "avisoLegal": "TEXTO_DO_AVISO"
  },
  "servico": "APIConsultaRenda",
  "idServico": "9000",
  "versao": "VERSAO_RETORNADA",
  "dados": [
    { "codigo": "1", "texto": "Rendimentos Recebidos de Pessoas Jurídicas",
      "valor": "CONTEUDO_CRIPTOGRAFADO_EM_BASE64" }
  ]
}''','JSON didático · apenas um item de dados') +
'''<h2>Campos do conjunto documentado</h2>''' + table(['Código','Informação'],[
('1','Rendimentos de pessoas jurídicas'),('2','Rendimentos tributáveis'),('3','Patrimônio total'),('4','Rendimentos isentos e não tributáveis'),('5','Receita de atividade rural'),('6','Aluguéis recebidos de pessoas físicas'),('7','Ano-calendário'),('8','Código da natureza da ocupação'),('9','Descrição da natureza da ocupação'),('10','Código da ocupação principal'),('11','Descrição da ocupação principal')]) +
'''<h2>Recomendações de interpretação</h2><ul><li>Associe cada valor ao seu código e ao conjunto de metadados aplicável.</li><li>Confira o ano-calendário antes de exibir um valor como atual.</li><li>Mantenha distinção entre informação ausente, falha de leitura e valor zero.</li><li>Evite depender apenas da posição de um elemento na lista.</li></ul>''' + note('Dicionário a completar antes da publicação','Precisão decimal, unidade, formato após descriptografia, nulabilidade e regras para campos ausentes devem ser explicitados no contrato homologado. Este modelo não assume essas regras.','warning') + refs(('versionamento_metadados_v1/','Conjunto de campos publicado'),('chamadas/api_reference/','Esquemas'),('faq/','Natureza declaratória dos dados')), 'Referência técnica')

page('erros','Referência e operação','Resolva o problema pela etapa',
     'Identifique a operação, o código HTTP e a mensagem antes de escolher a próxima ação.',
'''<div class="diagnostic"><label for="problem">Em qual situação você está?</label><select id="problem"><option value="401">HTTP 401 — acesso ou autorização</option><option value="403">HTTP 403 — acesso recusado</option><option value="404a">HTTP 404 — autorizações</option><option value="404c">HTTP 404 — consulta</option><option value="415">HTTP 415 — autenticação</option><option value="500">HTTP 500 — falha interna</option><option value="503">HTTP 503 — consulta indisponível</option><option value="crypto">HTTP 200, mas não consigo ler os valores</option></select><div id="diagnosis" role="status"></div></div>
<h2>Mapa de respostas de consulta</h2>''' + table(['HTTP','Leitura documentada','Próxima ação sugerida'],[
('200','Consulta realizada.','Descriptografar e interpretar os campos.'),
('400','Requisição inválida.','Conferir caminho e parâmetros.'),
('401','Incompatibilidade de autorização; no gateway também pode haver expiração do acesso.','Localizar a camada da falha e conferir o token correto.'),
('403','Acesso recusado.','Conferir vínculo contratante/destinatário e cadastro das chaves.'),
('404','Sem declaração no exercício indicado pela documentação.','Tratar a ausência de informação e orientar o processo de negócio.'),
('500','Falha interna.','Registrar contexto, avaliar disponibilidade e acionar suporte se persistir.'),
('503','Descrições divergem entre as fontes.','Conferir mensagem e acionar suporte se persistir.')]) +
'''<h2>O mesmo código pode ter outro significado</h2><p>Em <code>Autorizacoes</code>, o 404 é associado à ausência de autorização pela página de retornos. Em <code>Consultar</code>, é associado à ausência de declaração. Identifique a operação ao relatar o problema.</p>
<h2>Antes de repetir a chamada</h2><p>Corrija erros de entrada e acesso antes de repetir. Em falhas transitórias, a equipe deve definir espera e limite de tentativas. Uma repetição de consulta pode gerar novo consumo se resultar em sucesso; trate a política de repetição junto com as regras comerciais.</p>
<h2>Quando pedir ajuda</h2><p>Registre horário com fuso, ambiente, operação, HTTP e mensagem, com dados sensíveis removidos. Use <a href="#suporte">o roteiro de suporte</a> para encaminhar evidências.</p>''' + refs(('codigos_retorno_consultar/','Retornos de consulta'),('codigos_retorno_autorizacoes/','Retornos de autorizações'),('quick_start/','401 e 415 de autenticação'),('chamadas/api_reference/','Referência interativa')))

page('suporte','Referência e operação','Peça ajuda com o contexto certo',
     'Informe onde o fluxo parou para facilitar o diagnóstico.',
'''<h2>Escolha o canal</h2><div class="card-grid two"><div class="card"><h3>Integração ou indisponibilidade</h3><p>Abra um acionamento pelo canal indicado na página oficial. Tenha o CNPJ do contrato em mãos.</p>''' + link('suporte/','Abrir orientação de suporte Consulta Renda') + '''</div><div class="card"><h3>Contrato, cobrança e consumo</h3><p>A Área do Cliente reúne recursos relacionados ao contrato, boletos, relatórios de consumo e chaves.</p>''' + link('https://cliente.serpro.gov.br/','Acessar Área do Cliente') + '''</div></div>
<h2>Modelo de descrição do chamado</h2><p>Copie e complete com informações necessárias ao diagnóstico. Compartilhe dados de identificação somente no canal oficial apropriado.</p>''' + code('''Produto: Consulta Renda
Ambiente: demonstração ou produção
Operação: Consultar / Autorizacoes / status / autenticação
Data e hora com fuso:
Código HTTP e mensagem (sem dados pessoais):
O que eu esperava:
O que aconteceu:
Passos para reproduzir (com valores mascarados):
Frequência e impacto:
Verificações já realizadas:
Identificador de correlação, se retornado:
''','Texto para copiar') +
'''<p>Não inclua Consumer Secret, bearer token, token completo de compartilhamento, chave privada ou senha do certificado nos registros de diagnóstico compartilhados.</p>
<h2>Quando houver indisponibilidade</h2><p>Identifique o horário, a operação afetada e o resultado da consulta de status. A documentação diferencia o fluxo de indisponibilidade do suporte regular de produto.</p>''' + refs(('suporte/','Canais de suporte'),('codigos_retorno_status/','Indisponibilidade')))

page('versoes','Referência e operação','Entenda versões e mudanças',
     'Acompanhe o contrato da API e o conjunto de informações associado à autorização.',
'''<h2>Versão da API e versão de metadados</h2><p>A rota de produção observada utiliza <code>/v1</code>. O conjunto de dados autorizado também tem controle de versão. Não deduza automaticamente a versão dos metadados apenas pelo caminho da API.</p><p>A documentação explica que o compartilhamento mantém vínculo com o conjunto de metadados vigente quando foi registrado. Para compartilhar o conjunto mais atual, pode ser necessário emitir uma nova autorização, conforme a orientação oficial.</p>
<h2>Como acompanhar uma mudança</h2><ol><li>Identifique o anúncio oficial e as versões envolvidas.</li><li>Compare rotas, campos, tipos, autorizações e erros.</li><li>Execute os cenários de teste indicados no guia de migração.</li><li>Confirme compatibilidade e cronograma antes de alterar produção.</li></ol>
<h2>Situação da V2 nesta proposta</h2><p>O manual gerencial local menciona uma evolução planejada. A referência pública consultada nesta revisão apresenta a API v1. O modelo mantém a V2 como pauta de gestão, dependente de contrato técnico e cronograma confirmados.</p>
<h2>Histórico desta proposta editorial</h2>''' + table(['Data','Mudança','Efeito'],[('19/10/2026','Primeira edição do modelo de documentação.','Introduz jornada, explicações, exemplos e lista de validações. Nenhuma mudança na API é declarada.')]) + refs(('versionamento_metadados/','Versionamento de metadados'),('chamadas/api_reference/','Referência pública observada')), 'Explicação')

page('padrao','Para a gestão','O padrão proposto para a documentação',
     'Uma arquitetura editorial baseada em referências reconhecidas e adaptada à jornada da Consulta Renda.',
'''<h2>Existe um padrão de mercado?</h2><p>Há uma especificação consolidada para descrever APIs HTTP, a <strong>OpenAPI</strong>, e abordagens reconhecidas para organizar e redigir a documentação. Para este produto, a recomendação é combinar essas práticas. Elas cobrem problemas diferentes e não exigem mudar o comportamento da API.</p>''' + table(['Referência','O que oferece','Aplicação neste modelo'],[
('Diátaxis','Quatro formas de conteúdo: tutorial, guia prático, explicação e referência.','Páginas rotuladas pela necessidade do leitor e relacionadas entre si.'),
('OpenAPI','Descrição estruturada de operações, parâmetros, esquemas e respostas.','Referência técnica ligada ao contrato homologado; geração automática na publicação definitiva.'),
('Google developer documentation style guide','Diretrizes de escrita clara, voz ativa e instruções organizadas.','Objetivo primeiro, pré-requisitos explícitos, ações em sequência e links descritivos.'),
('Stripe Docs — Get started','Exemplo de portal com caminhos de início e tarefas de integração.','Entradas por intenção: entender, começar e resolver.')]) +
'''<h2>Arquitetura aplicada à Consulta Renda</h2>''' + table(['Necessidade do leitor','Conteúdo oferecido'],[
('“Quero saber se atende meu caso.”','Produto, dados disponíveis, requisitos e condições comerciais por link oficial.'),
('“Quero fazer funcionar pela primeira vez.”','Demonstração guiada, checklist e sequência até leitura do retorno.'),
('“Preciso realizar uma tarefa específica.”','Autenticação, autorização, notificações, descriptografia e suporte.'),
('“Preciso conferir o contrato.”','Rotas, parâmetros, dados, códigos e versionamento.'),
('“Preciso entender por que funciona assim.”','Papéis, dois tokens, certificado, autorização e metadados.')]) +
'''<h2>Estrutura de um guia de tarefa</h2><ol><li><strong>Objetivo:</strong> qual resultado o leitor vai obter.</li><li><strong>Pré-requisitos:</strong> o que precisa estar pronto.</li><li><strong>Responsável:</strong> quem executa cada etapa.</li><li><strong>Procedimento:</strong> ações e parâmetros em ordem.</li><li><strong>Confirmação:</strong> como reconhecer que funcionou.</li><li><strong>Falha:</strong> o que verificar e como pedir ajuda.</li><li><strong>Continuação:</strong> qual tarefa vem depois.</li><li><strong>Fonte:</strong> versão e responsável pela revisão.</li></ol>
<h2>Comece pela tarefa do cliente</h2><p>O menu separa quem está avaliando o produto, integrando a API ou resolvendo um erro. Os guias explicam cada etapa antes de apresentar a operação técnica. A referência continua disponível para consulta de rotas e parâmetros.</p><h2>Diferença em relação à organização atual</h2><p>A proposta reúne a sequência entre contrato, autenticação, autorização, consulta e leitura dos dados. Hoje, o cliente precisa percorrer páginas diferentes para montar esse fluxo.</p>''' + refs(('https://diataxis.fr/','Diátaxis'),('https://spec.openapis.org/oas/latest.html','OpenAPI'),('https://developers.google.com/style/highlights','Google: redação técnica'),('https://docs.stripe.com/get-started','Stripe: início da integração')), 'Proposta editorial')

page('gestao','Para a gestão','Validações antes da publicação oficial',
     'Pendências concretas identificadas nas fontes e um roteiro para transformar o modelo em documentação mantida pelo produto.',
'''<h2>Correções e decisões prioritárias</h2>''' + table(['Prioridade','Evidência / lacuna','Ação necessária'],[
('Alta','<a href="'+BASE+'como_compartilhar/" target="_blank" rel="noopener">Compartilhamento</a> cita Consulta Faturamento e dados de empresas.','Revisar textos, regras, exemplos e imagens para pessoa física.'),
('Alta','Retornos indicam <code>/Consultar/{token}/{niContratante}</code>; Swagger e autenticação usam <code>/Consultar/{token}</code>.','Confirmar rota homologada e unificar todas as fontes. O modelo adota o Swagger observado.'),
('Alta','Página de retornos usa <code>/Status</code>; Swagger usa <code>/status</code>.','Confirmar grafia e corrigir links/exemplos. O gateway distingue maiúsculas.'),
('Alta','Metadados descrevem acolhimento na assinatura; criptografia descreve consulta/geração das credenciais.','Documentar evento real, certificados aceitos, renovação e efeito sobre dados já cifrados.'),
('Alta','503 tem descrições diferentes; 404 aparece como sucesso em uma tabela e erro no Swagger.','Definir semântica, mensagem, ação do cliente e bilhetagem por operação.'),
('Alta','Descrição de dados menciona último mês, CNPJ e representação legal em página de renda PF.','Confirmar referência temporal e significado dos identificadores. Revisar o dicionário.'),
('Alta','Referência descreve CNPJ numérico; FAQ afirma ausência de impacto do CNPJ alfanumérico.','Homologar parâmetros, formatos e compatibilidade; corrigir tipagem e exemplos.'),
('Média','Exemplo de descriptografia novo e política de certificado não homologados.','Validar com a massa pública, certificados suportados e aplicação de referência.'),
('Média','Configuração da integração ativa está em PDF; conteúdo do PDF não foi validado aqui.','Incorporar payload, autenticação, resposta esperada, duplicidade e reenvio após revisão.'),
('Média','Valores de status, limites, SLA e formatos após descriptografia não consolidados nesta revisão.','Definir fonte responsável e explicitar os dados faltantes.'),
('Média','V2 é citada como planejamento no manual local.','Publicar migração somente com contrato técnico, compatibilidade e datas aprovados.')]) +
'''<h2>Responsabilidade editorial sugerida</h2>''' + table(['Papel','Responsabilidade'],[
('Gestão do produto','Jornada, escopo, regras comerciais e aprovação da mensagem ao cliente.'),
('Equipe técnica','Contrato OpenAPI, comportamento, exemplos e cenários homologados.'),
('Suporte / relacionamento','Dúvidas frequentes, diagnóstico e validação dos canais.'),
('Responsável pela documentação','Navegação, redação, links, revisão e histórico de mudanças.')]) +
'''<h2>Critérios de aceite</h2><ul><li>Um desenvolvedor sem experiência no produto conclui o tutorial usando apenas os materiais publicados.</li><li>Cada tarefa identifica pré-requisitos, resultado esperado e próximo passo.</li><li>Rotas e respostas coincidem com o OpenAPI homologado.</li><li>Demonstração e produção têm identificação e cobrança explícitas.</li><li>Os exemplos funcionam com a massa oficial de teste.</li><li>As pendências acima têm decisão, responsável e fonte.</li><li>A equipe revisa a documentação junto com cada mudança do produto.</li></ul>
<h2>Critério de revisão orientada ao cliente</h2><p>Em cada página, pergunte: “Uma pessoa que contratou o produto, mas ainda não conhece seus conceitos, consegue entender o objetivo, saber quem precisa agir, seguir os passos, reconhecer o resultado e descobrir o que fazer se falhar?” Se a resposta for não, a página ainda depende do conhecimento prévio que a revisão pretende remover.</p><p>A jornada principal deve ser validada com ao menos um cliente ou desenvolvedor que não participou da construção da API. Observe onde ele hesita, quais termos exige explicar e em que ponto precisa pedir ajuda. Use esses achados para priorizar correções editoriais.</p>
<h2>Como medir se melhorou</h2><p>Meça tempo até a primeira consulta legível, conclusão do tutorial sem ajuda, chamados por etapa e motivos de abandono da integração. Registre uma linha de base antes da mudança. As metas devem ser acordadas após essa medição.</p>
<h2>Escopo da revisão</h2><p>Foram lidas as páginas de introdução, contratação, autenticação, compartilhamento, criptografia, uso via documentação, demonstração, referência interativa, códigos de retorno, metadados, FAQ, integração ativa e suporte. Nenhuma consulta autenticada foi executada. A análise documental não confirma o comportamento real de produção.</p>''' + refs(('codigos_retorno_consultar/','Divergências de consulta'),('codigos_retorno_status/','Grafia de status'),('versionamento_metadados_v1/','Metadados'),('criptografia/','Acolhimento'),('faq/','FAQ'),('chamadas/api_reference/','Swagger')), 'Revisão interna')

page('agentes','Para agentes','Configurar Codex e Claude Code',
     'Prepare instruções e um prompt de trabalho para integrar a API em uma aplicação cliente.',
'''<h2>O que estes arquivos fazem</h2><p><code>AGENTS.md</code> e <code>CLAUDE.md</code> oferecem contexto de projeto aos agentes que ajudam a escrever código. O prompt propõe uma tarefa reutilizável. São modelos para copiar para a raiz do <strong>repositório da aplicação que vai integrar a API</strong>; não instalam ferramentas, não criam credenciais e não fazem uma integração automática neste manual.</p>
<h2>Três arquivos, três usos</h2>''' + table(['Arquivo','Como o agente o usa','Destino'],[
('<a href="apoio/modelos-agentes/AGENTS.md" target="_blank">Abrir modelo AGENTS.md ↗</a>','Codex carrega instruções de projeto. Claude Code também reconhece AGENTS.md em versões e configurações compatíveis.','Copie para a raiz da aplicação.'),
('<a href="apoio/modelos-agentes/CLAUDE.md" target="_blank">Abrir modelo CLAUDE.md ↗</a>','Claude Code carrega este arquivo. A primeira linha importa as instruções compartilhadas de AGENTS.md.','Copie ao lado do AGENTS.md na raiz da aplicação.'),
('<a href="apoio/modelos-agentes/PROMPT_integracao_consulta_renda.md" target="_blank">Abrir prompt reutilizável ↗</a>','O desenvolvedor inicia uma tarefa no chat do agente, completa os campos entre colchetes e fornece o texto.','Mantenha junto da integração ou copie para o repositório.')]) +
'''<h2>Como preparar o repositório</h2><ol><li>Abra a pasta da aplicação cliente, em que o código será integrado.</li><li>Copie <code>AGENTS.md</code> e <code>CLAUDE.md</code> para essa raiz. Revise as instruções para respeitar ferramentas, convenções e controles próprios da equipe.</li><li>Abra <code>PROMPT_integracao_consulta_renda.md</code>, preencha objetivo, componente, linguagem e escopo, e use-o para iniciar a tarefa no agente.</li><li>Confirme que o agente leu os arquivos de instrução e peça que ele relate divergências do contrato antes de depender delas.</li><li>Revise as alterações e os resultados dos testes antes de incorporar o código à aplicação.</li></ol>
<h2>Como começar uma tarefa</h2><p>O prompt reutilizável inclui este roteiro, com mais contexto nos arquivos acima:</p>''' + code('''Leia AGENTS.md e as instruções aplicáveis. Consulte a documentação oficial e o OpenAPI vigente. Antes de codificar, explique o fluxo e liste divergências entre a referência e as páginas de apoio. Não invente detalhes: sinalize o que depende de decisão técnica. Implemente somente o escopo informado, sem produção ou dados reais. Verifique localmente com dados sintéticos e relate alterações, verificações e pendências.''','Prompt inicial · trecho') +
'''<h2>O que o agente precisa confirmar</h2><ul><li>Como o repositório lida com configurações e credenciais, sem expô-las.</li><li>Qual contrato oficial governa a integração atual, em especial as divergências da seção <a href="#gestao">Validações antes da publicação</a>.</li><li>Como separar autenticação, autorização do titular, consulta, descriptografia e tratamento de erros.</li><li>Como provar o comportamento sem usar chaves, tokens, dados pessoais ou chamadas reais.</li></ul>
<h2>Verifique o carregamento das instruções</h2><p>No Codex, confirme que o <code>AGENTS.md</code> aparece no contexto do repositório. No Claude Code, como este pacote inclui os dois arquivos, confirme que o <code>CLAUDE.md</code> importou o <code>AGENTS.md</code>, por exemplo na memória ou no contexto da sessão. O carregamento depende da versão e das configurações da ferramenta.</p>''' + note('Limite importante','Esses arquivos orientam o agente; o texto não é um bloqueio técnico. Mantenha os controles reais de acesso, segredos e aprovação no ambiente e nas ferramentas da equipe.') +
'''<h2>Fontes oficiais sobre os arquivos de instrução</h2><ul><li><a href="https://learn.chatgpt.com/docs/agent-configuration/agents-md" target="_blank" rel="noopener noreferrer">Codex: instruções de projeto com AGENTS.md ↗</a></li><li><a href="https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools" target="_blank" rel="noopener noreferrer">Claude Code: compartilhar AGENTS.md com import em CLAUDE.md ↗</a></li></ul>''', 'Guia para agentes')

page('fontes','Para a gestão','Fontes e manutenção da documentação',
     'Referências consultadas em 19 de outubro de 2026 e instruções para manter a proposta.',
'''<h2>Fontes de produto</h2><p>A documentação oficial é a fonte das rotas, fluxos e comportamentos descritos. Quando houve divergência, ela foi registrada na área de gestão. O manual gerencial local serviu como contexto; seus planos futuros não foram tratados como funcionalidades publicadas.</p><div class="source-list">''' + ''.join('<p>'+link(p,t)+'</p>' for p,t in [
('','Introdução'),('como_contratar/','Contratação'),('quick_start/','Autenticação'),('uso_via_documentacao/','Uso via documentação'),('chamadas/demonstracao/','Demonstração e servidor trial'),('chamadas/api_reference/','Referência Swagger de produção'),('como_compartilhar/','Compartilhamento'),('criptografia/','Criptografia'),('integracao_ativa/','Integração ativa'),('codigos_retorno_consultar/','Retornos: consulta'),('codigos_retorno_autorizacoes/','Retornos: autorizações'),('codigos_retorno_status/','Retornos: status'),('versionamento_metadados/','Versionamento'),('versionamento_metadados_v1/','Campos publicados'),('faq/','FAQ'),('suporte/','Suporte')]) + '''</div>
<h2>Referências de documentação</h2>''' + refs(('https://diataxis.fr/','Diátaxis'),('https://spec.openapis.org/oas/latest.html','OpenAPI'),('https://developers.google.com/style/highlights','Google style guide'),('https://docs.stripe.com/get-started','Stripe Docs')) +
'''<h2>Como utilizar o arquivo</h2><p>Abra o HTML em um navegador. A navegação, a busca e a simulação funcionam localmente. Os links de fontes abrem os sites originais e precisam de conexão. O botão de impressão inclui todas as páginas da proposta.</p><p>Os campos de busca e marcações do checklist servem somente à navegação. Este arquivo não recebe credenciais e não realiza consultas à API. O checklist usa armazenamento local quando disponível.</p>
<h2>Antes de publicar</h2><p>Confirme as pendências com as áreas responsáveis, valide os exemplos e aprove o contrato técnico. Depois, publique no ambiente oficial. Registre a versão das fontes e a data da próxima revisão.</p>''', 'Proveniência')

# Organização da jornada da entrega inicial; pendências ficam no material interno.
import re
by_id = {p['id']: p for p in PAGES}
for ident in ('preparacao', 'conceitos', 'autenticacao', 'autorizacao', 'notificacoes', 'primeira-consulta', 'simulacao', 'descriptografia'):
    by_id[ident]['group'] = 'Funcionamento e integração'
by_id['conceitos']['title'] = 'Glossário da integração'
by_id['notificacoes']['title'] = 'Integrações ativa e passiva'
by_id['notificacoes']['lead'] = 'Conheça os caminhos para identificar uma autorização e continuar a consulta.'
by_id['notificacoes']['body'] = ('<h2>Antes de começar</h2><p>Prepare as credenciais e a chave pública da instituição e oriente o titular a autorizar o compartilhamento. Veja <a href="#preparacao">Prepare a integração</a> e <a href="#autorizacao">Obtenha e localize a autorização</a>.</p>'
    '<h2>Integração ativa</h2><p>A instituição pode receber um aviso de novo compartilhamento e associá-lo à autorização para seguir com a consulta. Consulte a orientação oficial antes de implementar o receptor.</p>' + link('integracao_ativa/', 'Orientação oficial de integração ativa') + link('arquivo/ConsultaRenda-IntegracaoAtiva.pdf', 'Manual de integração ativa em PDF') +
    '<h2>Integração passiva</h2><p>A instituição identifica a autorização consultando a operação de autorizações por contratante e titular. Confira o <a href="#autorizacao">guia de localização</a> e use o token do compartilhamento para consultar os dados.</p>'
    '<h2>Depois de identificar a autorização</h2><p>Consulte os dados conforme a <a href="#referencia">referência das operações</a> e siga o <a href="#descriptografia">guia de leitura dos valores</a>.</p>')
by_id['preparacao']['body'] = by_id['preparacao']['body'].replace('O cadastro da chave pública é chamado de <strong>acolhimento</strong> na documentação. A página de criptografia o associa à consulta ou geração das credenciais. A área de gestão registra uma descrição divergente em metadados.', 'O cadastro da chave pública é chamado de <strong>acolhimento</strong>. Consulte a orientação oficial de criptografia para realizar esse preparo antes da consulta.')
by_id['conceitos']['body'] = by_id['conceitos']['body'].replace('Proteger os valores destinados à instituição.', 'Criptografar as informações compartilhadas para a instituição.').replace('Descriptografar os valores recebidos.', 'Descriptografar as informações recebidas com a chave privada correspondente.')
by_id['duvidas']['body'] = by_id['duvidas']['body'].replace('<h2>Integração e operação</h2><div class="faq-list">', '<h2>Integração e operação</h2><div class="faq-list"><details><summary>Qual a diferença entre tokens e certificado?</summary><p>O bearer token autentica a aplicação; o token de compartilhamento identifica a autorização do titular. A chave pública protege as informações compartilhadas, e a chave privada correspondente permite que a instituição as leia. Consulte o <a href="#conceitos">glossário da integração</a>.</p></details>')
by_id['autorizacao']['body'] = by_id['autorizacao']['body'].replace('<h2>Como sua aplicação localiza o compartilhamento</h2>', '<h2>Como a instituição identifica a autorização</h2><p>Na integração ativa, a instituição pode receber um aviso; na passiva, consulta as autorizações. Veja <a href="#notificacoes">integrações ativa e passiva</a>.</p><h2>Como sua aplicação localiza o compartilhamento</h2>')
by_id['dados']['group'] = 'Metadados'
by_id['dados']['title'] = 'Metadados da versão 1.0'
by_id['dados']['lead'] = 'Consulte os campos da versão 1.0 documentada na referência pública.'
by_id['dados']['body'] = '<p>Esta página explica a estrutura de uma resposta ilustrativa e apresenta o conjunto de metadados V1. Para a comparação entre as versões e os novos grupos previstos, consulte <a href="#dados-v2">metadados previstos para V2</a>; para diferenciar os controles de versão, veja <a href="#versoes">versões e mudanças</a>.</p>' + by_id['dados']['body']

by_id['dados']['body'] = by_id['dados']['body'].replace('<h2>Campos do conjunto documentado</h2>', '<h2>Campos do conjunto de metadados V1</h2>')
by_id['versoes']['group'] = 'Metadados'
by_id['versoes']['body'] = by_id['versoes']['body'].replace('<h2>Situação da V2 nesta proposta</h2><p>O manual gerencial local menciona uma evolução planejada. A referência pública consultada nesta revisão apresenta a API v1. O modelo mantém a V2 como pauta de gestão, dependente de contrato técnico e cronograma confirmados.</p>', '<h2>Atualização V2 do produto</h2><p>Esta documentação acompanha a atualização V2 do Consulta Renda. O funcionamento geral permanece, com alterações no payload e na saída. A versão do produto, a rota da API e a versão dos metadados são identificações distintas.</p>')
by_id['versoes']['body'] = re.sub(r'<h2>Histórico desta proposta editorial</h2>.*?(?=<div class="sources">)', '', by_id['versoes']['body'], flags=re.S)
# Lista transcrita do documento "Consulta Renda - Lista de campos na V1 e V2", revisão de 20/10/2026.
METADADOS_V2_PREVISTOS = [('Informações gerais',
  [('Ano de exercício', 'Não', 'Sim', 'Novo na V2'),
   ('Ano-calendário', 'Sim', 'Sim', 'Mantido'),
   ('Data/Hora da entrega', 'Não', 'Sim', 'Novo na V2'),
   ('Tipo da declaração', 'Não', 'Sim', 'Novo na V2'),
   ('Obrigatoriedade', 'Não', 'Sim', 'Novo na V2'),
   ('Declaração processada', 'Não', 'Sim', 'Novo na V2'),
   ('CEP', 'Não', 'Sim', 'Novo na V2')]),
 ('Ocupação',
  [('Código da natureza da ocupação', 'Sim', 'Sim', 'Mantido'),
   ('Descrição do código da natureza da ocupação', 'Sim', 'Sim', 'Mantido'),
   ('Código da ocupação principal', 'Sim', 'Sim', 'Mantido'),
   ('Descrição do código da ocupação principal', 'Sim', 'Sim', 'Mantido')]),
 ('Rendimentos',
  [('Total de renda tributável',
    'Sim',
    'Sim',
    'Mantido com ajuste de nomenclatura. Na V1: "Rendimentos Tributáveis"'),
   ('Total de rendimentos tributáveis recebidos de pessoa jurídica',
    'Sim',
    'Sim',
    'Mantido com ajuste de nomenclatura. Na V1: "Rendimentos Recebidos de Pessoas Jurídicas"')]),
 ('Rendimentos – Pessoa Jurídica',
  [('CNPJ / CPF', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Rendimento recebido', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Contribuição previdenciária', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Imposto retido na fonte', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Décimo terceiro salário', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Imposto retido sobre o 13º salário', 'Não', 'Sim', 'Novo detalhamento na V2')]),
 ('Rendimentos – Aluguéis',
  [('Aluguéis recebidos e outros rendimentos',
    'Sim',
    'Sim',
    'Mantido com ampliação de escopo/nomenclatura. Na V1: "Rendimentos Recebidos de Pessoas Físicas – '
    'Aluguéis"')]),
 ('Rendimentos – Pessoa Física e Exterior',
  [('Código', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Nome', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Meses', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Valor', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Valor total', 'Não', 'Sim', 'Novo detalhamento na V2')]),
 ('Deduções – Livro-caixa', [('Mês', 'Não', 'Sim', 'Novo na V2'), ('Valor', 'Não', 'Sim', 'Novo na V2')]),
 ('Tributação exclusiva/definitiva',
  [('Código', 'Não', 'Sim', 'Novo na V2'), ('Valor', 'Não', 'Sim', 'Novo na V2')]),
 ('Rendimentos isentos e não tributáveis',
  [('Total de rendimentos isentos e não tributáveis',
    'Sim',
    'Não',
    'Na V1 existe como informação consolidada; na V2, conforme a relação fornecida, passa a ser apresentada '
    'por código e valor'),
   ('Código', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Valor', 'Não', 'Sim', 'Novo detalhamento na V2')]),
 ('Atividade rural',
  [('Receita de atividade rural',
    'Sim',
    'Não',
    'Na V1 existe como informação consolidada; na V2, conforme a relação fornecida, passa a ser detalhada'),
   ('Receita bruta total', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Despesa de custeio e investimento total', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Resultado tributável', 'Não', 'Sim', 'Novo detalhamento na V2'),
   ('Limite de 20% sobre a receita bruta total', 'Não', 'Sim', 'Novo detalhamento na V2')]),
 ('Patrimônio',
  [('Total de patrimônio', 'Sim', 'Sim', 'Mantido com ajuste de nomenclatura. Na V1: "Patrimônio Total"')]),
 ('Bens imóveis',
  [('Código do bem', 'Não', 'Sim', 'Novo na V2'),
   ('Descrição do bem', 'Não', 'Sim', 'Novo na V2'),
   ('País', 'Não', 'Sim', 'Novo na V2'),
   ('UF', 'Não', 'Sim', 'Novo na V2'),
   ('Município', 'Não', 'Sim', 'Novo na V2'),
   ('Logradouro', 'Não', 'Sim', 'Novo na V2'),
   ('Número', 'Não', 'Sim', 'Novo na V2'),
   ('Complemento', 'Não', 'Sim', 'Novo na V2'),
   ('Bairro', 'Não', 'Sim', 'Novo na V2'),
   ('CEP do imóvel', 'Não', 'Sim', 'Novo na V2'),
   ('Data de aquisição', 'Não', 'Sim', 'Novo na V2'),
   ('Inscrição municipal (IPTU)', 'Não', 'Sim', 'Novo na V2'),
   ('Área do imóvel', 'Não', 'Sim', 'Novo na V2'),
   ('Indicação de registro em cartório de registro de imóveis', 'Não', 'Sim', 'Novo na V2'),
   ('Número da matrícula do imóvel', 'Não', 'Sim', 'Novo na V2'),
   ('Nome do cartório de registro de imóveis', 'Não', 'Sim', 'Novo na V2'),
   ('Campo de discriminação do bem', 'Não', 'Sim', 'Novo na V2'),
   ('Situação patrimonial anterior', 'Não', 'Sim', 'Novo na V2'),
   ('Situação patrimonial atual', 'Não', 'Sim', 'Novo na V2')])]
comparacao_v2 = ''.join(
    '<h2>' + escape(grupo) + '</h2>' + table(['Campo', 'V1', 'V2 prevista', 'Observação'],
        [tuple(escape(campo) for campo in linha) for linha in linhas])
    for grupo, linhas in METADADOS_V2_PREVISTOS
)
page('dados-v2','Metadados','Metadados previstos para a versão 2.0',
     'Campos previstos e comparação com o conjunto de metadados V1.',
     '<p>A V2 prevê maior detalhamento de rendimentos, informações fiscais e bens imóveis. A lista abaixo apresenta os campos por grupo e compara sua presença na V1 e na V2 prevista. Os nomes e observações seguem o documento de referência, cuja revisão é de 20/10/2026; os detalhes ainda dependem de validação técnica.</p>'
     '<p>Na tabela, “Sim” indica presença na versão indicada e “Não” indica que o campo não consta naquela versão na relação fornecida. As linhas V1 consolidadas são mantidas para explicar o detalhamento previsto na V2; elas não indicam que a informação deixou de existir.</p>'
     '<p>Consulte também <a href="#dados">dados retornados e metadados V1</a> e <a href="#versoes">versões e mudanças</a>.</p>' + comparacao_v2, 'Referência técnica')
by_id = {p['id']: p for p in PAGES}
order = ['inicio','produto','preparacao','conceitos','autenticacao','autorizacao','notificacoes','primeira-consulta','simulacao','descriptografia','versoes','dados','dados-v2','ambientes','referencia','erros','suporte','duvidas']
PAGES = [by_id[i] for i in order]
by_id['duvidas']['group'] = 'Dúvidas frequentes'
for p in PAGES:
    p['body'] = re.sub(r'<aside class="callout [^"]*">(?:(?!</aside>).)*?#gestao(?:(?!</aside>).)*?</aside>', '', p['body'], flags=re.S)
    p['body'] = re.sub(r'<a href="#gestao">[^<]*</a>', 'a equipe de suporte', p['body'])
    p['body'] = p['body'].replace('veja a equipe de suporte antes de implementar essa regra', 'consulte a equipe de suporte antes de implementar essa regra').replace('Quando as fontes públicas divergem, a resposta aponta a pendência em vez de escolher uma versão sem validação.', 'Consulte a equipe de suporte quando precisar esclarecer uma informação.')

css = (ROOT / 'apoio' / 'portal.css').read_text(encoding='utf-8')
js = (ROOT / 'apoio' / 'portal.js').read_text(encoding='utf-8')
logo = base64.b64encode((ROOT / 'apoio' / 'logo-consulta-renda.png').read_bytes()).decode('ascii')
serpro_logo = base64.b64encode((ROOT / 'apoio' / 'serpro-logo-branca.png').read_bytes()).decode('ascii')
brazil_flag = base64.b64encode((ROOT / 'apoio' / 'bandeira-brasil.png').read_bytes()).decode('ascii')
openapi_json = base64.b64encode((ROOT / 'apoio' / 'consulta-renda-openapi-proposta.json').read_bytes()).decode('ascii')
groups = list(dict.fromkeys(p['group'] for p in PAGES))
def nav_title(p):
    if p['id'] == 'duvidas':
        return 'Dúvidas frequentes - FAQ'
    return p['title'] if p['id'] != 'inicio' else 'Visão geral'

nav = ''.join('<div class="nav-group"><p>'+g+'</p>'+''.join(f'<a href="#{p["id"]}" data-nav="{p["id"]}">{nav_title(p)}</a>' for p in PAGES if p['group']==g)+'</div>' for g in groups)
sections = ''.join(f'<article id="{p["id"]}" class="doc-page" data-group="{p["group"]}"><header class="page-heading"><span class="eyebrow">{p["group"]} <span>/</span> {p["kind"]}</span><h1 tabindex="-1">{p["title"]}</h1><p class="lead">{p["lead"]}</p></header>{p["body"]}</article>' for p in PAGES)
html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Consulta Renda · Produto e integração</title><meta name="description" content="O que a Consulta Renda fornece e como avaliar, integrar, consultar dados e resolver problemas."><style>{css}</style></head><body>
<a class="skip" href="#content">Ir para o conteúdo</a>
<header class="topbar"><button id="menu" type="button" aria-label="Abrir navegação" aria-expanded="false">☰</button><a href="#inicio" class="brand"><img class="brand-mark" src="data:image/png;base64,{logo}" alt="Logo Consulta Renda"><span>Consulta Renda<small>Documentação do produto</small></span></a><div class="edition">Proposta para revisão <span>22 out 2026</span></div><a class="openapi-download openapi-download-top" href="data:application/json;base64,{openapi_json}" download="consulta-renda-openapi-proposta.json" title="Baixar especificação OpenAPI (JSON)" aria-label="Baixar especificação OpenAPI (JSON)"><span class="download-icon" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M12 3.5v11m0 0 4-4m-4 4-4-4M5 19h14"></path></svg></span><span>OpenAPI</span></a></header>
<div class="page-shell"><aside class="sidebar" id="sidebar"><div class="sidebar-top"><label class="search-label" for="search">Buscar na documentação</label><div class="version-picker"><button class="version-toggle" id="version-toggle" type="button" aria-haspopup="listbox" aria-expanded="false" aria-controls="version-menu" aria-label="Versão atual: V2. Abrir seletor de versões">V2</button><div class="version-menu" id="version-menu" role="listbox" aria-label="Versões da documentação" hidden><button class="version-option" type="button" role="option" aria-selected="true" data-version="v2">V2</button><button class="version-option" type="button" role="option" aria-selected="false" data-version="v1" data-href="{BASE}" aria-label="V1 — documentação oficial publicada">V1</button></div></div></div><div class="searchbox"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="Tokens, erros, certificado…" autocomplete="off"><kbd>/</kbd></div><p class="search-help">Busque em todas as páginas.</p><div id="results" hidden aria-live="polite"></div><nav id="navigation" aria-label="Documentação">{nav}</nav></aside><div class="scrim" id="scrim" hidden></div><div class="workspace"><main id="content">{sections}<nav class="pagination" aria-label="Sequência de leitura"><a id="previous" href="#inicio"></a><a id="next" href="#produto"></a></nav><footer class="page-footer">Consulta Renda · Proposta para revisão <span>Fontes públicas conferidas em 19/10/2026 · Revisão editorial em 22/10/2026</span></footer></main><aside class="on-page"><p>NESTA PÁGINA</p><nav id="toc" aria-label="Nesta página"></nav></aside></div></div><footer class="serpro-footer"><div class="serpro-footer-inner"><div class="serpro-brand" aria-label="Serpro"><img class="serpro-logo" src="data:image/png;base64,{serpro_logo}" alt="Serpro"><img class="br-flag" src="data:image/png;base64,{brazil_flag}" alt="Bandeira do Brasil"></div><section><h2>Cidadão</h2><button type="button" class="footer-link">Área do Cliente</button></section><section><h2>Suporte</h2><button type="button" class="footer-link">Central de Ajuda</button></section><section class="privacy"><h2>Privacidade</h2><button type="button" class="footer-link">Termos de Uso e Política de Privacidade</button></section></div></footer><div id="toast" role="status"></div><script>{js}</script></body></html>'''
out = ROOT / 'Consulta_Renda_Documentacao_Proposta.html'
out.write_text(html,encoding='utf-8')
(ROOT / 'apoio' / 'exemplo_descriptografia.py').write_text(DECRYPT,encoding='utf-8')
print(json.dumps({'arquivo':str(out),'paginas':len(PAGES),'bytes':out.stat().st_size},ensure_ascii=False))
