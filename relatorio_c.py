import streamlit as st
import pandas as pd
import plotly.express as px


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

col1, col2 = st.columns(gap="medium", spec=2)

# Agrupa a coluna de Data e Cidade, junto com a coluna Total
venda_data_cidade = base_vendas.groupby(['Date', 'City']).agg({'Total': 'sum'}).reset_index()

# Filtra por mês selecionado
venda_mes = venda_data_cidade[venda_data_cidade['Date'].dt.to_period('M').astype(str) == mes_selecionado]

with col1:
    st.write("Faturamento por dia")
    st.bar_chart(venda_mes, x='Date', y='Total', color='City')

# Agrupa produto e cidade
venda_tipo_produto = base_vendas.groupby(['Date', 'Product line', 'City']).agg({'Total': 'sum'}).reset_index()

venda_produto_mes = venda_tipo_produto[venda_tipo_produto['Date'].dt.to_period('M').astype(str) == mes_selecionado]

with col2:
    st.write("Faturamento por tipo de produto")
    st.bar_chart(venda_produto_mes, x='Product line', y='Total', color='City', horizontal=True)

col3, col4, col5 = st.columns(gap='medium', spec=3)

with col3:
    st.write("Faturamento por cidade")
    st.bar_chart(venda_mes, x='City', y='Total')

# Tipo de pagamento com base no período    
tipo_pagamento = base_vendas[base_vendas['Date'].dt.to_period('M').astype(str) == mes_selecionado]

# Soma os valores individuais de cada tipo de pagamento
pagamento = tipo_pagamento.groupby('Payment').agg({'Total': 'sum'}).reset_index()


with col4:
    fig1 = px.pie(values=pagamento['Total'], names=pagamento['Payment'], title='Gráfico de Pizza')
    st.plotly_chart(fig1)

# Agrupa as Cidades e faz a soma da coluna Rating
aval_media = base_vendas.groupby(['Date', 'City']).agg({'Rating': 'sum'}).reset_index()

aval_prod = aval_media[aval_media['Date'].dt.to_period('M').astype(str) == mes_selecionado]

with col5:
    st.write('Avaliação Média')
    st.bar_chart(aval_prod, x='City', y='Rating')

