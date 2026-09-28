"""Comparações ajustadas por perfil, por padronização (sem regressão).

A ideia: para comparar dois grupos com perfis diferentes (ex.: pública tem
muito mais alunos de baixa renda que privada), dividimos os alunos em estratos
parecidos (mesma faixa de renda, mesma escolaridade da mãe...), comparamos
dentro de cada estrato e fazemos uma média ponderada dessas comparações.
"""

import pandas as pd


def diferenca_ajustada(df: pd.DataFrame, grupo: str, a: str, b: str,
                       estratos: list[str], valor: str = "MEDIA") -> float:
    """Diferença média b - a comparando só alunos do mesmo estrato.

    Os pesos são a distribuição do grupo `a` entre os estratos: responde
    "quanto um aluno típico de `a` ganharia se estivesse em `b`, mantido o
    perfil". Estratos sem alunos dos dois grupos ficam de fora.
    """
    medias = df.groupby(estratos + [grupo], observed=True)[valor].mean().unstack()
    diferencas = (medias[b] - medias[a]).dropna()
    pesos = df[df[grupo] == a].groupby(estratos, observed=True).size()
    pesos = pesos.reindex(diferencas.index)
    return float((diferencas * pesos).sum() / pesos.sum())


def media_padronizada(df: pd.DataFrame, grupo: str, estratos: list[str],
                      valor: str = "MEDIA") -> pd.Series:
    """Média de cada grupo se todos tivessem a composição nacional de estratos.

    Um estado com muitos alunos pobres tem média bruta baixa mesmo que seus
    alunos vão bem para o perfil que têm; a média padronizada remove esse
    efeito. Estrato ausente num grupo usa a média nacional daquele estrato.
    """
    composicao = df.groupby(estratos, observed=True).size()
    composicao = composicao / composicao.sum()
    nacional = df.groupby(estratos, observed=True)[valor].mean()
    por_estrato = df.groupby([grupo] + estratos, observed=True)[valor].mean()

    resultado = {}
    for nome in df[grupo].dropna().unique():
        medias = por_estrato.loc[nome].reindex(composicao.index).fillna(nacional)
        resultado[nome] = (medias * composicao).sum()
    return pd.Series(resultado, name=f"{valor} padronizada")
