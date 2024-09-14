import sys
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from generate_tables_fake import create_tables_fake

create_tables_fake(2000)

db_path = os.path.join("data", "db_sqllite", "uber_rides.db")
db_uri = f'sqlite:///{db_path}'

engine = create_engine(db_uri)

df_viagem = pd.read_sql_query('SELECT * FROM viagens', con=engine)
df_latlong = pd.read_sql_query('SELECT * FROM latlong_viagens', con=engine)

print(f"viagem: {df_viagem.shape}")
print(f"latlong_viagens: {df_latlong.shape}")

