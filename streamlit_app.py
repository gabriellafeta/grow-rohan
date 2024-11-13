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

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if connection_string is None:
    raise Exception("Environment variable AZURE_STORAGE_CONNECTION_STRING is not set.")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = 'expansionbees0001'
container_client = blob_service_client.get_container_client(container_name)

bees_logo = "bezinho.jpg"
blob_client_logo = blob_service_client.get_blob_client(container=container_name, blob=bees_logo)
blob_content_logo = blob_client_logo.download_blob().readall()


col1, col2 = st.columns([1, 5])

with col1:
    st.image(blob_content_logo, use_column_width=True)

with col2:
    st.title("BEES Sales Leaderboard Report")


#------------------------------------------------------------------------------------------------------

#### Mandar arquivos na pasta DataID para o Azure Blob Storage
##### Tables from Blob
                
blob_name = 'grow_data.csv'
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_content = blob_client.download_blob().content_as_text()
sales_incentive = StringIO(blob_content)
sales_incentive_df = pd.read_csv(sales_incentive)


##### Import Images

bees_logo = "bezinho.jpg"
blob_client_logo = blob_service_client.get_blob_client(container=container_name, blob=bees_logo)
blob_content_logo = blob_client_logo.download_blob().readall()



#------------------------------------------------------------------------------------------------------








#------------------------------------------------------------------------------------------------------









