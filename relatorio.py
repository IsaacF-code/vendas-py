import streamlit as st
import pandas as pd


# Carregar CSV
base_vendas = pd.read_csv('vendas.csv', sep=';', decimal=',')

# st.sidebar.page_link("relatorio.py", label="Vendas", icon="💰")

st.sidebar.selectbox(
    "Mês",
    ("teste", "teste 2"),
    index=None,
    placeholder="Selecione o mês"
)

