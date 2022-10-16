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


def input_data():
    # Separação da página em um número de colunas
    # col1, col2 = st.columns(2)
    col1 = st.sidebar
    col2 = st.sidebar

    # ['ESCOLARI', 'IDADE', 'SEXO', 'IBGE', 'DIAGPREV', 'BASEDIAG', 'TOPO',
    # 'MORFO', 'EC', 'CIRURGIA', 'RADIO', 'QUIMIO', 'TMO', 'OUTROS', 'RRAS',
    # 'RECNENHUM', 'IBGEATEN', 'HABILIT2', 'TRATDIAG', 'DISTANCIA_CIDADES',
    # 'SOBREVIDA_12MESES']

    ###--------------------------------------DISTANCIA_CIDADES-------------------------------------
    ## 'IBGE' - input relacionado à residência
    ibge = col1.selectbox('Código da cidade de residência do paciente segundo IBGE com digito verificado:', lista_ibge)
    ibge = int(ibge[:7])

    ## 'IBGEATEN' - input relacionado ao atendimento
    ibgeaten = col1.selectbox('Código da cidade de atendimento do paciente segundo IBGE com digito verificado:', lista_ibge)
    ibgeaten = int(ibgeaten[:7])
    
    ###--------------------------------------FEATURES QUE NÃO SÃO PRÉ-PROCESSADAS------------------
    ## 'IDADE' - input do usuário
    idade = col1.number_input('Idade do paciente:', min_value=0, max_value=100, step=1, 
    format='%i')

    ##'SEXO' - input do sexo
    sexo = col1.radio('Código para o sexo do paciente:', ['0 - MASCULINO', '1 - FEMININO'])
    sexo = sexo[0]

    ##'CIRURGIA'
    cirurgia = col2.radio("Tratamento recebido no hospital = CIRURGIA", ['0 - NÃO', '1 - SIM'])
    cirurgia = cirurgia[0]

    ##'RADIO'
    radio = col2.radio("Tratamento recebido no hospital = RADIOTERAPIA", ['0 - NÃO', '1 - SIM'])
    radio = radio[0]

    ##'QUIMIO'
    quimio = col2.radio("Tratamento recebido no hospital = QUIMIOTERAPIA", ['0 - NÃO', '1 - SIM'])
    quimio = quimio[0]

    ##'TMO'
    tmo = col2.radio("Tratamento recebido no hospital = TMO", ['0 - NÃO', '1 - SIM'])
    tmo = tmo[0]

    ##'OUTROS'
    outros = col2.radio("Tratamento recebido no hospital = OUTROS", ['0 - NÃO', '1 - SIM'])
    outros = outros[0]
    
    ##'RECNENHUM'
    recnenhum = col2.radio("Paciente sem recidiva:", ['0 - NÃO', '1 - SIM'])
    recnenhum = recnenhum[0]

    ###-------------------------------------------------TRATDIAG---------------------------
    ## 'DTDIAG' - input da data do diagnóstico
    dtdiag = col1.date_input('Data do diagnóstico:')

    ## 'DTTRAT' - input data do início do tratamento
    dttrat = col1.date_input("Data do início do tratamento")

    ###-------------------------------------------------FEATURES PRÉ-PROCESSADAS-------------------------
    ##'ESCOLARI' - input da escolaridade
    escolari = col1.selectbox('Código para escolaridade do paciente:', ['1 - ANALFABETO', '2 - ENS. FUND.INCOMPLETO', 
    '3 - ENS. FUND.COMPLETO', '4 - ENSINO MÉDIO', '5 - SUPERIOR'])
    escolari = int(escolari[0])

    ##'DIAGPREV' - input sobre diagnóstico e/ou tratamento anteriores 
    diagprev = col1.selectbox('Diagnóstico e tratamento anterior:', ['1 - SEM DIAGNÓSTICO NEM TRATAMENTO', '2 - COM DIAGNÓSTICO E SEM TRATAMENTO'])
    diagprev = int(diagprev[0])

    ##'BASEDIAG' - input do código da base do diagnóstico
    basediag = col1.selectbox('Código da base do diagnóstico:', ['1 - EXAME CLINICO', '2 - RECURSOS AUXILIARES NÃO MICROSCÓPICOS', '3 - CONFIRMAÇÃO MICROSCÓPICA'])
    basediag = int(basediag[0])

    ##'TOPO' - input da código da topografia
    topo = col1.selectbox('Código da topografia (Formato:C999):', ['C019', 'C109', 'C029', 'C021', 'C049', 'C051', 'C099', 'C069', 'C062', 'C091', 'C108', 'C102', 
    'C040', 'C050', 'C060', 'C090', 'C031', 'C059', 'C100', 'C052', 'C041', 'C020', 'C028', 'C103', 'C039', 'C048', 'C004', 'C022', 'C098', 'C009', 'C030', 'C101', 
    'C058', 'C006', 'C023', 'C061', 'C068', 'C005', 'C008', 'C003'])

    ##'MORFO' - input do código da morfologia
    morfo = col1.selectbox('Código da morfologia (Formato:99999):', [80703, 80723, 80733, 80743])
    morfo = int(morfo)
    
    ##'EC' - input do estádio clínico
    ec = col1.selectbox('Estadio clínico:', ['I', 'II', 'III', 'IV', 'IVA', 'IVB', 'IVC'])

    ##'RRAS'
    rras = col2.selectbox("Código RRAS (Redes Regionais de Atenção à Saúde):", ['1 - Grande São Paulo', 
                                                                                '2 - Araçatuba', 
                                                                                '3 - Araraquara', 
                                                                                '4 - Baixada Santista', 
                                                                                '5 - Barretos', 
                                                                                '6 - Bauru', 
                                                                                '7 - Campinas', 
                                                                                '8 - Franca', 
                                                                                '9 - Marília',
                                                                                '10 - Piracicaba', 
                                                                                '11 - Presidente Prudente', 
                                                                                '12 - Registro', 
                                                                                '13 - Ribeirão Preto', 
                                                                                '14 - São João da Boa Vista', 
                                                                                '15 - São José do Rio Preto',  
                                                                                '16 - Sorocaba', 
                                                                                '17 - Taubaté'])
    rras = int(rras[:2])    

    ##'HABILIT2'
    habilit2 = col1.selectbox('Habilitações - Categorias:', ['1 - UNACON', '2 - CACON'])
    habilit2 = int(habilit2[0])

    st.sidebar.warning('Todas as informações foram inseridas corretamente?\n\n Se sim, agora clique em "Prever as probabilidades do paciente sobreviver"')

    # --------------------------------------------- União dos dados em DataFrame ---------------------------------
    # Criação do conjunto de dados do paciente
    input_dict = {
    'ESCOLARI': escolari, 
    'IDADE': idade,
    'SEXO': sexo, 
    'IBGE': ibge,
    'DIAGPREV': diagprev, 
    'BASEDIAG': basediag, 
    'TOPO': topo, 
    'MORFO': morfo, 
    'EC': ec,
    'CIRURGIA': cirurgia, 
    'RADIO': radio, 
    'QUIMIO': quimio, 
    'TMO': tmo, 
    'OUTROS': outros, 
    'RRAS': rras,
    'RECNENHUM': recnenhum,
    'IBGEATEN': ibgeaten,
    'HABILIT2': habilit2,
    'DTDIAG': dtdiag,
    'DTTRAT': dttrat,
    }

    return input_dict

def read_data(input_dict):

    input_df = pd.DataFrame(input_dict, index=[0])

    return input_df

def preprocess(input_df, data):
    # Copia os dados
    df = input_df.copy()
    ###--------------------------------------DIFERENÇA ENTRE DATAS---------------------------------
    df[['DTDIAG', 'DTTRAT']] = df[['DTDIAG', 'DTTRAT']].apply(pd.to_datetime)

    df['TRATDIAG'] = (df.DTTRAT - df.DTDIAG)/np.timedelta64(1, 'D')

    df = df.drop(columns=['DTDIAG', 'DTTRAT'], axis=1)
    
    ###--------------------------------------PRÉ PROCESSAMENTO FEATURES----------------------------
    le_escolari = preprocessing.LabelEncoder()
    le_escolari.fit(data.ESCOLARI)
    
    le_diagprev = preprocessing.LabelEncoder()
    le_diagprev.fit(data.DIAGPREV)
    
    le_basediag = preprocessing.LabelEncoder()
    le_basediag.fit(data.BASEDIAG)
    
    le_topo = preprocessing.LabelEncoder()
    le_topo.fit(data.TOPO)
    
    le_morfo = preprocessing.LabelEncoder()
    le_morfo.fit(data.MORFO)
    
    le_ec = preprocessing.LabelEncoder()
    le_ec.fit(data.EC)
    
    le_habilit2 = preprocessing.LabelEncoder()
    le_habilit2.fit(data.HABILIT2)

    df.ESCOLARI = le_escolari.transform(df.ESCOLARI)
    df.DIAGPREV = le_diagprev.transform(df.DIAGPREV)
    df.BASEDIAG = le_basediag.transform(df.BASEDIAG)
    df.TOPO     = le_topo.transform(df.TOPO)
    df.MORFO    = le_morfo.transform(df.MORFO)
    df.EC       = le_ec.transform(df.EC)
    df.HABILIT2 = le_habilit2.transform(df.HABILIT2)

    df = df[['ESCOLARI', 'IDADE', 'SEXO', 'DIAGPREV', 'BASEDIAG', 'TOPO', 'MORFO', 'EC', 
    'CIRURGIA', 'RADIO', 'QUIMIO', 'TMO', 'OUTROS', 'RRAS', 'RECNENHUM', 'HABILIT2', 
    'TRATDIAG', 'DISTANCIA_CIDADES']]
    
    return df


# Lista com as cidades e seus códigos do IBGE
lista_ibge = []
# open file and read the content in a list
with open(r'lista_ibge.txt', 'r') as fp:
    for line in fp:
        # remove linebreak from a current name
        # linebreak is the last character of each line
        x = line[:-1]

        # add current item to the list
        lista_ibge.append(x)

##--------------------------------------CARREGAR MODELOS-------------------------------------------
def carrega_modelos():

    with open('modelos/sobrevida_6meses.pickle' , 'rb') as f:
        model1 = pickle.load(f)
    
    with open('modelos/sobrevida_12meses.pickle' , 'rb') as f:
        model2 = pickle.load(f)

    with open('modelos/sobrevida_18meses.pickle' , 'rb') as f:
        model3 = pickle.load(f)

    with open('modelos/sobrevida_24meses.pickle' , 'rb') as f:
        model4 = pickle.load(f)

    with open('modelos/sobrevida_30meses.pickle' , 'rb') as f:
        model5 = pickle.load(f)

    with open('modelos/sobrevida_36meses.pickle' , 'rb') as f:
        model6 = pickle.load(f)

    with open('modelos/sobrevida_42meses.pickle' , 'rb') as f:
        model7 = pickle.load(f)

    with open('modelos/sobrevida_48meses.pickle' , 'rb') as f:
        model8 = pickle.load(f)

    with open('modelos/sobrevida_54meses.pickle' , 'rb') as f:
        model9 = pickle.load(f)

    with open('modelos/sobrevida_60meses.pickle' , 'rb') as f:
        model10 = pickle.load(f)

    return  model1, model2, model3, model4, model5, model6, model7, model8, model9, model10

# Uso da função carrega modelos
model1, model2, model3, model4, model5, model6, model7, model8, model9, model10 = carrega_modelos()

##--------------------------------------PREPARA DADOS DE IBGE PARA CALCULAR DISTANCIA-------------------------------------------
ibge_df = pd.read_csv('dados/ibge.csv')

ibge_df['GEOLOC'] = list(zip(ibge_df.latitude, ibge_df.longitude))
    
IBGE = ibge_df[['codigo_ibge', 'GEOLOC']].copy()
IBGE.columns = ['IBGE', 'GEOLOCALIZACAO']

IBGEATEN = ibge_df[['codigo_ibge', 'GEOLOC']].copy()
IBGEATEN.columns = ['IBGEATEN', 'GEOLOCALIZACAO_ATEN']


##--------------------------------------PREPARA DADOS PARA PRÉ-PROCESSAMENTO-------------------------------------------
dfb = pd.read_csv('dados/cancer_boca.csv', index_col='Unnamed: 0')
dfo = pd.read_csv('dados/cancer_orofaringe.csv', index_col='Unnamed: 0')
data = pd.concat([dfb, dfo], ignore_index=True)

#---------------------------------------RODAR O APP-----------------------------------------------
image = Image.open('fotos/imt.jpeg')
st.image(image, use_column_width=False)

add_selectbox = st.sidebar.selectbox(
    'Como gostaria de fazer a predição?',
    ('Individual', 'Grupo')
)

if add_selectbox == 'Individual':

    # Leitura dos dados no app
    input_dict = input_data()

    if st.button("Prever as probabilidades do paciente sobreviver"):
        
        input_df = read_data(input_dict=input_dict)
        # Adiciona os dados de geolocalização
        input_df = input_df.merge(IBGE, how='left', on='IBGE')
        input_df = input_df.merge(IBGEATEN, how='left', on='IBGEATEN')
        # Cálcula a distância entre as cidades
        distancias = []
        for i in range(input_df.shape[0]):
            geo       = input_df.iloc[i].GEOLOCALIZACAO
            geo_aten  = input_df.iloc[i].GEOLOCALIZACAO_ATEN
            dist = geodesic(geo, geo_aten).km
            distancias.append(dist)
        input_df['DISTANCIA_CIDADES'] = distancias
        # Retira as colunas que não são utilizadas
        input_df = input_df.drop(['GEOLOCALIZACAO', 'GEOLOCALIZACAO_ATEN',
        'IBGE', 'IBGEATEN'], axis=1)

        # Processa os dados
        input_df = preprocess(input_df=input_df, data=data)
        #---------------------------------PREDIÇÃO DOS MODELOS----------------------------------------------
        prediction1 = model1.predict_proba(input_df)[0][1]        
        prediction2 = model2.predict_proba(input_df)[0][1]        
        prediction3 = model3.predict_proba(input_df)[0][1]        
        prediction4 = model4.predict_proba(input_df)[0][1] 
        prediction5 = model5.predict_proba(input_df)[0][1]        
        prediction6 = model6.predict_proba(input_df)[0][1]        
        prediction7 = model7.predict_proba(input_df)[0][1]        
        prediction8 = model8.predict_proba(input_df)[0][1]      
        prediction9 = model9.predict_proba(input_df)[0][1] 
        prediction10 = model10.predict_proba(input_df)[0][1]
        
        output = '' + '##### 6 meses: {:.2f}%\n'.format(prediction1*100)
        output += '##### 12 meses: {:.2f}%\n'.format(prediction2*100)
        output += '##### 18 meses: {:.2f}%\n'.format(prediction3*100)
        output += '##### 24 meses: {:.2f}%\n'.format(prediction4*100)
        output += '##### 30 meses: {:.2f}%\n'.format(prediction5*100)
        output2 = '' + '##### 36 meses: {:.2f}%\n'.format(prediction6*100)
        output2 += '##### 42 meses: {:.2f}%\n'.format(prediction7*100)
        output2 += '##### 48 meses: {:.2f}%\n'.format(prediction8*100)
        output2 += '##### 54 meses: {:.2f}%\n'.format(prediction9*100)
        output2 += '##### 60 meses: {:.2f}%\n'.format(prediction10*100)

        esq, dir = st.columns(2)
        
        esq.success(output)
        dir.success(output2)

        # Dados para o gráfico
        x = ['6 meses','12 meses','18 meses','24 meses','30 meses',
            '36 meses','42 meses','48 meses','54 meses','60 meses']
        x_rev = x[::-1]

        y1 = [prediction1, prediction2, prediction3, prediction4, prediction5, prediction6, prediction7, prediction8, prediction9, prediction10]

        y1_upper = []
        y1_lower = []
        for pred in y1:
            y1_upper.append(float(pred) + 0.05)
            y1_lower.append(float(pred) - 0.05)
        y1_lower = y1_lower[::-1]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x+x_rev,
            y=y1_upper+y1_lower,
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
            name='Faixa de erro',
            line_shape='spline'
        ))
        fig.add_trace(go.Scatter(
            x=x, y=y1,
            line_color='rgb(0,100,80)',
            name='Probabilidade de sobrevivência do paciente',
            line_shape='spline'
        ))

        fig.update_traces(mode='lines+markers+text')

        fig.update_layout(xaxis_title='Tempo após previsão', 
        yaxis_title='Probabilidade do paciente sobreviver', 
        title='Probabilidade do paciente sobreviver ao decorrer dos meses')
        
        st.plotly_chart(fig, use_container_width=True)

elif add_selectbox == 'Grupo':
    
    file_upload = st.file_uploader('Upload do arquivo CSV para predições', type=['csv'])

    if file_upload is not None:
        # Leitura do batch
        data = pd.read_csv(file_upload)
        # Predições do batch
        prediction1 = model2.predict_proba(data)
        st.write(prediction1)