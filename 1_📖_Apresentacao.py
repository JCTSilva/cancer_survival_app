# Bibliotecas utilizadas
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.figure_factory as ff
import plotly.express as px
from sklearn.metrics import roc_curve, auc


eureka = Image.open('fotos/eureka2022-logo.png')
st.image(eureka, use_column_width=True)
st.markdown('## Aplicação de Inteligência Artificial para predição de sobrevida em pacientes com câncer')

#Função para gerar o plot de resultados
def plot_confusion_matriz(confusion_matrix, tab):
    # Quantidade de acertos e erros
    VN = confusion_matrix[0][0]
    FP = confusion_matrix[0][1]
    FN = confusion_matrix[1][0]
    VP = confusion_matrix[1][1]
    
    # (VP+VN)/(VP+VN+FV+FN)
    acuracia = (VP+VN)/(VP+FP+VN+FN)
    precisao = (VP)/(VP+FP)
    revocacao = (VP)/(VP+FN)
    f1_score = (2*precisao*revocacao)/(precisao+revocacao)

    # Porcentagem de acertos e erros do modelo
    VN_ = VN/(VN+FP)
    FP_ = FP/(VN+FP)
    VP_ = VP/(VP+FN)
    FN_ = FN/(VP+FN)

    # Normalização dos resultados
    confusion_matrix = [[VN_, FP_], [FN_,VP_]]

    x = ['não sobrevive', 'sobrevive']
    y = ['não sobrevive', 'sobrevive']

    # change each element of z to type string for annotations
    z_text = [[str(y)[:4] for y in x] for x in confusion_matrix]

    # set up figure 
    fig = ff.create_annotated_heatmap(confusion_matrix, x=x, y=y, annotation_text=z_text, colorscale='blues')

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=0.5,
                            y=-0.15,
                            showarrow=False,
                            text="<b>Predicted value<b>",
                            xref="paper",
                            yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                            x=-0.35,
                            y=0.5,
                            showarrow=False,
                            text="<b>Real value<b>",
                            textangle=-90,
                            xref="paper",
                            yref="paper"))

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=40, l=200))

    # add colorbar
    fig['data'][0]['showscale'] = True
    # Plot!
    fig.update_layout(title=f'<i><b>Confusion Matrix<b><i> (Accuracy={100*acuracia:.1f}% - Recall={100*revocacao:.1f}%)')
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
        labels=dict(x='<b>False Positive Rate<b>', y='<b>True Positive Rate<b>'),
        width=700, height=500
    )
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(constrain='domain')
    
    # Plot!
    fig.update_layout(title=f'<i><b>ROC Curve (AUC={100*auc(fpr, tpr):.1f}%)<i><b>')
    tab.plotly_chart(fig, use_container_width=True)

# Definicao das imagens e videos
video_apresentacao = open('fotos/TeaserTcc20220921.mp4', 'rb')
video_bytes = video_apresentacao.read()
perfiljean = Image.open('fotos/JeanCarloTeodoroDaSilva.jpeg')
perfillucas = Image.open('fotos/LucasSerafim.jpeg')
perfiljones = Image.open('fotos/Jones.jpeg')
perfilvanderlei = Image.open('fotos/Vanderlei.jpeg')
perfilstela = Image.open('fotos/Stela.jpeg')
perfilmaria = Image.open('fotos/MariaPaula.png')
fosp = Image.open('fotos/Fosp.png')
accamargo = Image.open('fotos/ACCamargo.png')

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

    col1.image(perfiljean, caption='Jean Carlo Teodoro da Silva', width=275)
    botaojean = col1.button("LinkedIn de Jean Carlo")
    if botaojean:
        col1.success('https://www.linkedin.com/in/jean-carlo-teodoro-da-silva/')

    col2.image(perfillucas, caption='Lucas Paulino Serafim', width=275)
    botaolucas = col2.button("LinkedIn de Lucas")
    if botaolucas:
        col2.success('https://www.linkedin.com/in/lucas-serafim/')

    col1, col2 = tab1.columns(2)
    
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
    tab2.markdown('''Este trabalho trata do desenvolvimento de uma inteligência artificial (IA) para prever a sobrevida de pacientes com câncer 
    de boca ou de orofaringe. Os resultados providos pela IA são comparados com os dos modelos de predição utilizados atualmente na área médica. 
    Esta abordagem mostra potencial para melhorar implementações na área de saúde.''')
    
with tab3:
    tab3.markdown('''O objetivo do projeto foi desenvolver um algoritmo de aprendizado de máquina, capaz de realizar a predição da probabilidade 
    de sobrevida de um paciente acometido por determinado tipo de câncer ao longo de 5 anos, após o início do tratamento.\n\n O projeto também visa 
    realizar um estudo comparativo entre os resultados apresentados pelo modelo desenvolvido e a utilização das técnicas utilizadas atualmente 
    pela medicina.''')

with tab4:

    tab4.markdown('### Desempenho médio dos modelos de Inteligência Artificial (IA):')
    
    col1, col2 = tab4.columns(2)

    col1.success('#### ***Accuracy = 66,8%***')
    col1.success('#### ***ROC Curve (AUC) = 73,2%***')
    col1.success('#### ***Recall = 66,9%***')
    
    # Definição das tabs
    tab40, tab41, tab42, tab43, tab44, tab45, tab46, tab47, tab48, tab49 = st.tabs(['6 meses', '12 meses', '18 meses', '24 meses', '30 meses', '36 meses', '42 meses', '48 meses', '54 meses', '60 meses',])

        
    # Resultados para a label 6 meses
    with tab40:
        tab40.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_6meses = [[245,85],[625,1792]]
        plot_confusion_matriz(confusion_matrix_6meses, tab40)
        
        tab40.markdown('### Desempenho do modelo bioestatístico:')
        biomatrix = [[94, 222], [316, 1930]]
        plot_confusion_matriz(biomatrix, tab40)

        tab40.markdown('### Mais sobre o desempenho da Inteligência Artificial:')
        roc_curve_plot(r'curvaROC/y_true_6meses.txt', r'curvaROC/y_score_6meses.txt', tab40)

    # Resultados para a label 12 meses
    with tab41:
        tab41.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_12meses = [[606, 267], [561, 1313]]
        plot_confusion_matriz(confusion_matrix_12meses, tab41)
        
        tab41.markdown('### Desempenho do modelo bioestatístico:')
        biomatrix = [[409, 427], [391, 1335]]
        plot_confusion_matriz(biomatrix, tab41)
        
        tab41.markdown('### Mais sobre o desempenho da Inteligência Artificial:')
        roc_curve_plot(r'curvaROC/y_true_12meses.txt', r'curvaROC/y_score_12meses.txt', tab41)

    # Resultados para a label 18 meses
    with tab42:
        tab42.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_18meses = [[851, 414], [475, 1007]]
        plot_confusion_matriz(confusion_matrix_18meses, tab42)
        roc_curve_plot(r'curvaROC/y_true_18meses.txt', r'curvaROC/y_score_18meses.txt', tab42)
        
    # Resultados para a label 24 meses
    with tab43:
        tab43.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_24meses = [[1014, 503], [417, 820]]
        plot_confusion_matriz(confusion_matrix_24meses, tab43)
        roc_curve_plot(r'curvaROC/y_true_24meses.txt', r'curvaROC/y_score_24meses.txt', tab43)
 
    # Resultados para a label 30 meses
    with tab44:
        tab44.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_30meses = [[1104, 585], [358, 700]]
        plot_confusion_matriz(confusion_matrix_30meses, tab44)
        roc_curve_plot(r'curvaROC/y_true_30meses.txt', r'curvaROC/y_score_30meses.txt', tab44)

    # Resultados para a label 36 meses
    with tab45:
        tab45.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_36meses = [[1219, 609], [310, 616]]
        plot_confusion_matriz(confusion_matrix_36meses, tab45)
        roc_curve_plot(r'curvaROC/y_true_36meses.txt', r'curvaROC/y_score_36meses.txt', tab45)

    # Resultados para a label 42 meses
    with tab46:
        tab46.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_42meses = [[1336, 702], [241, 468]]
        plot_confusion_matriz(confusion_matrix_42meses, tab46)
        roc_curve_plot(r'curvaROC/y_true_42meses.txt', r'curvaROC/y_score_42meses.txt', tab46)

    # Resultados para a label 48 meses
    with tab47:
        tab47.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_48meses = [[1484, 797], [167, 306]]
        plot_confusion_matriz(confusion_matrix_48meses, tab47)
        roc_curve_plot(r'curvaROC/y_true_48meses.txt', r'curvaROC/y_score_48meses.txt', tab47)

    # Resultados para a label 54 meses
    with tab48:
        tab48.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_54meses = [[1568, 873], [112, 194]]
        plot_confusion_matriz(confusion_matrix_54meses, tab48)
        roc_curve_plot(r'curvaROC/y_true_54meses.txt', r'curvaROC/y_score_54meses.txt', tab48)

    # Resultados para a label 60 meses
    with tab49:
        tab49.markdown('### Desempenho da Inteligência Artificial:')
        confusion_matrix_60meses = [[1632, 962], [58, 102]]
        plot_confusion_matriz(confusion_matrix_60meses, tab49)
        roc_curve_plot(r'curvaROC/y_true_60meses.txt', r'curvaROC/y_score_60meses.txt', tab49)

with tab5:
    tab5.markdown('''Podemos concluir que a ferramenta desenvolvida no projeto pode ser usada, por médicos e outros profissionais da área da saúde 
    para realizar a estimativa da resposta de um paciente a determinado tratamento.\n\n O uso da ferramenta permite que médicos realizem simulações de 
    cenários e determinem qual o melhor tipo de tratamento para cada paciente, individualmente.\n\nO algoritmo desenvolvido apresenta resultados de 
    acurácia equivalentes, e em alguns intervalos, melhores, em relação aos métodos utilizados atualmente na área médica.''')

with tab6:

    tab6.markdown("## Apoio da FOSP:")
    # Separação das colunas
    col1, col2 = tab6.columns(2)

    col1.image(perfilstela, caption='Stela Verzinhasse Peres', width=200)
    col2.image(fosp, caption='Fundação Oncocentro de São Paulo - FOSP', width=300)
    botaostela = col1.button("LinkedIn de Stela")
    if botaostela:
        col1.success('https://www.linkedin.com/in/stela-verzinhasse-peres-a1573a9a/')

    tab6.markdown("## Apoio do AC Camargo:")
    
    col1, col2 = tab6.columns(2)
    col1.image(perfilmaria, caption='Maria Paula Curado', width=200)
    col2.image(accamargo, caption='AC Camargo', width=300)