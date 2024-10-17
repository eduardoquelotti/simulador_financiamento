import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Funções para calcular financiamento
def calcular_sac(valor_imovel, entrada, taxa_juros, prazo):
    valor_financiado = valor_imovel - entrada
    amortizacao = valor_financiado / prazo
    saldo_devedor = valor_financiado
    tabela = []

    for mes in range(1, prazo + 1):
        juros = saldo_devedor * (taxa_juros / 12)
        prestacao = amortizacao + juros
        saldo_devedor -= amortizacao
        tabela.append([mes, prestacao, amortizacao, juros, saldo_devedor])

    return pd.DataFrame(tabela, columns=["Mês", "Prestação", "Amortização", "Juros", "Saldo Devedor"])

def calcular_price(valor_imovel, entrada, taxa_juros, prazo):
    valor_financiado = valor_imovel - entrada
    i = taxa_juros / 12
    prestacao = valor_financiado * (i * (1 + i) ** prazo) / ((1 + i) ** prazo - 1)
    saldo_devedor = valor_financiado
    tabela = []

    for mes in range(1, prazo + 1):
        juros = saldo_devedor * i
        amortizacao = prestacao - juros
        saldo_devedor -= amortizacao
        tabela.append([mes, prestacao, amortizacao, juros, saldo_devedor])

    return pd.DataFrame(tabela, columns=["Mês", "Prestação", "Amortização", "Juros", "Saldo Devedor"])

# Interface com o usuário
st.title("Simulador de Financiamento Imobiliário")

valor_imovel = st.number_input("Valor do Imóvel (R$)", min_value=50000.0, step=1000.0)
entrada = st.number_input("Valor da Entrada (R$)", min_value=0.0, step=1000.0)
taxa_juros = st.slider("Taxa de Juros Anual (%)", 6.0, 12.0, step=0.1)
prazo = st.slider("Prazo (meses)", 60, 360, step=12)
tipo_amortizacao = st.selectbox("Sistema de Amortização", ["SAC", "Tabela Price"])

if st.button("Simular"):
    if tipo_amortizacao == "SAC":
        resultado = calcular_sac(valor_imovel, entrada, taxa_juros / 100, prazo)
    else:
        resultado = calcular_price(valor_imovel, entrada, taxa_juros / 100, prazo)
    
    st.subheader("Tabela de Financiamento")
    st.dataframe(resultado)

    # Gráfico do saldo devedor
    fig = px.line(resultado, x="Mês", y="Saldo Devedor", title="Evolução do Saldo Devedor")
    st.plotly_chart(fig)