"""Carregamento do parquet e o recorte usado em todas as análises."""

from pathlib import Path

import pandas as pd

from dicionario import NOTAS, PRESENCAS

PROCESSED = Path(__file__).resolve().parents[1] / "data" / "processed"


def carregar(ano: int = 2023, colunas: list[str] | None = None) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED / f"enem_{ano}.parquet", columns=colunas)


def concluintes(df: pd.DataFrame) -> pd.DataFrame:
    """Alunos que terminam o ensino médio no ano do exame e fizeram as 4 provas.

    O recorte é obrigatório para comparar escolas: o INEP só registra o tipo
    de escola de quem conclui o ensino médio naquele ano. Quem já concluiu ou é
    treineiro aparece sempre como "Não respondeu". Exigir presença nos dois
    dias evita que um zero de falta derrube a média.

    Adiciona MEDIA: a média simples das cinco notas (4 provas + redação).
    """
    presente = df[PRESENCAS].eq("Presente").all(axis=1)
    recorte = df[(df["TP_ST_CONCLUSAO"] == "Conclui em 2023") & presente].copy()
    recorte["MEDIA"] = recorte[NOTAS].mean(axis=1)
    return recorte
