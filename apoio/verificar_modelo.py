from pathlib import Path
from html.parser import HTMLParser
import ast
import base64
import contextlib
import io
import json
import os
import tempfile
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

ROOT = Path(__file__).resolve().parent.parent

class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.pages = []
        self.external_assets = []
        self.code_count = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and a.get('href', '').startswith('#'):
            self.links.append(a['href'][1:].split('~')[0])
        if tag == 'article':
            self.pages.append(a.get('id'))
        if tag in ('script', 'img', 'iframe', 'link'):
            resource = a.get('src') or a.get('href') or ''
            if resource.startswith(('http://', 'https://')):
                self.external_assets.append(a)
        if tag == 'pre':
            self.code_count += 1

p = Structure()
p.feed((ROOT / 'Consulta_Renda_Documentacao_Proposta.html').read_text(encoding='utf-8'))
assert len(p.ids) == len(set(p.ids)), 'IDs duplicados'
assert set(p.links) <= set(p.ids), f'Links quebrados: {set(p.links)-set(p.ids)}'
assert len(p.pages) == 18, len(p.pages)
assert not p.external_assets, 'Dependências externas no HTML'
assert p.code_count >= 10
assert 'alt="Logo Consulta Renda"' in (ROOT / 'Consulta_Renda_Documentacao_Proposta.html').read_text(encoding='utf-8')
assert 'data:image/png;base64,' in (ROOT / 'Consulta_Renda_Documentacao_Proposta.html').read_text(encoding='utf-8')
source = (ROOT / 'apoio' / 'exemplo_descriptografia.py').read_text(encoding='utf-8')
ast.parse(source)

# Execute the exact proposed snippet with a disposable, synthetic PKCS#12 key.
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
p12 = pkcs12.serialize_key_and_certificates(
    b'fixture-local', key, None, None,
    serialization.BestAvailableEncryption(b'senha-sintetica')
)
values = ['48000.00', 'Ocupação fictícia']
payload = {'dados': [
    {'codigo': str(i+1), 'texto': 'Campo de teste',
     'valor': base64.b64encode(key.public_key().encrypt(v.encode('utf-8'), padding.PKCS1v15())).decode('ascii')}
    for i,v in enumerate(values)
]}
ns = {}
output = io.StringIO()
with patch('builtins.input', return_value='fixture-sintetica.p12'), patch('getpass.getpass', return_value='senha-sintetica'), patch.object(Path, 'read_bytes', return_value=p12), patch.object(Path, 'read_text', return_value=json.dumps(payload)), contextlib.redirect_stdout(output):
    exec(compile(source, 'exemplo_descriptografia.py', 'exec'), ns)
assert [x['valor'] for x in ns['dados_legiveis']] == values
assert '2 campos' in output.getvalue()

print(json.dumps({
    'paginas': len(p.pages), 'links_internos_validos': len(p.links),
    'dependencias_remotas': len(p.external_assets),
    'exemplo_descriptografia': 'aprovado com chave e resposta sinteticas locais',
    'api_real': 'nao executada'
}, ensure_ascii=False))
