from globals import *
import streamlit as st # type: ignore
import sqlite3
import pandas as pd # type: ignore
import altair as alt # type: ignore
def carregar_dados():
    """carregar dados do banco """
    with sqlite3.connect(BANCO_DADOS) as conn:
        query = "SELECT * FROM registros"  # Nome correto da tabela
        df = pd.read_sql_query(query, conn)
        return df
    return None

# Exibir detalhes de um registro selecionado
def exibir_detalhes(linha):
    """ exibir detalhes """
    st.subheader("Detalhes do Registro")
    for coluna, valor in linha.items():
        st.write(f"**{coluna}**: {valor}")

# Interface principal
def visualizar():
    """ principal """
    st.markdown(
        """
        <style>
            .header {
                background-color: #FF4B4B; /* Fundo vermelho */
                padding: 10px;
                color: white;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .bordered-section {
                border: 2px solid #007bff; /* Cor da borda */
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
            }
            .full-width {
                width: 100%;
            }
        </style>
        <div class="header">
            Lista de Créditos Solicitados.
        </div>
        """,
        unsafe_allow_html=True
    )
    # Carregar os dados do banco
    df = carregar_dados()

    # Filtrar as colunas relevantes 
    df_filtrado = df[["nome", "risco", "renda_mensal","credito_solicitado"]]

    # Destacar toda a linha com situação "crítica" em vermelho
    def colorir_linhas(row):
        if row["risco"] == "alto":
            return ["background-color: red; color: white;" for _ in row]
        if row["risco"] == "moderado":
            return ["background-color: yellow; color: black;" for _ in row]
        if row["risco"] == "baixo":
            return ["background-color: green; color: black;" for _ in row]
        
        return [""] * len(row)

    # Aplicar estilos de coloração nas linhas
    st.subheader("Tabela de Dados")
    styled_df = df_filtrado.style.apply(colorir_linhas, axis=1)

    # Usar `st.table()` para garantir exibição completa dos dados filtrados
    st.table(styled_df)

    # Permitir seleção de um registro para ver detalhes
    indice = st.text_input("Informe o índice da linha para visualizar detalhes:")
    if indice.isdigit() and int(indice) < len(df_filtrado):
        linha = df.iloc[int(indice)].to_dict()  # Obter linha completa
        exibir_detalhes(linha)
    elif indice:
        st.warning("Índice inválido. Informe um número válido.")

    # Gerar gráfico de barras com a totalização por risco
    st.subheader("Gráfico de Barras - Totalização por Risco")
    grafico_df = df["risco"].value_counts().reset_index()
    grafico_df.columns = ["risco", "Total"]

    grafico = alt.Chart(grafico_df).mark_bar().encode(
        x="risco",
        y="Total",
        color="risco"
    ).properties(
        width=800,
        height=400
    )
    st.altair_chart(grafico)
