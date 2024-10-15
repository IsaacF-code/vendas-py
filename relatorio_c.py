import streamlit as st
import pandas as pd
import matplotlib as plt


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
# vendas_filtradas = base_vendas[base_vendas['Date'].dt.to_period('M').astype(str) == mes_selecionado]
# st.write(vendas_filtradas)

col1, col2 = st.columns(gap="medium", spec=2)

# Agrupa a coluna de Data e Cidade, junto com a coluna Total
venda_data_cidade = base_vendas.groupby(['Date', 'City']).agg({'Total': 'sum'}).reset_index()

# Filtra por mês selecionado
venda_mes = venda_data_cidade[venda_data_cidade['Date'].dt.to_period('M').astype(str) == mes_selecionado]

with col1:
    st.write("Faturamento por dia")
    st.bar_chart(venda_mes, x='Date', y='Total', color='City')


venda_tipo_produto = base_vendas.groupby(['Date', 'Product line', 'City']).agg({'Total': 'sum'}).reset_index()

venda_produto_mes = venda_tipo_produto[venda_tipo_produto['Date'].dt.to_period('M').astype(str) == mes_selecionado]

with col2:
    st.write("Faturamento por tipo de produto")
    st.bar_chart(venda_produto_mes, x='Product line', y='Total', color='City', horizontal=True)

col3, col4, col5 = st.columns(3)

with col3:
    st.write("Faturamento por cidade")
    st.bar_chart(venda_mes, x='City', y='Total')

# exemplo de gráfico pizza
# data = pd.DataFrame({
#     "Categoria": ['A', 'B', 'C', 'D'],
#     "Valores": [25, 30, 15, 20]
# })

# st.title("Gráfico de pizza")
# plt.pie(data['Valores'], labels=data['Categoria'])

# st.pyplot()


# base_vendas['Total'] = base_vendas['Date'].dt.to_period('M')

# vendas_por_mes = base_vendas.groupby('Total')

# st.bar_chart(vendas_por_mes)

# st.write(vendas_filtradas)


# st.sidebar.page_link("relatorio.py", label="Vendas", icon="💰")