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

##--------------------------------------Funções para gerar os gráficos-------------------------------------------
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
data = pd.read_csv('dados/analise_dataset.csv', index_col='Unnamed: 0')

lat = st.sidebar

idademin = lat.slider('Idade mínima dos pacientes:', min_value=0, max_value=100, step=1, format='%i')
idademax = lat.slider('Idade máxima dos pacientes:', min_value=100, max_value=0, step=1, format='%i')
escolari = lat.selectbox('Escolaridade dos pacientes:', ['TODAS AS OPÇÕES', 'Analfabeto', 'Ensino fund. Incompleto', 
'Ensino fund. Completo', 'Ensino Médio', 'Ensino Superior'])
ec = lat.selectbox('Estadio clínico:', ['TODAS AS OPÇÕES', 'I', 'II', 'III', 'IV', 'IVA', 'IVB', 'IVC'])

aux_df = data.loc[data.IDADE >= idademin].copy()
aux_df = data.loc[data.IDADE <= idademax].copy()
if escolari != 'TODAS AS OPÇÕES':
    aux_df = data.loc[data.Escolaridade == escolari].copy()
if ec != 'TODAS AS OPÇÕES':
    aux_df = data.loc[data.EC == ec].copy()

st.markdown(f'### Total de casos: {aux_df.shape[0]}')
graficos(df=aux_df)

# Define a layer to display on a map
layer = pdk.Layer(
    "GridLayer",
    aux_df,
    pickable=True,
    extruded=True,
    cell_size=10000,
    elevation_scale=400,
    get_position='LAT_LONG'
)

view_state = pdk.ViewState(latitude=-24, longitude=-48, zoom=6, bearing=0, pitch=45)

# Render
r = pdk.Deck(
    layers=layer,
    initial_view_state=view_state,
    tooltip={"text": "{position}\nCount: {count}"},
)

st.pydeck_chart(pydeck_obj=r)