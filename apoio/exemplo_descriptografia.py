# Exemplo proposto: Python + pacote cryptography.
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
