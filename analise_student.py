from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import kruskal

# =========================================================
# 1. CONFIGURACOES INICIAIS
# =========================================================

CAMINHO_DADOS = Path("data") / "student-mat.csv"
PASTA_SAIDA = Path("outputs")

ROTULOS_STUDYTIME = {
    1: "1 - menos de 2 horas",
    2: "2 - de 2 a 5 horas",
    3: "3 - de 5 a 10 horas",
    4: "4 - mais de 10 horas",
}

# =========================================================
# 2. CARREGAMENTO DOS DADOS
# =========================================================

def carregar_dados(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {caminho}\n"
            "Baixe a base Student Performance da UCI e coloque o arquivo "
            "student-mat.csv dentro da pasta data/."
        )

    return pd.read_csv(caminho, sep=";")

def mostrar_informacoes_iniciais(dados: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("INFORMACOES INICIAIS DO DATASET")
    print("=" * 60)

    print("\nPrimeiras linhas:")
    print(dados.head())

    print("\nInformacoes gerais:")
    dados.info()

    print("\nFormato do dataset:")
    print(f"Linhas: {dados.shape[0]}")
    print(f"Colunas: {dados.shape[1]}")

# =========================================================
# 3. SELECAO E VERIFICACAO DAS VARIAVEIS
# =========================================================

def selecionar_variaveis(dados: pd.DataFrame) -> pd.DataFrame:
    colunas_necessarias = ["studytime", "G3"]

    colunas_ausentes = [
        coluna for coluna in colunas_necessarias
        if coluna not in dados.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"Colunas ausentes no dataset: {colunas_ausentes}"
        )

    return dados[colunas_necessarias].copy()


def verificar_dados(dados: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("VERIFICACAO DAS VARIAVEIS SELECIONADAS")
    print("=" * 60)

    print("\nValores nulos por coluna:")
    print(dados.isnull().sum())

    print("\nTipos das colunas:")
    print(dados.dtypes)

def limpar_dados(dados: pd.DataFrame) -> pd.DataFrame:
    linhas_antes = len(dados)

    dados_limpos = dados.dropna().copy()

    linhas_depois = len(dados_limpos)

    print("\n" + "=" * 60)
    print("LIMPEZA BASICA")
    print("=" * 60)

    print(f"Linhas antes da limpeza: {linhas_antes}")
    print(f"Linhas depois da limpeza: {linhas_depois}")
    print(f"Linhas removidas: {linhas_antes - linhas_depois}")

    return dados_limpos

# =========================================================
# 4. ESTATISTICA DESCRITIVA
# =========================================================

def calcular_estatisticas(dados: pd.DataFrame) -> pd.DataFrame:
    estatisticas = pd.DataFrame(
        {
            "media": dados.mean(numeric_only=True),
            "mediana": dados.median(numeric_only=True),
            "moda": dados.mode().iloc[0],
            "variancia": dados.var(numeric_only=True),
            "desvio_padrao": dados.std(numeric_only=True),
            "q1": dados.quantile(0.25, numeric_only=True),
            "q2": dados.quantile(0.50, numeric_only=True),
            "q3": dados.quantile(0.75, numeric_only=True),
            "amplitude": dados.apply(
                lambda coluna: np.ptp(coluna.to_numpy())
            ),
        }
    )

    return estatisticas

def mostrar_estatisticas(
    estatisticas: pd.DataFrame
) -> None:

    print("\n" + "=" * 60)
    print("ESTATISTICA DESCRITIVA")
    print("=" * 60)

    print(estatisticas.round(2))

# =========================================================
# 5. VISUALIZACOES
# =========================================================

def criar_visualizacoes(dados: pd.DataFrame) -> None:
    PASTA_SAIDA.mkdir(exist_ok=True)

    sns.set_theme(style="whitegrid")

    # -----------------------------------------------------
    # Histograma das notas finais
    # -----------------------------------------------------

    plt.figure(figsize=(8, 5))

    sns.histplot(
        dados["G3"],
        bins=10,
        kde=False,
        color="#3a7ca5"
    )

    plt.title("Distribuicao das notas finais (G3)")
    plt.xlabel("Nota final (G3)")
    plt.ylabel("Quantidade de alunos")

    plt.tight_layout()

    plt.savefig(
        PASTA_SAIDA / "histograma_g3.png",
        dpi=150
    )

    plt.show()

    # -----------------------------------------------------
    # Boxplot geral de G3
    # -----------------------------------------------------

    plt.figure(figsize=(7, 4))

    sns.boxplot(
        x=dados["G3"],
        color="#81b29a"
    )

    plt.title("Boxplot das notas finais (G3)")
    plt.xlabel("Nota final (G3)")

    plt.tight_layout()

    plt.savefig(
        PASTA_SAIDA / "boxplot_g3.png",
        dpi=150
    )

    plt.show()

    # -----------------------------------------------------
    # Distribuicao de studytime
    # -----------------------------------------------------

    contagem_studytime = (
        dados["studytime"]
        .map(ROTULOS_STUDYTIME)
        .value_counts()
        .reindex(ROTULOS_STUDYTIME.values(), fill_value=0)
    )

    plt.figure(figsize=(9, 5))

    sns.barplot(
        x=contagem_studytime.index,
        y=contagem_studytime.values,
        color="#f2cc8f"
    )

    plt.title("Distribuicao do tempo semanal de estudo")

    plt.xlabel("Categoria de tempo de estudo")
    plt.ylabel("Quantidade de alunos")

    plt.xticks(rotation=20, ha="right")

    plt.tight_layout()

    plt.savefig(
        PASTA_SAIDA / "barras_studytime.png",
        dpi=150
    )

    plt.show()

    # -----------------------------------------------------
    # Boxplot por categoria de studytime
    # -----------------------------------------------------

    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=dados,
        x="studytime",
        y="G3",
        palette="Set2"
    )

    plt.title(
        "Notas finais por categoria de tempo de estudo"
    )

    plt.xlabel("Tempo semanal de estudo")
    plt.ylabel("Nota final (G3)")

    plt.xticks(
        ticks=[0, 1, 2, 3],
        labels=[
            "menos de 2h",
            "2 a 5h",
            "5 a 10h",
            "mais de 10h",
        ],
    )

    plt.tight_layout()

    plt.savefig(
        PASTA_SAIDA / "boxplot_studytime_g3.png",
        dpi=150
    )

    plt.show()

    print("\nGraficos salvos na pasta outputs/:")
    print("- histograma_g3.png")
    print("- boxplot_g3.png")
    print("- barras_studytime.png")
    print("- boxplot_studytime_g3.png")

# =========================================================
# 6. INTERPRETACOES AUTOMATICAS
# =========================================================

def identificar_faixa_mais_comum(
    notas: pd.Series
) -> str:

    faixas = pd.cut(
        notas,
        bins=[-0.1, 4, 9, 14, 20],
        labels=["0 a 4", "5 a 9", "10 a 14", "15 a 20"],
    )

    return str(faixas.value_counts().idxmax())

def mostrar_interpretacoes(
    dados: pd.DataFrame
) -> None:

    media_g3 = dados["G3"].mean()

    faixa_mais_comum = identificar_faixa_mais_comum(
        dados["G3"]
    )

    studytime_mais_frequente = (
        dados["studytime"].mode().iloc[0]
    )

    rotulo_studytime = ROTULOS_STUDYTIME.get(
        studytime_mais_frequente,
        "categoria desconhecida"
    )

    print("\n" + "=" * 60)
    print("INTERPRETACOES AUTOMATICAS")
    print("=" * 60)

    print(f"Media das notas finais (G3): {media_g3:.2f}")

    print(
        f"Faixa de notas mais comum: "
        f"{faixa_mais_comum}"
    )

    print(
        "Categoria de tempo de estudo "
        f"mais frequente: {rotulo_studytime}"
    )

# =========================================================
# 7. ASSOCIACAO ENTRE VARIAVEIS
# =========================================================

def classificar_forca_correlacao(
    correlacao: float
) -> str:

    valor_absoluto = abs(correlacao)

    if valor_absoluto < 0.20:
        return "muito fraca"

    if valor_absoluto < 0.40:
        return "fraca"

    if valor_absoluto < 0.60:
        return "moderada"

    if valor_absoluto < 0.80:
        return "forte"

    return "muito forte"

# ---------------------------------------------------------
# Correlacao de Spearman
# ---------------------------------------------------------

def calcular_correlacao_spearman(
    dados: pd.DataFrame
) -> float:

    return dados["studytime"].corr(
        dados["G3"],
        method="spearman"
    )

# ---------------------------------------------------------
# Teste de Kruskal-Wallis
# ---------------------------------------------------------

def calcular_kruskal(
    dados: pd.DataFrame
) -> Tuple[float, float]:

    grupos = [
        grupo["G3"].values
        for _, grupo in dados.groupby("studytime")
    ]

    estatistica, p_valor = kruskal(*grupos)

    return estatistica, p_valor

# ---------------------------------------------------------
# Epsilon squared
# ---------------------------------------------------------

def calcular_epsilon_quadrado(
    h: float,
    n: int,
    k: int
) -> float:

    epsilon2 = (h - k + 1) / (n - k)

    return max(0, epsilon2)

def classificar_epsilon_quadrado(
    epsilon2: float
) -> str:

    if epsilon2 < 0.01:
        return "efeito insignificante"

    if epsilon2 < 0.08:
        return "efeito pequeno"

    if epsilon2 < 0.26:
        return "efeito moderado"

    return "efeito grande"

# =========================================================
# 8. ANALISE DE ASSOCIACAO
# =========================================================

def mostrar_analise_associacao(
    dados: pd.DataFrame
) -> None:

    # -----------------------------------------------------
    # Correlacao de Spearman
    # -----------------------------------------------------

    correlacao = calcular_correlacao_spearman(
        dados
    )

    forca_correlacao = (
        classificar_forca_correlacao(correlacao)
    )

    # -----------------------------------------------------
    # Kruskal-Wallis
    # -----------------------------------------------------

    estatistica_kw, p_valor_kw = (
        calcular_kruskal(dados)
    )

    # -----------------------------------------------------
    # Epsilon squared
    # -----------------------------------------------------

    epsilon2 = calcular_epsilon_quadrado(
        h=estatistica_kw,
        n=len(dados),
        k=dados["studytime"].nunique()
    )

    classificacao_epsilon2 = (
        classificar_epsilon_quadrado(epsilon2)
    )

    # -----------------------------------------------------
    # Estatisticas por grupo
    # -----------------------------------------------------

    media_por_tempo_estudo = (
        dados.groupby("studytime")["G3"]
        .agg(["count", "mean", "median", "std"])
        .rename(
            columns={
                "count": "quantidade",
                "mean": "media_G3",
                "median": "mediana_G3",
                "std": "desvio_padrao_G3",
            }
        )
    )

    media_por_tempo_estudo.index = (
        media_por_tempo_estudo.index.map(
            ROTULOS_STUDYTIME
        )
    )

    # -----------------------------------------------------
    # Resultados
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("ASSOCIACAO ENTRE TEMPO DE ESTUDO E NOTA FINAL")
    print("=" * 60)

    print(
        f"Correlacao de Spearman: "
        f"{correlacao:.3f}"
    )

    print(
        f"Forca da associacao: "
        f"{forca_correlacao}"
    )

    print("\n" + "=" * 60)
    print("TESTE DE KRUSKAL-WALLIS")
    print("=" * 60)

    print(
        f"Estatistica H: "
        f"{estatistica_kw:.3f}"
    )

    print(
        f"p-valor: "
        f"{p_valor_kw:.5f}"
    )

    if p_valor_kw < 0.05:
        print(
            "Resultado: existem diferencas "
            "estatisticamente significativas "
            "entre os grupos de tempo de estudo."
        )

    else:
        print(
            "Resultado: nao foram encontradas "
            "diferencas estatisticamente "
            "significativas entre os grupos."
        )

    print("\n" + "=" * 60)
    print("TAMANHO DO EFEITO (EPSILON SQUARED)")
    print("=" * 60)

    print(
        f"Epsilon squared (ε²): "
        f"{epsilon2:.3f}"
    )

    print(
        f"Interpretacao do efeito: "
        f"{classificacao_epsilon2}"
    )

    print("\n" + "=" * 60)
    print("RESUMO DAS NOTAS POR CATEGORIA")
    print("=" * 60)

    print(media_por_tempo_estudo.round(2))

# =========================================================
# 9. EXECUCAO DO PIPELINE
# =========================================================

def main() -> None:
    dados = carregar_dados(CAMINHO_DADOS)

    mostrar_informacoes_iniciais(dados)

    dados_selecionados = selecionar_variaveis(
        dados
    )

    verificar_dados(dados_selecionados)

    dados_limpos = limpar_dados(
        dados_selecionados
    )

    estatisticas = calcular_estatisticas(
        dados_limpos
    )

    mostrar_estatisticas(estatisticas)

    criar_visualizacoes(dados_limpos)

    mostrar_interpretacoes(dados_limpos)

    mostrar_analise_associacao(
        dados_limpos
    )

if __name__ == "__main__":
    main()