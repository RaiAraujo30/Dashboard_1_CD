import pandas as pd
import streamlit as st
from pathlib import Path


# ==========================
# Carregamento e preparação
# ==========================

@st.cache_data
def carregar_dados(caminho_vendas: str = "FCD_vendas.csv",
                   caminho_produtos: str = "FCD_produtos.csv") -> pd.DataFrame:
    
    # Lê os arquivos CSV
    vendas = pd.read_csv(caminho_vendas, sep=";")
    produtos = pd.read_csv(caminho_produtos, sep=";")

    # Converte a coluna de data (dia/mês/ano)
    vendas["data_venda"] = pd.to_datetime(
        vendas["data_venda"],
        format="%d/%m/%Y",
        dayfirst=True,
        errors="coerce"
    )

    # Junta com tabela de produtos para trazer nome, categoria, etc.
    df = vendas.merge(produtos, on="produto_id", how="left")

    # Cria colunas auxiliares de período
    df["ano"] = df["data_venda"].dt.year
    df["mes"] = df["data_venda"].dt.month
    df["ano_mes"] = df["data_venda"].dt.to_period("M").astype(str)  # ex: '2024-01'

    return df


# ==========================
# Funções de análise
# ==========================

def aplicar_filtros(df: pd.DataFrame):
    """Aplica filtros de Loja, Produto e Período usando widgets do Streamlit."""

    st.sidebar.header("Filtros")

    # ----------------
    # Filtro por Loja
    # ----------------
    lojas_disponiveis = sorted(df["loja_id"].unique())
    lojas_selecionadas = st.sidebar.multiselect(
        "Selecione a(s) loja(s):",
        options=lojas_disponiveis,
        default=lojas_disponiveis,
        format_func=lambda x: f"Loja {x}"
    )

    # -------------------
    # Filtro por Produto
    # -------------------
    produtos_disponiveis = sorted(df["produto_nome"].dropna().unique())
    produtos_selecionados = st.sidebar.multiselect(
        "Selecione o(s) produto(s):",
        options=produtos_disponiveis,
        default=produtos_disponiveis
    )

    # -------------------
    # Filtro por Período
    # -------------------
    data_min = df["data_venda"].min()
    data_max = df["data_venda"].max()

    periodo = st.sidebar.date_input(
        "Selecione o intervalo de datas:",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )

    if isinstance(periodo, tuple) or isinstance(periodo, list):
        data_inicio, data_fim = periodo
    else:
        # Se por algum motivo vier uma única data, considere como início e fim
        data_inicio = periodo
        data_fim = periodo

    # Garante que fim seja >= início
    if data_fim < data_inicio:
        st.sidebar.warning("A data final é anterior à data inicial. Ajuste o intervalo.")
        data_inicio, data_fim = data_fim, data_inicio

    # --------------
    # Aplica filtros
    # --------------
    df_filtrado = df.copy()

    if lojas_selecionadas:
        df_filtrado = df_filtrado[df_filtrado["loja_id"].isin(lojas_selecionadas)]

    if produtos_selecionados:
        df_filtrado = df_filtrado[df_filtrado["produto_nome"].isin(produtos_selecionados)]

    df_filtrado = df_filtrado[
        (df_filtrado["data_venda"] >= pd.to_datetime(data_inicio)) &
        (df_filtrado["data_venda"] <= pd.to_datetime(data_fim))
    ]

    return df_filtrado, lojas_selecionadas, produtos_selecionados, (data_inicio, data_fim)


def grafico_serie_temporal(df_filtrado: pd.DataFrame):
    """Gráfico de série temporal de quantidade vendida por mês."""
    st.subheader("Série temporal – Quantidade vendida por mês")

    if df_filtrado.empty:
        st.info("Não há dados para o período e filtros selecionados.")
        return

    serie = (
        df_filtrado
        .set_index("data_venda")
        .resample("M")["quantidade_vendida"]
        .sum()
        .rename("Quantidade Vendida")
    )

    # Ajuste de índice para exibição mais amigável (ex: Jan/2024)
    serie.index = serie.index.to_period("M").to_timestamp()

    st.line_chart(serie)


def grafico_top10_produtos(df_filtrado: pd.DataFrame):
    """Gráfico de barras com Top 10 produtos mais vendidos (por quantidade)."""
    st.subheader("Top 10 produtos mais vendidos (por quantidade)")

    if df_filtrado.empty:
        st.info("Não há dados para o período e filtros selecionados.")
        return

    top10 = (
        df_filtrado
        .groupby("produto_nome", as_index=False)["quantidade_vendida"]
        .sum()
        .sort_values("quantidade_vendida", ascending=False)
        .head(10)
    )

    if top10.empty:
        st.info("Não foi possível calcular o Top 10 para os filtros atuais.")
        return

    top10 = top10.set_index("produto_nome")

    st.bar_chart(top10)


def indicador_receita_total(df_filtrado: pd.DataFrame):
    """Exibe a receita total destacada."""
    st.subheader("Indicador de Receita Total")

    if df_filtrado.empty:
        st.metric(label="Receita Total no Período", value="R$ 0,00")
        return

    receita_total = df_filtrado["valor_total"].sum()
    st.metric(
        label="Receita Total no Período Filtrado",
        value=f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )


# ==========================
# Layout principal Streamlit
# ==========================

def main():
    st.set_page_config(
        page_title="Dashboard de Movimentações de Vendas",
        layout="wide"
    )

    st.title("Dashboard de Movimentações de Vendas")
    st.markdown(
        """
        **Objetivo:** Permitir que gestores analisem vendas por loja, produto e período, 
        identifiquem tendências, produtos estratégicos e picos de demanda, apoiando 
        decisões de marketing, reposição e planejamento de estoque.
        """
    )

    # Verifica se os arquivos CSV existem na pasta
    base_path = Path(".")
    caminho_vendas = base_path / "FCD_vendas.csv"
    caminho_produtos = base_path / "FCD_produtos.csv"

    if not caminho_vendas.exists() or not caminho_produtos.exists():
        st.error(
            "Arquivos CSV não encontrados.\n\n"
            "Certifique-se de que **FCD_vendas.csv** e **FCD_produtos.csv** "
            "estão na mesma pasta deste arquivo .py."
        )
        return

    # Carrega dados
    df = carregar_dados(str(caminho_vendas), str(caminho_produtos))

    # Aplica filtros
    df_filtrado, lojas, produtos, (data_inicio, data_fim) = aplicar_filtros(df)

    # Exibe um resumo dos filtros atuais
    st.markdown("### Resumo dos filtros aplicados")
    col1, col2, col3 = st.columns(3)

    with col1:
        if lojas:
            st.write("**Lojas:**", ", ".join(f"Loja {l}" for l in lojas))
        else:
            st.write("**Lojas:** Todas")

    with col2:
        if produtos and len(produtos) < 5:
            st.write("**Produtos:**", ", ".join(produtos))
        elif produtos:
            st.write(f"**Produtos:** {len(produtos)} selecionados")
        else:
            st.write("**Produtos:** Todos")

    with col3:
        st.write(
            "**Período:** ",
            f"{data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}"
        )

    st.markdown("---")

    # Indicador de receita total
    indicador_receita_total(df_filtrado)

    st.markdown("---")

    # Gráficos principais em layout de duas colunas
    col_esq, col_dir = st.columns(2)

    with col_esq:
        grafico_serie_temporal(df_filtrado)

    with col_dir:
        grafico_top10_produtos(df_filtrado)

    st.markdown("---")

    # Opcional: tabela detalhada
    with st.expander("Ver tabela detalhada das vendas filtradas"):
        if df_filtrado.empty:
            st.write("Nenhum dado para exibir.")
        else:
            st.dataframe(
                df_filtrado[
                    [
                        "venda_id",
                        "data_venda",
                        "loja_id",
                        "produto_nome",
                        "categoria",
                        "marca",
                        "quantidade_vendida",
                        "valor_unitario",
                        "valor_total",
                        "forma_pagamento",
                        "canal_venda",
                    ]
                ].sort_values("data_venda")
            )

    # Texto final conectando com a tomada de decisão (item 4 do enunciado)
    st.markdown(
        """
        ---
        ### Como este dashboard apoia a decisão dos gestores

        - **Planejamento de estoque:**  
          A série temporal permite identificar picos de demanda e sazonalidades,
          ajudando a planejar melhor o estoque e evitar rupturas ou excesso de produtos.

        - **Produtos estratégicos:**  
          O gráfico de **Top 10 produtos mais vendidos** destaca quais itens são
          mais importantes para o faturamento, sendo candidatos a ações de marketing,
          promoções ou maior atenção na reposição.

        - **Análise de receita:**  
          O indicador de **Receita Total no período** facilita comparações entre
          diferentes janelas de tempo (por mês, trimestre, ano) e entre lojas ou
          produtos específicos.

        Ajustando os filtros de loja, produto e período, os gestores podem explorar
        cenários diferentes e tomar decisões de marketing, reposição e planejamento
        de vendas de forma mais embasada.
        """
    )


if __name__ == "__main__":
    main()
