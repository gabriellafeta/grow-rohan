# importando arquivos
import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceExistsError
from io import StringIO
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

#------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide") # Configuração da página larga
#------------------------------------------------------------------------------------------------------
# Uploading data

connection_string = "DefaultEndpointsProtocol=https;AccountName=beesexpansion0001;AccountKey=QBAsqeUnSwNe7hKHJwWrKfH1XE0LpERqc/N/x5jg51pKCvoOgaZw0NvIgxKwyciZ2JxnnjdBbu0b+ASt9jRAaA==;EndpointSuffix=core.windows.net"

if connection_string is None:
    raise Exception("Environment variable AZURE_STORAGE_CONNECTION_STRING is not set.")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = 'expansionbees0001'
container_client = blob_service_client.get_container_client(container_name)

bees_logo = "bezinho.jpg"
blob_client_logo = blob_service_client.get_blob_client(container=container_name, blob=bees_logo)
blob_content_logo = blob_client_logo.download_blob().readall()


col1, col2= st.columns([1, 5])

with col1:
    st.image(blob_content_logo, use_column_width=True)

with col2:
    st.title("GROW KPI's")


#------------------------------------------------------------------------------------------------------

#### Mandar arquivos na pasta DataID para o Azure Blob Storage
##### Tables from Blob
                
blob_name = 'grow_data.csv'
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_content = blob_client.download_blob().content_as_text()
grow_data = StringIO(blob_content)
grow_data_df = pd.read_csv(grow_data)


##### Import Images

bees_logo = "bezinho.jpg"
blob_client_logo = blob_service_client.get_blob_client(container=container_name, blob=bees_logo)
blob_content_logo = blob_client_logo.download_blob().readall()



#------------------------------------------------------------------------------------------------------
## Weekly table

current_timestamp = grow_data_df['day_date'].max()
current_timestamp = datetime.strptime(current_timestamp, '%Y-%m-%d')
current_day = current_timestamp.day
current_month_name = current_timestamp.strftime('%B')

current_timestamp = grow_data_df['day_date'].max()
current_timestamp = datetime.strptime(current_timestamp, '%Y-%m-%d')
current_day = current_timestamp.day
current_month_name = current_timestamp.strftime('%B')


max_week = grow_data_df['week_ref'].max()
current_week = grow_data_df[grow_data_df['week_ref'] == max_week]

hits = current_week.pivot_table(
    index='USER_ID', 
    columns='day_date', 
    values='hits', 
    aggfunc='sum', 
    fill_value=0
)

max_week = grow_data_df['week_ref'].max()
current_week = grow_data_df[grow_data_df['week_ref'] == max_week]


hits = hits.dropna(how='all')
hits = hits.sort_index()

hits = current_week.pivot_table(
    index='USER_ID', 
    columns='day_date', 
    values='hits', 
    aggfunc='sum', 
    fill_value=0
)
#------------------------------------------------------------------------------------------------------
## Styler

def style_df(df, font_size='14px'):

    # Criar o Styler
    styler = df.style.format(na_rep="-", precision=0)\
        .set_table_styles([
            # Estilo do cabeçalho
            {'selector': 'thead th',
             'props': [('background-color', '#1af07e'), ('color', 'black'), ('font-weight', 'bold'), ('text-align', 'center')]},
            # Estilo da fonte e tamanho para toda a tabela
            {'selector': 'table, th, td',
             'props': [('font-size', font_size), ('text-align', 'center')]}, 
            # Removendo linhas de grade
            {'selector': 'table',
             'props': [('border-collapse', 'collapse'), ('border-spacing', '0'), ('border', '0')]}
        ])
    # Ocultar o índice
    styler = styler.hide(axis='index')

    return styler



#------------------------------------------------------------------------------------------------------

hits_main_df = style_df(hits)
hits_html_df = hits_main_df.to_html()

hits_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {hits_html_df}
</div>
"""


#------------------------------------------------------------------------------------------------------

colA_1 = st.columns(1)
colB_1 = st.columns(1)
colB = st.columns(1)




with colA_1[0]:
    st.markdown(f"<i style='font-size: smaller;'>Update up to {current_day - 1}th of {current_month_name}</i>", unsafe_allow_html=True)

with colB[0]:
    st.markdown(hits, unsafe_allow_html=True)










hits = hits.dropna(how='all')
hits = hits.sort_index()

#------------------------------------------------------------------------------------------------------
## Styler

def style_df(df, font_size='14px'):

    # Criar o Styler
    styler = df.style.format(na_rep="-", precision=0)\
        .set_table_styles([
            # Estilo do cabeçalho
            {'selector': 'thead th',
             'props': [('background-color', '#1af07e'), ('color', 'black'), ('font-weight', 'bold'), ('text-align', 'center')]},
            # Estilo da fonte e tamanho para toda a tabela
            {'selector': 'table, th, td',
             'props': [('font-size', font_size), ('text-align', 'center')]}, 
            # Removendo linhas de grade
            {'selector': 'table',
             'props': [('border-collapse', 'collapse'), ('border-spacing', '0'), ('border', '0')]}
        ])
    # Ocultar o índice
    styler = styler.hide(axis='index')

    return styler



#------------------------------------------------------------------------------------------------------

hits_main_df = style_df(hits)
hits_html_df = hits_main_df.to_html()

hits_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {hits_html_df}
</div>
"""


#------------------------------------------------------------------------------------------------------

colA_1 = st.columns(1)
colB_1 = st.columns(1)
colB = st.columns(1)




with colA_1[0]:
    st.markdown(f"<i style='font-size: smaller;'>Update up to {current_day - 1}th of {current_month_name}</i>", unsafe_allow_html=True)

with colB[0]:
    st.markdown(hits, unsafe_allow_html=True)

