import streamlit as st
import pandas as pd


# Carregar CSV
base_vendas = pd.read_csv('vendas.csv', sep=';', decimal=',')

# Converter para data
base_vendas['Date'] = pd.to_datetime(base_vendas['Date'], format='%m/%d/%Y', dayfirst=False, errors='coerce')

# Verifica se há valores nulos
if base_vendas['Date'].isnull().any():
    st.write("Algumas não poderam ser convertidas")

# Extrair meses
meses = base_vendas['Date'].dt.to_period('M').unique()

# Filtro dos meses
mes_selecionado = st.sidebar.selectbox(
    "Mês",
    meses.astype(str),
    index=None,
    placeholder="Selecione o mês"
)

# Filtrar por mês selecionado
vendas_filtradas = base_vendas[base_vendas['Date'].dt.to_period('M').astype(str) == mes_selecionado]

base_vendas['Total'] = base_vendas['Date'].dt.to_period('M')

vendas_por_mes = base_vendas.groupby('Total')

st.bar_chart(vendas_por_mes)

# st.write(vendas_filtradas)


# st.sidebar.page_link("relatorio.py", label="Vendas", icon="💰")