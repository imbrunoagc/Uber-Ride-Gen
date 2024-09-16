import sys
import os
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine

import altair as alt

dir_current = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(dir_current, "..", "pipe"))
from generate_tables_fake import create_tables_fake


from configs.settings import setup_page
from pages import home, analytics
from components.sidebar import sidebar
from components.footer import footer

# Configs of page
setup_page()


DONWLOAD_FAKER = False

if DONWLOAD_FAKER:
    data_load = st.text('Loading data...')
    create_tables_fake(3000)
    data_load.text("Done! (using st.cache_data)")

db_path = os.path.join("data", "db_sqllite", "uber_rides.db")
db_uri = f'sqlite:///{db_path}'

engine = create_engine(db_uri)

df_viagem = pd.read_sql_query('SELECT * FROM viagens', con=engine)
df_latlong = pd.read_sql_query('SELECT * FROM latlong_viagens', con=engine)

db_viagens_latlong = df_viagem\
    .merge(df_latlong[
                df_latlong['tipo'] == 'origem'][['id_viagem', 'lat', 'long']],
                    on='id_viagem')\
                        .rename(columns={'long':'lon'})

#######################
# Show Raw Data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df_viagem.shape)
    st.write(df_viagem)


#######################
# Columns header
col1, col2, col3 = st.columns(3)

col1\
    .metric("Number of races",
            df_viagem['id_viagem'].nunique())

total_km = df_viagem['distancia_km'].sum()
col2\
    .metric("Total km driven",f'{total_km:.2f}')

total_price = df_viagem['preco_viagem'].sum()
col3\
    .metric("Total price of races", f'R$ {total_price:.2f}')

df_viagem['data_viagem'] = pd.to_datetime(df_viagem['data_viagem'])

# Criar colunas separadas para ano, mês e hora
df_viagem['date'] = df_viagem['data_viagem'].dt.date
df_viagem['ano'] = df_viagem['data_viagem'].dt.year
df_viagem['mes'] = df_viagem['data_viagem'].dt.month
df_viagem['hora'] = df_viagem['data_viagem'].dt.hour

#######################
col1_filter_date, col2_filter_month, col3_filter_hour = st.columns(3)

list_dates = df_viagem['date'].sort_values(ascending=True).unique()

chosen_date = col1_filter_date.date_input(
    "Choose Your Date",
    value=list_dates[0],
    min_value=list_dates[0],
    max_value=list_dates[-1],
    format="MM.DD.YYYY"
)
#st.write(f"Chosen date: {chosen_date}")

choose_month = col2_filter_month.selectbox(
    "Choose your month",
    options=df_viagem['mes'].unique()
)

choose_hour = col3_filter_hour.selectbox(
    "Choose your hour",
    options=df_viagem['hora'].sort_values(ascending=True).unique()
)



#######################
# text content



#######################
# text content


#######################
# text content



#######################
# text content



#######################
# text content



#######################
# text content



#######################
# text content



#######################
# Footer
footer()