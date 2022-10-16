# Bibliotecas utilizadas
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.figure_factory as ff
import plotly.express as px
from sklearn.metrics import roc_curve, auc

#Função para gerar o plot de resultados
def plot_confusion_matriz(confusion_matrix, tab):

    z = confusion_matrix

    x = ['não sobrevive', 'sobrevive']
    y = ['não sobrevive', 'sobrevive']

    # change each element of z to type string for annotations
    z_text = [[str(y)[:4] for y in x] for x in z]

    # set up figure 
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='blues')

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=0.5,
                            y=-0.15,
                            showarrow=False,
                            text="Predicted value",
                            xref="paper",
                            yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=-0.35,
                            y=0.5,
                            showarrow=False,
                            text="Real value",
                            textangle=-90,
                            xref="paper",
                            yref="paper"))

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=50, l=200))

    # add colorbar
    fig['data'][0]['showscale'] = True
    # Plot!
    acuracia = (float(confusion_matrix[0][0])+float(confusion_matrix[1][1]))/2
    fig.update_layout(title=f'Matrix confusão (Acurácia={acuracia:.2f})')
    tab.plotly_chart(fig, use_container_width=True)

def roc_curve_plot(path1, path2, tab):

    # Lista com as cidades e seus códigos do IBGE
    y_true = []
    # open file and read the content in a list
    with open(path1, 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            y_true.append(int(x))

    # Lista com as cidades e seus códigos do IBGE
    y_score = []
    # open file and read the content in a list
    with open(path2, 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            y_score.append(float(x))

    fpr, tpr, thresholds = roc_curve(y_true, y_score)

    fig = px.area(
        x=fpr, y=tpr,
        labels=dict(x='False Positive Rate', y='True Positive Rate'),
        width=700, height=500
    )
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(constrain='domain')
    
    # Plot!
    fig.update_layout(title=f'Curva ROC (AUC={auc(fpr, tpr):.2f})')
    tab.plotly_chart(fig, use_container_width=True)

# Definicao das imagens e videos
video_apresentacao = open('fotos/TeaserTcc20220921.mp4', 'rb')
video_bytes = video_apresentacao.read()
perfiljean = Image.open('fotos/JeanCarloTeodoroDaSilva.jpeg')
perfillucas = Image.open('fotos/LucasSerafim.jpeg')
perfiljones = Image.open('fotos/Jones.jpeg')
perfilvanderlei = Image.open('fotos/Vanderlei.jpeg')

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
    botaojean = col1.button("LinkedIn de Jean Carlo")
    if botaojean:
        col1.success('https://www.linkedin.com/in/jean-carlo-teodoro-da-silva/')

    col2.image(perfillucas, caption='Lucas Paulino Serafim', width=275)
    botaolucas = col2.button("LinkedIn de Lucas")
    if botaolucas:
        col2.success('https://www.linkedin.com/in/lucas-serafim/')

    col1.markdown('## Orientador:')
    col1.image(perfiljones, caption='Jones Eduardo Egydio', width=200)
    botaojones = col1.button("LinkedIn de Jones")
    if botaojones:
        col1.success('https://www.linkedin.com/in/jones-egydio-msc-3300359/')

    col2.markdown('## Coorientador:')
    col2.image(perfilvanderlei, caption='Vanderlei Cunha Parro', width=200)
    botaovanderlei = col2.button("LinkedIn de Vanderlei")
    if botaovanderlei:
        col2.success('https://www.linkedin.com/in/vparro/')
    
with tab2:
    tab2.markdown('Este trabalho trata do desenvolvimento de uma inteligência artificial (IA) para prever a sobrevida de pacientes com câncer de boca ou de orofaringe. Os resultados providos pela IA são comparados com os dos modelos de predição utilizados atualmente na área médica. Esta abordagem mostra potencial para melhorar implementações na área de saúde.')
    
with tab3:
    pass

with tab4:

    tab4.markdown('## Modelos de Inteligência Artificial (IA) em dados de validação:')
    
    # Definição das tabs
    tab40, tab41, tab42, tab43, tab44, tab45, tab46, tab47, tab48, tab49 = st.tabs(['6 meses', '12 meses', '18 meses', '24 meses', '30 meses', '36 meses', '42 meses', '48 meses', '54 meses', '60 meses',])

        
    # Resultados para a label 6 meses
    with tab40:
        confusion_matrix_6meses = [[0.66842452,  0.33157548], [0.3371059, 0.6628941]]
        plot_confusion_matriz(confusion_matrix_6meses, tab40)
        roc_curve_plot(r'curvaROC/y_true_6meses.txt', r'curvaROC/y_score_6meses.txt', tab40)
 
    # Resultados para a label 12 meses
    with tab41:
        confusion_matrix_12meses = [[0.70366133, 0.29633867],[0.30053191, 0.69946809]]
        plot_confusion_matriz(confusion_matrix_12meses, tab41)
        roc_curve_plot(r'curvaROC/y_true_12meses.txt', r'curvaROC/y_score_12meses.txt', tab41)

    # Resultados para a label 18 meses
    with tab42:
        confusion_matrix_18meses = [[0.66842452,  0.33157548], [0.3371059, 0.6628941]]
        plot_confusion_matriz(confusion_matrix_18meses, tab42)
        roc_curve_plot(r'curvaROC/y_true_18meses.txt', r'curvaROC/y_score_18meses.txt', tab42)
        
    # Resultados para a label 24 meses
    with tab43:
        confusion_matrix_24meses = [[0.66842452,  0.33157548], [0.3371059, 0.6628941]]
        plot_confusion_matriz(confusion_matrix_24meses, tab43)
        roc_curve_plot(r'curvaROC/y_true_24meses.txt', r'curvaROC/y_score_24meses.txt', tab43)
 
    # Resultados para a label 30 meses
    with tab44:
        confusion_matrix_30meses = [[0.66842452,  0.33157548], [0.3371059, 0.6628941]]
        plot_confusion_matriz(confusion_matrix_30meses, tab44)
        roc_curve_plot(r'curvaROC/y_true_30meses.txt', r'curvaROC/y_score_30meses.txt', tab44)

    # Resultados para a label 36 meses
    with tab45:
        confusion_matrix_36meses = [[0.66684902, 0.33315098], [0.33477322, 0.66522678]]
        plot_confusion_matriz(confusion_matrix_36meses, tab45)
        roc_curve_plot(r'curvaROC/y_true_36meses.txt', r'curvaROC/y_score_36meses.txt', tab45)

    # Resultados para a label 42 meses
    with tab46:
        confusion_matrix_42meses = [[0.66842452,  0.33157548], [0.3371059, 0.6628941]]
        plot_confusion_matriz(confusion_matrix_42meses, tab46)
        roc_curve_plot(r'curvaROC/y_true_42meses.txt', r'curvaROC/y_score_42meses.txt', tab46)

    # Resultados para a label 48 meses
    with tab47:
        confusion_matrix_48meses = [[0.65059185, 0.34940815], [0.35306554, 0.64693446]]
        plot_confusion_matriz(confusion_matrix_48meses, tab47)
        roc_curve_plot(r'curvaROC/y_true_48meses.txt', r'curvaROC/y_score_48meses.txt', tab47)

    # Resultados para a label 54 meses
    with tab48:
        confusion_matrix_54meses = [[0.65059185, 0.34940815], [0.35306554, 0.64693446]]
        plot_confusion_matriz(confusion_matrix_54meses, tab48)
        roc_curve_plot(r'curvaROC/y_true_54meses.txt', r'curvaROC/y_score_54meses.txt', tab48)

    # Resultados para a label 60 meses
    with tab49:
        confusion_matrix_60meses = [[0.62914418, 0.37085582], [0.3625, 0.6375]]
        plot_confusion_matriz(confusion_matrix_60meses, tab49)
        roc_curve_plot(r'curvaROC/y_true_60meses.txt', r'curvaROC/y_score_60meses.txt', tab49)

with tab5:
    pass

with tab6:
    pass