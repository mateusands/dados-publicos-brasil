"""Converte o CSV dos microdados do ENEM em um Parquet enxuto.

Uso:
    uv run enem/src/preparar.py            # ano padrão (2023)

O CSV tem ~1,7 GB e ~4 milhões de linhas. Três escolhas deixam isso tratável:

1. `usecols`: das ~76 colunas, lemos só as que a análise usa.
2. `dtype`: códigos viram int8/category e notas float32, em vez dos int64,
   float64 e strings que o pandas escolheria sozinho.
3. `chunksize`: o arquivo é lido em pedaços, então o pico de memória é o de um
   pedaço, não o do arquivo inteiro.

O CSV é lido direto de dentro do zip, sem extrair. O resultado é um Parquet em
enem/data/processed/ que os notebooks carregam em segundos.
"""

import argparse
import time
import zipfile
from pathlib import Path

import pandas as pd

from dicionario import COLUNAS, DTYPES, categorizar

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
LINHAS_POR_CHUNK = 500_000


def ler_csv(ano: int) -> pd.DataFrame:
    zip_path = RAW / f"microdados_enem_{ano}.zip"
    membro = f"microdados_enem_{ano}/DADOS/MICRODADOS_ENEM_{ano}.csv"

    pedacos = []
    with zipfile.ZipFile(zip_path) as z, z.open(membro) as csv:
        leitor = pd.read_csv(
            csv,
            sep=";",
            encoding="latin-1",
            usecols=COLUNAS,
            dtype=DTYPES,
            chunksize=LINHAS_POR_CHUNK,
        )
        for i, pedaco in enumerate(leitor, start=1):
            pedacos.append(pedaco)
            print(f"\rchunk {i}: {i * LINHAS_POR_CHUNK:,} linhas lidas", end="", flush=True)
    print()

    # As categorias só são aplicadas depois do concat: cada chunk veria um
    # conjunto diferente de valores, e o concat de categorias diferentes
    # volta a ser texto.
    return categorizar(pd.concat(pedacos, ignore_index=True))


def preparar(ano: int) -> Path:
    inicio = time.perf_counter()
    df = ler_csv(ano)
    destino = PROCESSED / f"enem_{ano}.parquet"
    df.to_parquet(destino, index=False)

    memoria = df.memory_usage(deep=True).sum() / 1e6
    print(f"{len(df):,} linhas, {df.shape[1]} colunas, {memoria:.0f} MB em memória")
    print(f"{destino.name}: {destino.stat().st_size / 1e6:.0f} MB em disco")
    print(f"tempo: {time.perf_counter() - inicio:.0f} s")
    return destino


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ano", type=int, default=2023)
    preparar(parser.parse_args().ano)
