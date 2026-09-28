"""Colunas usadas, tipos de leitura e rótulos dos códigos do ENEM 2023.

Os rótulos foram copiados do dicionário oficial que vem no zip do INEP
(DICIONÁRIO/Dicionário_Microdados_Enem_2023.xlsx). Em outros anos os códigos
e as faixas de renda mudam, então confira no dicionário daquele ano.
"""

import pandas as pd

NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
PRESENCAS = ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]

# Tipos na leitura. "Int8" (maiúsculo) é o inteiro que aceita vazio: quem não
# declarou a escola ou faltou à prova vem sem valor nessas colunas. Os textos
# só viram category depois do concat dos chunks (ver preparar.py).
DTYPES = {
    "TP_FAIXA_ETARIA": "Int8",
    "TP_SEXO": "str",
    "TP_COR_RACA": "Int8",
    "TP_ST_CONCLUSAO": "Int8",
    "TP_ESCOLA": "Int8",
    "IN_TREINEIRO": "Int8",
    "SG_UF_ESC": "str",
    "TP_DEPENDENCIA_ADM_ESC": "Int8",
    "TP_LOCALIZACAO_ESC": "Int8",
    "SG_UF_PROVA": "str",
    **dict.fromkeys(PRESENCAS, "Int8"),
    **dict.fromkeys(NOTAS, "float32"),
    "TP_STATUS_REDACAO": "Int8",
    "Q001": "str",  # escolaridade do pai
    "Q002": "str",  # escolaridade da mãe
    "Q006": "str",  # renda familiar
}
COLUNAS = list(DTYPES)

ESCOLARIDADE = {
    "A": "Nunca estudou",
    "B": "Fundamental I incompleto",
    "C": "Fundamental I completo",
    "D": "Fundamental II completo",
    "E": "Médio completo",
    "F": "Superior completo",
    "G": "Pós-graduação",
    "H": "Não sei",
}

# Faixas em reais. O salário mínimo de 2023 era R$ 1.320, então B = até 1 SM,
# C = até 1,5 SM, D = até 2 SM, e assim por diante até Q = acima de 20 SM.
RENDA = {
    "A": "Nenhuma renda",
    "B": "Até 1.320",
    "C": "1.320 a 1.980",
    "D": "1.980 a 2.640",
    "E": "2.640 a 3.300",
    "F": "3.300 a 3.960",
    "G": "3.960 a 5.280",
    "H": "5.280 a 6.600",
    "I": "6.600 a 7.920",
    "J": "7.920 a 9.240",
    "K": "9.240 a 10.560",
    "L": "10.560 a 11.880",
    "M": "11.880 a 13.200",
    "N": "13.200 a 15.840",
    "O": "15.840 a 19.800",
    "P": "19.800 a 26.400",
    "Q": "Acima de 26.400",
}

# As 17 faixas agrupadas em 5, em salários mínimos. Útil quando cruzar renda
# com outra variável deixaria grupos pequenos demais (ex.: renda x estado).
RENDA_SM = {
    "Nenhuma renda": "Até 1 SM", "Até 1.320": "Até 1 SM",
    "1.320 a 1.980": "1 a 2 SM", "1.980 a 2.640": "1 a 2 SM",
    "2.640 a 3.300": "2 a 4 SM", "3.300 a 3.960": "2 a 4 SM", "3.960 a 5.280": "2 a 4 SM",
    "5.280 a 6.600": "4 a 7 SM", "6.600 a 7.920": "4 a 7 SM", "7.920 a 9.240": "4 a 7 SM",
    **dict.fromkeys(list(RENDA.values())[10:], "Mais de 7 SM"),
}
FAIXAS_SM = ["Até 1 SM", "1 a 2 SM", "2 a 4 SM", "4 a 7 SM", "Mais de 7 SM"]

ROTULOS = {
    "TP_FAIXA_ETARIA": {
        1: "Menor de 17", 2: "17", 3: "18", 4: "19", 5: "20", 6: "21", 7: "22",
        8: "23", 9: "24", 10: "25", 11: "26 a 30", 12: "31 a 35", 13: "36 a 40",
        14: "41 a 45", 15: "46 a 50", 16: "51 a 55", 17: "56 a 60",
        18: "61 a 65", 19: "66 a 70", 20: "Maior de 70",
    },
    "TP_SEXO": {"M": "Masculino", "F": "Feminino"},
    "TP_COR_RACA": {
        0: "Não declarado", 1: "Branca", 2: "Preta", 3: "Parda", 4: "Amarela",
        5: "Indígena", 6: "Não dispõe da informação",
    },
    "TP_ST_CONCLUSAO": {
        1: "Já concluiu", 2: "Conclui em 2023", 3: "Conclui após 2023",
        4: "Não concluiu e não está cursando",
    },
    "TP_ESCOLA": {1: "Não respondeu", 2: "Pública", 3: "Privada"},
    "TP_DEPENDENCIA_ADM_ESC": {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"},
    "TP_LOCALIZACAO_ESC": {1: "Urbana", 2: "Rural"},
    "TP_STATUS_REDACAO": {
        1: "Sem problemas", 2: "Anulada", 3: "Cópia texto motivador", 4: "Em branco",
        6: "Fuga ao tema", 7: "Não atendimento ao tipo textual",
        8: "Texto insuficiente", 9: "Parte desconectada",
    },
    **dict.fromkeys(PRESENCAS, {0: "Faltou", 1: "Presente", 2: "Eliminado"}),
    "Q001": ESCOLARIDADE,
    "Q002": ESCOLARIDADE,
    "Q006": RENDA,
}


def categorizar(df: pd.DataFrame) -> pd.DataFrame:
    """Troca códigos por rótulos, como categorias ordenadas.

    Ordenadas porque a ordem importa: um groupby por renda sai de "Nenhuma
    renda" até "Acima de 26.400", e não em ordem alfabética.
    """
    df = df.copy()
    for coluna, rotulos in ROTULOS.items():
        tipo = pd.CategoricalDtype(list(rotulos.values()), ordered=True)
        df[coluna] = df[coluna].map(rotulos).astype(tipo)
    for coluna in ["SG_UF_ESC", "SG_UF_PROVA"]:
        df[coluna] = df[coluna].astype("category")
    df["IN_TREINEIRO"] = df["IN_TREINEIRO"].astype("boolean")
    return df
