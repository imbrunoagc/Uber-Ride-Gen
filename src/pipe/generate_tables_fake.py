import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import streamlit as st

dir_current = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(dir_current, "..", "gen"))
sys.path.append(os.path.join(dir_current, "..", "database"))

from fake_races_uber import gerar_viagem, gerar_latlong, gerar_feedback
from declare_table import Base, Viagem, LatLongViagem, FeedbackViagem

# Caminho do diretório de dados
db_path = os.path.join(dir_current, "..", "..", "data", "db_sqllite", "uber_rides.db")
db_uri = f'sqlite:///{db_path}'

@st.cache_data()
def create_tables_fake(
    numero_de_viagens:int=3000,
    db_uri:str=db_uri
    ) -> None:

    # Gerando as tabelas
    ##numero_de_viagens = 1000

    # Gerando a tabela de viagens
    viagens = [gerar_viagem() for _ in range(numero_de_viagens)]
    df_viagens = pd.DataFrame(viagens)

    # Gerando a tabela de latitude/longitude
    latlong_viagens = []
    for viagem in viagens:
        latlong_viagens.extend(gerar_latlong(viagem['id_viagem']))

    df_latlong_viagens = pd.DataFrame(latlong_viagens)

    
    classificacao = []
    for viagem in viagens:
        classificacao.extend(gerar_feedback(viagem['id_viagem']))
        
    df_feedback = pd.DataFrame(classificacao)

    # Criando o banco de dados SQLite em memória (ou em arquivo se preferir)
    engine = create_engine(db_uri, echo=False)

    # Criando as tabelas no banco de dados
    Base.metadata.create_all(engine)

    # Criando uma sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Carregando os dados das viagens para o SQLite
    for index, row in df_viagens.iterrows():
        viagem = Viagem(
            id_viagem=row['id_viagem'],
            nome_motorista=row['nome_motorista'],
            nome_passageiro=row['nome_passageiro'],
            data_viagem=row['data_viagem'],
            distancia_km=row['distancia_km'],
            preco_viagem=row['preco_viagem']
        )
        try:
            session.add(viagem)
        except Exception as e:
            print(f"error {e}")
    print(f"viagem carregado com sucesso, total de linhas: {index+1}")


    # Carregando os dados de latitude e longitude para o SQLite
    for index, row in df_latlong_viagens.iterrows():
        latlong = LatLongViagem(
            id_viagem=row['id_viagem'],
            lat=row['lat'],
            long=row['long'],
            tipo=row['tipo']
        )
        try:
            session.add(latlong)
        except Exception as e:
            print(f"error {e}")
    print(f"latlong carregado com sucesso, total de linhas: {index+1}")



    for index, row in df_feedback.iterrows():
        feedback = FeedbackViagem(
            id_viagem=row['id_viagem'],
            classificacao=row['rating'],
            feedback=row['feedback']
        )
        try:
            session.add(feedback)
        except Exception as e:
            print(f"error {e}")
    print(f"Feedback carregado com sucesso, total de linhas: {index+1}")
    
    # Commit para salvar os dados no banco de dados
    session.commit()

    # Fechando a sessão
    session.close()
    
    print(f"db gravado no caminho: {db_uri}")

if __name__ == "__main__":
    create_tables_fake(10000)