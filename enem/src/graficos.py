"""Estilo comum dos gráficos: paleta, eixos discretos e função para salvar.

A paleta categórica segue uma ordem fixa, validada para daltonismo nos três
primeiros slots. Com mais de três séries, agrupe em "Outros" ou divida em
vários gráficos em vez de inventar cores.
"""

from pathlib import Path

import matplotlib.pyplot as plt

FIGURAS = Path(__file__).resolve().parents[1] / "reports" / "figures"

AZUL, LARANJA, VERDE_AGUA = "#2a78d6", "#eb6834", "#1baf7a"
CATEGORICA = [AZUL, LARANJA, VERDE_AGUA]
# Rampa sequencial (um só tom, do claro ao escuro) para faixas ordenadas como renda.
SEQUENCIAL = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6",
              "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
CINZA = "#8a8984"

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
GRADE = "#e4e3df"


def aplicar_estilo() -> None:
    plt.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "axes.edgecolor": GRADE,
        "axes.labelcolor": TEXTO_SECUNDARIO,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler(color=CATEGORICA),
        "grid.color": GRADE,
        "grid.linewidth": 0.8,
        "xtick.color": TEXTO_SECUNDARIO,
        "ytick.color": TEXTO_SECUNDARIO,
        "lines.linewidth": 2,
        "lines.markersize": 8,
        "legend.frameon": False,
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def salvar(fig, nome: str) -> Path:
    destino = FIGURAS / f"{nome}.png"
    fig.savefig(destino)
    return destino
