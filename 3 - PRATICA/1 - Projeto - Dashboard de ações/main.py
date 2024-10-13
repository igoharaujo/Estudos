import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta
import numpy as np


#Função
@st.cache_data
def carregar_dados(acao):
    texto_tickers = " ".join(acao)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes = dados_acao.history(period='1d', start='2010-01-01', end='2024-10-10')
    cotacoes = cotacoes['Close']
    return cotacoes

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=';')
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers


acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)



# INTERFACE
st.write(f"""
# Preço das Ações
         
O gráfico abaixo representa a evolução do preço das ações ao longo do tempo

""")

#filtro
st.sidebar.header("Filtros")



# Filtro acao
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualiar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "close"})

#filtro data
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", 
                                   min_value=data_inicial, 
                                   max_value=data_final, 
                                   value=(data_inicial, data_final),
                                   step=timedelta(days=1)
                                   )
        

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]        
#Grafico
st.line_chart(dados)

#Calculo de perfomance
texto_performance_ativos = ""


if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns={"close": acao_unica})


carteira =[1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)


for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] = carteira[i] * (1 + performance_ativo)

    if np.isnan(performance_ativo):  
        continue
    if performance_ativo > 0:
        texto_performance_ativos += f"  \n{acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos += f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos += f"  \n{acao}: {performance_ativo:.1%}"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteria com os ativos: :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = f"Performance da carteria com os ativos: :red[{performance_carteira:.1%}]"

else:
    texto_performance_carteira = f"Performance da carteria com os ativos: {performance_carteira:.1%}"


st.write(f"""
### Perfomance dos ativos
         
Essa foi a perfomance de cada ativo no período selecionado:
         
{texto_performance_ativos}


{texto_performance_carteira}

""")