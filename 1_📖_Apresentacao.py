# Bibliotecas utilizadas
from turtle import delay
import pandas as pd
import numpy as np
import streamlit as st
import pickle
from sklearn import  preprocessing
import plotly.express as px
from PIL import Image
from geopy.distance import geodesic

# Definicao das imagens e videos
video_apresentacao = open('/home/FinalProject_IMT_CANCER/TeaserTcc20220921.mp4', 'rb')
video_bytes = video_apresentacao.read()
perfiljean = Image.open('/home/FinalProject_IMT_CANCER/JeanCarloTeodoroDaSilva.jpeg')
perfillucas = Image.open('/home/FinalProject_IMT_CANCER/LucasSerafim.jpeg')
perfiljones = Image.open('/home/FinalProject_IMT_CANCER/Jones.jpeg')
perfilvanderlei = Image.open('/home/FinalProject_IMT_CANCER/Vanderlei.jpeg')

# Definição das tabs
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Vídeo teaser', 'Responsáveis', 'Resumo', 'Objetivo', 'Resultados', 'Conclusões', 'Apoio'])

with tab0:

    # Separação das colunas
    col1, col2 = tab0.columns(2)

    tab0.markdown('## Entenda sobre o projeto em 1 minuto')
    tab0.video(video_bytes, format="video/mp4", start_time=0)



with tab1:
    
    tab1.markdown('## Desenvolvedores:')

    # Separação das colunas
    col1, col2 = tab1.columns(2)

    col1.image(perfiljean, caption='Jean Carlo T. da Silva', width=275)
    botaojean = col1.button("Linkedin de Jean Carlo")
    if botaojean:
        col1.success('https://www.linkedin.com/in/jean-carlo-teodoro-da-silva/')

    col2.image(perfillucas, caption='Lucas Paulino Serafim', width=275)
    botaolucas = col2.button("Linkedin de Lucas")
    if botaolucas:
        col2.success('https://www.linkedin.com/in/lucas-serafim/')

    col1.markdown('## Orientador:')
    col1.image(perfiljones, caption='Jones Eduardo Egydio', width=200)
    botaojones = col1.button("Linkedin de Jones")
    if botaojones:
        col1.success('https://www.linkedin.com/in/jones-egydio-msc-3300359/')

    col2.markdown('## Coorientador:')
    col2.image(perfilvanderlei, caption='Vanderlei Cunha Parro', width=200)
    botaovanderlei = col2.button("Linkedin de Vanderlei")
    if botaovanderlei:
        col2.success('https://www.linkedin.com/in/vparro/')
    
with tab2:
    tab2.markdown('Este trabalho trata do desenvolvimento de uma inteligência artificial (IA) para prever a sobrevida de pacientes com câncer de boca ou de orofaringe. Os resultados providos pela IA são comparados com os dos modelos de predição utilizados atualmente na área médica. Esta abordagem mostra potencial para melhorar implementações na área de saúde.')
    
with tab3:
    pass

with tab4:
    pass

with tab5:
    pass

with tab6:
    pass