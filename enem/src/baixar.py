"""Baixa o zip dos microdados do ENEM direto do INEP.

Uso:
    uv run enem/src/baixar.py            # ano padrão (2023)
    uv run enem/src/baixar.py --ano 2022

O zip (~550 MB) fica em enem/data/raw/ e não é extraído: o preparar.py lê o
CSV de dentro do zip, sem ocupar 1,7 GB extras no disco.
"""

import argparse
import ssl
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
URL = "https://download.inep.gov.br/microdados/microdados_enem_{ano}.zip"
INTERMEDIARIO = "http://secure.globalsign.com/cacert/rnpicpedugr46ovtlsca2025.crt"
BLOCO = 1024 * 1024


def contexto_ssl() -> ssl.SSLContext:
    """Contexto SSL que completa a cadeia de certificados do INEP.

    O servidor do INEP não envia o certificado intermediário, e o Python (ao
    contrário do navegador) não vai buscá-lo sozinho. Baixamos o intermediário
    do endereço indicado no próprio certificado e o usamos só para montar a
    cadeia: com PARTIAL_CHAIN desligado, ela ainda precisa terminar numa raiz
    confiável do sistema, então um intermediário adulterado seria recusado.
    """
    with urllib.request.urlopen(INTERMEDIARIO, timeout=30) as resposta:
        pem = ssl.DER_cert_to_PEM_cert(resposta.read())
    contexto = ssl.create_default_context()
    contexto.verify_flags &= ~ssl.VERIFY_X509_PARTIAL_CHAIN
    contexto.load_verify_locations(cadata=pem)
    return contexto


def abrir(url: str):
    try:
        return urllib.request.urlopen(url, timeout=60)
    except urllib.error.URLError as erro:
        if not isinstance(erro.reason, ssl.SSLCertVerificationError):
            raise
        return urllib.request.urlopen(url, timeout=60, context=contexto_ssl())


def baixar(ano: int) -> Path:
    destino = RAW / f"microdados_enem_{ano}.zip"
    resposta = abrir(URL.format(ano=ano))
    total = int(resposta.headers["Content-Length"])

    if destino.exists() and destino.stat().st_size == total:
        print(f"{destino.name} já baixado ({total / 1e6:.0f} MB)")
        return destino

    # Baixa num .part e só renomeia no fim: um download interrompido nunca
    # fica parecendo um arquivo completo.
    parcial = destino.with_suffix(".zip.part")
    baixado = 0
    with resposta, parcial.open("wb") as arquivo:
        while bloco := resposta.read(BLOCO):
            arquivo.write(bloco)
            baixado += len(bloco)
            print(f"\r{baixado / 1e6:6.0f} / {total / 1e6:.0f} MB", end="", flush=True)
    print()

    if baixado != total:
        sys.exit(f"download incompleto: {baixado} de {total} bytes")
    parcial.rename(destino)
    return destino


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ano", type=int, default=2023)
    print(baixar(parser.parse_args().ano))
