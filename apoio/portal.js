document.documentElement.classList.add('js');
const pages=[...document.querySelectorAll('.doc-page')];
const navLinks=[...document.querySelectorAll('[data-nav]')];
const search=document.getElementById('search');
const results=document.getElementById('results');
const navigation=document.getElementById('navigation');
const sidebar=document.getElementById('sidebar');
const menu=document.getElementById('menu');
const scrim=document.getElementById('scrim');
let currentId='inicio';
let topicObserver;
const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const index=pages.map(p=>({id:p.id,title:p.querySelector('h1').textContent,text:p.textContent.replace(/\s+/g,' ').trim()}));
function closeMenu(){sidebar.classList.remove('open');menu.setAttribute('aria-expanded','false');scrim.hidden=true;}
function route(){
  let raw;try{raw=decodeURIComponent(location.hash.slice(1));}catch{raw='inicio';}
  let [id,heading]=raw.split('~');
  if(!pages.some(p=>p.id===id))id='inicio';
  const active=pages.find(p=>p.id===id);
  pages.forEach(p=>p.classList.toggle('active',p===active));
  navLinks.forEach(a=>{if(a.dataset.nav===id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  document.title=active.querySelector('h1').textContent+' · Consulta Renda';
  const toc=document.getElementById('toc');toc.replaceChildren();
  const headings=[...active.querySelectorAll('h2')];
  headings.forEach((h,i)=>{h.id=id+'-h'+i;const a=document.createElement('a');a.href='#'+id+'~'+i;a.dataset.tocTopic=String(i);a.textContent=h.textContent;toc.append(a);});
  if(topicObserver)topicObserver.disconnect();
  const tocLinks=[...toc.querySelectorAll('[data-toc-topic]')];
  const markTopic=i=>tocLinks.forEach(a=>{if(Number(a.dataset.tocTopic)===i)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
  topicObserver=new IntersectionObserver(entries=>{
    const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);
    if(visible.length)markTopic(Number(visible[0].target.id.slice(id.length+2)));
    else {
      const passed=headings.filter(h=>h.getBoundingClientRect().top<125);
      if(passed.length)markTopic(Number(passed[passed.length-1].id.slice(id.length+2)));
    }
  },{rootMargin:'-125px 0px -65% 0px',threshold:0});
  headings.forEach(h=>topicObserver.observe(h));
  if(heading!==undefined&&headings[Number(heading)])markTopic(Number(heading));
  const i=pages.indexOf(active),prev=document.getElementById('previous'),next=document.getElementById('next');
  prev.hidden=i===0;next.hidden=i===pages.length-1;
  if(i>0){prev.href='#'+pages[i-1].id;prev.textContent='← '+pages[i-1].querySelector('h1').textContent;}
  if(i<pages.length-1){next.href='#'+pages[i+1].id;next.textContent=pages[i+1].querySelector('h1').textContent+' →';}
  closeMenu();
  if(heading!==undefined){const h=headings[Number(heading)];if(h)h.scrollIntoView({block:'start'});}
  else if(currentId!==id||window.scrollY>0){window.scrollTo({top:0,behavior:'instant'});}
  currentId=id;
}
window.addEventListener('hashchange',route);route();
menu.addEventListener('click',()=>{const open=!sidebar.classList.contains('open');sidebar.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));scrim.hidden=!open;});
scrim.addEventListener('click',closeMenu);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();search.value='';updateSearch();}if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();if(window.innerWidth<=760){sidebar.classList.add('open');menu.setAttribute('aria-expanded','true');scrim.hidden=false;}search.focus();}});
function updateSearch(){
  const term=normalize(search.value.trim());results.replaceChildren();navigation.hidden=!!term;results.hidden=!term;
  if(!term)return;
  const terms=term.split(/\s+/);
  const matches=index.filter(p=>terms.every(t=>normalize(p.text).includes(t))).sort((a,b)=>(normalize(b.title).includes(term)?1:0)-(normalize(a.title).includes(term)?1:0));
  const count=document.createElement('p');count.className='search-count';count.textContent=matches.length?matches.length+' página(s) encontrada(s)':'Nenhuma página encontrada. Tente “token”, “erro” ou “certificado”.';results.append(count);
  matches.forEach(p=>{const a=document.createElement('a');a.className='search-hit';a.href='#'+p.id;a.textContent=p.title;const small=document.createElement('small');const pos=normalize(p.text).indexOf(terms[0]);small.textContent='…'+p.text.slice(Math.max(0,pos-30),Math.max(0,pos-30)+140)+'…';a.append(small);a.addEventListener('click',()=>{search.value='';updateSearch();closeMenu();});results.append(a);});
}
search.addEventListener('input',updateSearch);
let toastTimer;
function toast(text){const el=document.getElementById('toast');el.textContent=text;el.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('visible'),2500);}
async function copyText(text){
  if(navigator.clipboard&&window.isSecureContext){try{await navigator.clipboard.writeText(text);return true;}catch{}}
  const area=document.createElement('textarea');area.value=text;area.style.cssText='position:fixed;top:-9999px';document.body.append(area);area.select();let ok=false;try{ok=document.execCommand('copy');}catch{}area.remove();return ok;
}
document.querySelectorAll('.copy').forEach(btn=>btn.addEventListener('click',async()=>{const ok=await copyText(btn.closest('.codebox').querySelector('code').textContent);toast(ok?'Código copiado.':'Selecione e copie o código manualmente.');}));
const checkboxes=[...document.querySelectorAll('.checklist input')];
let stored={};try{stored=JSON.parse(localStorage.getItem('consulta-renda-checklist-v1')||'{}')||{};}catch{}
checkboxes.forEach(c=>{c.checked=stored[c.dataset.key]===true;c.addEventListener('change',()=>{stored[c.dataset.key]=c.checked;try{localStorage.setItem('consulta-renda-checklist-v1',JSON.stringify(stored));}catch{}updateProgress();});});
function updateProgress(){document.getElementById('check-progress').textContent=checkboxes.filter(c=>c.checked).length+' de '+checkboxes.length+' itens concluídos.';}
updateProgress();
document.getElementById('print').addEventListener('click',()=>window.print());
const diagnoses={
  '401':['Identifique qual token e qual camada falharam.','No gateway, confira a validade do bearer token e renove se necessário. Na consulta de negócio, confira serviço, versão e destinatário da autorização. Renovar o bearer token não corrige um compartilhamento incompatível.'],
  '403':['Confira o vínculo e o acesso da instituição.','Verifique contrato, identificações e cadastro das chaves. A documentação contém orientações sobre acolhimento; se a situação persistir, encaminhe o contexto ao suporte.'],
  '404a':['Verifique se existe autorização para esse par de identificações.','Confira CNPJ, CPF, destinatário escolhido e conclusão do compartilhamento. A página de retornos de Autorizações associa esse código à ausência de autorização.'],
  '404c':['Trate a ausência de declaração.','A documentação de Consultar associa 404 ao CPF sem declaração no exercício atual. Não interprete isso como renda zero.'],
  '415':['Confira o formato da solicitação de acesso.','Na chamada de token, utilize Content-Type: application/x-www-form-urlencoded e o campo grant_type=client_credentials.'],
  '500':['Registre a falha e avalie a disponibilidade.','Confira a operação, o horário e a mensagem. Verifique /status e siga o fluxo de suporte se a falha persistir.'],
  '503':['Confira a mensagem antes de decidir a ação.','As páginas oficiais consultadas descrevem causas diferentes. Uma política de repetição precisa considerar a mensagem real, a disponibilidade e a orientação do suporte.'],
  'crypto':['Separe consulta bem-sucedida de leitura bem-sucedida.','Confira ambiente, chave privada correspondente e configuração de descriptografia. Vá ao guia de descriptografia para seguir a sequência.']
};
const problem=document.getElementById('problem');function diagnose(){const [title,body]=diagnoses[problem.value];const target=document.getElementById('diagnosis');target.replaceChildren();const b=document.createElement('strong');b.textContent=title;const p=document.createElement('p');p.textContent=body;target.append(b,p);}
problem.addEventListener('change',diagnose);diagnose();
let stage=0;
const scenario=document.getElementById('scenario'),nextSim=document.getElementById('sim-next');
function resetSim(){stage=0;document.getElementById('sim-title').textContent='Comece pelo acesso à API';document.getElementById('sim-text').textContent='A aplicação solicita um token de acesso com suas credenciais. Aqui usaremos apenas identificadores fictícios.';document.getElementById('sim-output').textContent='Nenhuma etapa executada.';nextSim.textContent='Simular autenticação →';nextSim.disabled=false;document.querySelectorAll('[data-stage]').forEach(e=>e.classList.remove('done'));}
function advanceSim(){
  stage++;let title,text,output,label,done=false;
  if(stage===1){title='Acesso à API preparado';text='O token de acesso vai no cabeçalho Authorization das próximas chamadas.';output='HTTP 200 · fictício\n{ "access_token": "BEARER_FICTICIO" }';label='Simular busca de autorização →';}
  if(stage===2&&scenario.value==='none'){title='Nenhuma autorização encontrada';text='Confira os identificadores e a conclusão do compartilhamento pelo titular. O fluxo para antes de consultar renda.';output='GET /Autorizacoes/CNPJ_FICTICIO/CPF_FICTICIO\nHTTP 404 · cenário didático';done=true;}
  else if(stage===2){title='Compartilhamento localizado';text='A autorização identifica o titular, o destinatário e as condições do compartilhamento. Seu token será usado na consulta.';output='Token de compartilhamento fictício: AUTORIZACAO_FICTICIA\nAutorização compatível: assumida neste cenário';label='Simular consulta de renda →';}
  if(stage===3&&scenario.value==='noirpf'){title='Declaração não encontrada';text='A ausência de declaração precisa de tratamento no processo de negócio. Ela não corresponde a renda zero.';output='GET /Consultar/AUTORIZACAO_FICTICIA\nHTTP 404 · cenário didático';done=true;}
  else if(stage===3){title='Resposta recebida';text='Os campos podem ser identificados, mas seus valores ainda exigem descriptografia. O texto abaixo apenas representa o conteúdo cifrado.';output='HTTP 200 · fictício\n{ "dados": [\n  { "codigo": "1", "valor": "CIFRADO_FICTICIO" }\n] }';label='Mostrar leitura didática →';}
  if(stage===4){title='Dados legíveis para interpretação';text='Na aplicação real, esta etapa usa a chave privada. Aqui apenas mostramos um valor inventado, sem executar criptografia.';output='Código: 1\nInformação: rendimentos de pessoas jurídicas\nValor fictício para ilustração: 48.000,00\nLeia também o ano-calendário e o conjunto de metadados.';done=true;}
  document.getElementById('sim-title').textContent=title;document.getElementById('sim-text').textContent=text;document.getElementById('sim-output').textContent=output;nextSim.textContent=done?'Cenário concluído':label;nextSim.disabled=done;
  document.querySelectorAll('[data-stage]').forEach(e=>e.classList.toggle('done',Number(e.dataset.stage)<=stage));
}
nextSim.addEventListener('click',advanceSim);document.getElementById('sim-reset').addEventListener('click',resetSim);scenario.addEventListener('change',resetSim);
