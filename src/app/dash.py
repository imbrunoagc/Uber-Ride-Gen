import sys
import os
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine

from generate_tables_fake import create_tables_fake

data_load_state = st.text('Loading data...')
create_tables_fake(2000)
data_load_state.text("Done! (using st.cache_data)")

db_path = os.path.join("data", "db_sqllite", "uber_rides.db")
db_uri = f'sqlite:///{db_path}'

engine = create_engine(db_uri)

#df_viagem = pd.read_sql_query('SELECT * FROM viagens', con=engine)
#df_latlong = pd.read_sql_query('SELECT * FROM latlong_viagens', con=engine)

db_viagens_latlong = pd.read_sql_query(
    '''
SELECT 
    v.id,
    v.id_viagem,
    v.nome_motorista,
    v.nome_passageiro,
    STRFTIME('%Y-%m-%d %H:%M:%S', v.data_viagem) AS data_viagem,
    v.distancia_km,
    v.preco_viagem,
    lv.tipo,
    lv.lat,
    lv.long as lon
FROM
    viagens v
INNER JOIN 
    latlong_viagens lv ON v.id_viagem = lv.id_viagem

    ''', con=engine
)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(db_viagens_latlong)

DATE_COLUMN = 'data_viagem'
db_viagens_latlong[DATE_COLUMN] = pd.to_datetime(db_viagens_latlong[DATE_COLUMN])

st.subheader('Number of races by hour')
hist_values = np.histogram(db_viagens_latlong[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 24, 12)
filtered_data = db_viagens_latlong[db_viagens_latlong[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all races at %s:00' % hour_to_filter)
st.map(filtered_data)

