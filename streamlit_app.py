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

# Convert the string to a datetime object
current_timestamp = pd.to_datetime(current_timestamp, format='%Y-%m-%d')

# Add one day using pd.Timedelta
current_timestamp = current_timestamp + pd.Timedelta(days=1)

# Extract the day and month name
current_day = current_timestamp.day
current_month_name = current_timestamp.strftime('%B')

current_timestamp = grow_data_df['day_date'].max()
current_timestamp = datetime.strptime(current_timestamp, '%Y-%m-%d')
current_day = current_timestamp.day
current_month_name = current_timestamp.strftime('%B')


max_month = grow_data_df['month_ref'].max()
grow_data_df = grow_data_df[grow_data_df['month_ref'] == max_month]

email_to_name = {
    "ocsicaviteteleseller2@gmail.com": "Khya",
    "ocsicaviteteleseller3@gmail.com": "Laarnie",
    "ocsicaviteteleseller4@gmail.com": "Belle",
    "ocsicaviteteleseller6@gmail.com": "Andrea",
    "ocsicaviteteleseller@gmail.com": "Patrice"
}

grow_data_df['Agent'] = grow_data_df['USER_ID'].map(email_to_name)


## max_week = grow_data_df['week_ref'].max()
## current_week = grow_data_df[grow_data_df['week_ref'] == max_week]

hits = grow_data_df.pivot_table(
    index='Agent', 
    columns='day_date', 
    values='hits', 
    aggfunc='sum', 
    fill_value=0
)

hits = hits.dropna(how='all')
hits = hits.sort_index()

hits_week = grow_data_df.pivot_table(
    index='Agent', 
    columns='Week', 
    values='hits', 
    aggfunc='sum', 
    fill_value=0
)

hits_week = hits_week.dropna(how='all')
hits_week = hits_week.sort_index()


taken = grow_data_df.pivot_table(
    index='Agent', 
    columns='day_date', 
    values='order_taken', 
    aggfunc='sum', 
    fill_value=0
)

max_week = grow_data_df['week_ref'].max()
current_week = grow_data_df[grow_data_df['week_ref'] == max_week]


taken = taken.dropna(how='all')
taken = taken.sort_index()

taken_week = grow_data_df.pivot_table(
    index='Agent', 
    columns='Week', 
    values='order_taken', 
    aggfunc='sum', 
    fill_value=0
)

taken_week = taken_week.dropna(how='all')
taken_week = taken_week.sort_index()

influenced = grow_data_df.pivot_table(
    index='Agent', 
    columns='day_date', 
    values='orders_influenced', 
    aggfunc='sum', 
    fill_value=0
)

max_week = grow_data_df['week_ref'].max()
current_week = grow_data_df[grow_data_df['week_ref'] == max_week]


influenced = influenced.dropna(how='all')
influenced = influenced.sort_index()


influenced_week = grow_data_df.pivot_table(
    index='Agent', 
    columns='Week', 
    values='orders_influenced', 
    aggfunc='sum', 
    fill_value=0
)

influenced_week = influenced_week.dropna(how='all')
influenced_week = influenced_week.sort_index()





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

    return styler



#------------------------------------------------------------------------------------------------------

hits_main_df = style_df(hits)
hits_html_df = hits_main_df.to_html()

hits_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {hits_html_df}
</div>
"""
title_html_hits = """
<h1 style="font-size: 18px; font-weight: bold; text-align: center;">HITS</h1>
"""
title_html_hits_day = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Daily</h1>
"""

hits_week_df = style_df(hits_week)
hits_week_html_df = hits_week_df.to_html()

hits_week_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {hits_week_html_df}
</div>
"""
title_html_hits_week = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Weekly</h1>
"""
#---------------------------------------------------------------------------------------------------------
taken_main_df = style_df(taken)
taken_html_df = taken_main_df.to_html()

taken_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {taken_html_df}
</div>
"""
title_html_taken = """
<h1 style="font-size: 18px; font-weight: bold; text-align: center;">ORDERS TAKEN</h1>
"""

taken_week_df = style_df(taken_week)
taken_html_df_week = taken_week_df.to_html()

taken_week_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {taken_html_df_week}
</div>
"""
title_html_taken_week = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Weekly</h1>
"""
title_html_taken_day = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Daily</h1>
"""
#---------------------------------------------------------------------------------------------------------

influenced_main_df = style_df(influenced)
influenced_html_df = influenced_main_df.to_html()

influenced_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {influenced_html_df}
</div>
"""
title_html_influenced = """
<h1 style="font-size: 18px; font-weight: bold; text-align: center;">ORDERS INFLUENCED</h1>
"""

influenced_main_df_week = style_df(influenced_week)
influenced_html_df_week = influenced_main_df_week.to_html()

influenced_html_week = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    {influenced_html_df_week}
</div>
"""
title_html_influenced_week = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Weekly</h1>
"""
title_html_influenced_day = """
<h1 style="font-size: 18px; font-weight: bold; text-align: left;">Daily</h1>
"""


#------------------------------------------------------------------------------------------------------

colA_1 = st.columns(1)
colB = st.columns(1)
colC = st.columns(1)
colD = st.columns(1)




with colA_1[0]:
    st.markdown(f"<i style='font-size: smaller;'>Update up to {current_day}th of {current_month_name}</i>", unsafe_allow_html=True)

with colB[0]:
    st.markdown(title_html_hits, unsafe_allow_html=True)
    st.markdown(title_html_hits_day, unsafe_allow_html=True)
    st.markdown(hits_html, unsafe_allow_html=True)
    st.markdown(title_html_hits_week, unsafe_allow_html=True)
    st.markdown(hits_week_html, unsafe_allow_html=True)

with colC[0]:
    st.markdown(title_html_taken, unsafe_allow_html=True)
    st.markdown(title_html_taken_day, unsafe_allow_html=True)
    st.markdown(taken_html, unsafe_allow_html=True)
    st.markdown(title_html_taken_week, unsafe_allow_html=True)
    st.markdown(taken_week_html, unsafe_allow_html=True)

with colD[0]:
    st.markdown(title_html_influenced, unsafe_allow_html=True)
    st.markdown(title_html_influenced_day, unsafe_allow_html=True)
    st.markdown(influenced_html, unsafe_allow_html=True)
    st.markdown(title_html_influenced_week, unsafe_allow_html=True)
    st.markdown(influenced_html_week, unsafe_allow_html=True)
