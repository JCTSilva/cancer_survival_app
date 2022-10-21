# Bibliotecas utilizadas
import pandas as pd
import numpy as np
import streamlit as st
import pickle
from sklearn import preprocessing
import plotly.express as px
from PIL import Image
from geopy.distance import geodesic
import plotly.graph_objects as go
import pydeck as pdk


eureka = Image.open('fotos/eureka2022-logo.png')
st.image(eureka, use_column_width=True)

##--------------------------------------Função para gerar os gráficos-------------------------------------------
def graficos(df):

    data = df.copy()

    fig = px.histogram(data, x="IDADE", color="Vivo_Morto", 
    title="<b><i>Última informação sobre os pacientes por idade<b><i>", 
    color_discrete_sequence=px.colors.sequential.RdBu).update_xaxes(categoryorder='total descending')
    fig.update_layout(xaxis_title_text='Idade',yaxis_title_text='Contagem')
    fig.update_traces(opacity=0.9)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(data, x="Escolaridade", color="Vivo_Morto", 
    title="<b><i>Última informação sobre os pacientes por escolaridade<b><i>", 
    histnorm = 'percent', color_discrete_sequence=px.colors.sequential.RdBu).update_xaxes(categoryorder='total descending')
    fig.update_layout(xaxis_title_text='Escolaridade',yaxis_title_text='Porcentagem')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.pie(data, names='Sexo_Nome', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(title='Relação de pacientes por sexo')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(data, x="EC", color="Vivo_Morto", 
    title="<b><i>Última informação sobre os pacientes por estadio clínico<b><i>", 
    histnorm = 'percent', color_discrete_sequence=px.colors.sequential.RdBu).update_xaxes(categoryorder='total descending')
    fig.update_layout(xaxis_title_text='Estadio clínico',yaxis_title_text='Porcentagem')
    st.plotly_chart(fig, use_container_width=True)

##--------------------------------------Leitura dos dados do banco-------------------------------------------
@st.experimental_memo
def le_analise_dataset():
    dataframe = pd.read_csv('dados/analise_dataset.csv', index_col='Unnamed: 0')
    return dataframe

##--------------------------------------Filtro dos dados para análise-------------------------------------------
@st.experimental_memo
def filtra_dados(dataframe):
    
    return ""
##--------------------------------------Filtro dos dados para análise-------------------------------------------
@st.experimental_memo
def filtra_dados(dataframe, idademin, idademax, escolari, ec):
    aux_df = dataframe.loc[dataframe.IDADE >= idademin].copy()
    aux_df = aux_df.loc[aux_df.IDADE <= idademax].copy()
    if escolari != 'TODAS AS OPÇÕES':
        aux_df = aux_df.loc[aux_df.Escolaridade == escolari].copy()
    if ec != 'TODAS AS OPÇÕES':
        aux_df = aux_df.loc[aux_df.EC == ec].copy()
    return aux_df

##--------------------------------------Setup de variáveis-------------------------------------------
data = le_analise_dataset()

##--------------------------------------Corpo da página-------------------------------------------
# Variável para alocar informações na barra lateral
lat = st.sidebar

# Input das variáveis
idademin = lat.slider('Idade mínima dos pacientes:', min_value=0, max_value=100, step=1, format='%i')
idademax = lat.slider('Idade máxima dos pacientes:', min_value=100, max_value=0, step=1, format='%i')
escolari = lat.selectbox('Escolaridade dos pacientes:', ['TODAS AS OPÇÕES', 'Analfabeto', 'Ensino fund. Incompleto', 
'Ensino fund. Completo', 'Ensino Médio', 'Ensino Superior'])
ec = lat.selectbox('Estadio clínico:', ['TODAS AS OPÇÕES', 'I', 'II', 'III', 'IV', 'IVA', 'IVB', 'IVC'])

# Filtro dos dados para gerar os gráficos
aux_df = filtra_dados(data, idademin, idademax, escolari, ec)

# Output dos resultados
st.markdown(f'### Total de casos: {aux_df.shape[0]}')
graficos(df=aux_df)