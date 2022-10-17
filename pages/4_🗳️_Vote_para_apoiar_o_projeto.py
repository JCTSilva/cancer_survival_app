# Bibliotecas utilizadas
import pandas as pd
import numpy as np
import streamlit as st
import pickle
from sklearn import  preprocessing
import plotly.express as px
from PIL import Image
from geopy.distance import geodesic


eureka = Image.open('fotos/eureka2022-logo.png')
st.image(eureka, use_column_width=True)

qrcodevoto = Image.open('fotos/qr.png')

st.markdown('### Vote no projeto para apoiar o desenvolvimento do sistema de saúde brasileiro por meio do link ou QR code abaixo.\n')
st.warning('Nós fizemos uso de um encurtador de link. Portanto, não estranhe ou se preocupe com vírus se houver uma página intermediária para acessar a página de voto. \n\n Agradecemos o apoio!')
st.markdown('https://bityli.com/projeto-tcc-cancer-ia')
st.image(qrcodevoto, caption='QR code para votar no projeto', width=300, output_format='PNG')