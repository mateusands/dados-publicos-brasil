# ENEM 2023: nota por estado, tipo de escola e renda

Quanto o lugar onde o aluno mora, o tipo de escola em que estudou e a renda da
família explicam a nota no ENEM?

## Perguntas

1. **Estado**: quais UFs têm as maiores e menores médias? A diferença é
   igual nas cinco provas?
2. **Tipo de escola**: qual a distância entre escola pública e privada? E
   dentro da pública, entre federal, estadual e municipal?
3. **Renda**: como a nota cresce com a faixa de renda familiar? O crescimento é
   linear ou tem saltos?
4. **Cruzamentos**: a diferença entre pública e privada some quando se compara
   alunos da mesma faixa de renda? Um aluno pobre de escola federal vai melhor
   que um aluno rico de escola estadual?

## Dados

[Microdados do ENEM 2023](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem),
publicados pelo INEP: um CSV de ~1,7 GB, com uma linha por inscrito
(~3,9 milhões) e ~76 colunas. Os dados são anonimizados, sem nome nem CPF.

**Por que 2023 e não 2024?** A partir de 2024 o INEP divide os dados em
`PARTICIPANTES` e `RESULTADOS`, sem chave para ligar os dois arquivos. Com
isso, não dá mais para cruzar a nota com o questionário socioeconômico (renda).

## Como rodar

```bash
uv run enem/src/baixar.py      # baixa o zip (~550 MB) para data/raw/
uv run enem/src/preparar.py    # CSV do zip -> data/processed/enem_2023.parquet
uv run jupyter lab             # abre enem/notebooks/
```

## Estrutura

```
enem/
├── data/
│   ├── raw/          zip original do INEP (fora do git)
│   └── processed/    parquet enxuto gerado pelo preparar.py (fora do git)
├── notebooks/
│   ├── 01_exploracao.ipynb   volume, quem são os inscritos, recorte, primeira olhada
│   └── 02_cruzamentos.ipynb  escola x renda x estado, com ajuste pelo perfil
├── reports/figures/  gráficos exportados pelos notebooks
└── src/
    ├── baixar.py     download do INEP
    ├── dicionario.py colunas usadas, tipos e rótulos dos códigos
    ├── preparar.py   leitura em chunks e conversão para parquet
    ├── base.py       carregar() e o recorte concluintes() usado nas análises
    ├── ajuste.py     comparações ajustadas por perfil (padronização)
    └── graficos.py   paleta e estilo comum dos gráficos
```

## Achados até agora

| | |
|---|---|
| Volume | 1,8 GB de CSV → 46 MB de Parquet; 3,6 GB estimados em memória na leitura ingênua → 153 MB |
| Armadilha | o tipo de escola só existe para quem conclui o ensino médio em 2023 (1,4 mi de 3,9 mi inscritos) |
| Escola | privada 617 · federal 595 · municipal 523 · estadual 511 |
| Renda | de 472 (sem renda) a 655 (acima de R$ 26,4 mil), subindo em todas as faixas |
| Estado | de 491 (AM) a 563 (MG) |
| Escola, ajustada | a vantagem da privada cai de 100 para 67 pontos comparando a mesma renda, e para 60 somando a escolaridade dos pais |
| Rede federal | a partir de R$ 1.320 de renda, empata com a privada ou a supera; aluno pobre de federal ≈ aluno rico de estadual |
| Estado, ajustado | a distância entre estados cai de 71 para 43 pontos; CE vai de 25º para 12º, SP de 2º para 9º |

Médias das 5 notas, entre concluintes de 2023 presentes nas 4 provas (1,05 mi).
