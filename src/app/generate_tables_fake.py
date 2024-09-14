import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dir_current = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(dir_current, "..", "gen"))
sys.path.append(os.path.join(dir_current, "..", "database"))

from fake_races_uber import gerar_viagem, gerar_latlong
from declare_table import Base, Viagem, LatLongViagem

# Caminho do diretório de dados
db_path = os.path.join(dir_current, "..", "..", "data", "db_sqllite", "uber_rides.db")
db_uri = f'sqlite:///{db_path}'

# Gerando as tabelas
numero_de_viagens = 1000

# Gerando a tabela de viagens
viagens = [gerar_viagem() for _ in range(numero_de_viagens)]
df_viagens = pd.DataFrame(viagens)

# Gerando a tabela de latitude/longitude
latlong_viagens = []
for viagem in viagens:
    latlong_viagens.extend(gerar_latlong(viagem['id_viagem']))

df_latlong_viagens = pd.DataFrame(latlong_viagens)


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
    print("viagem carregado com sucesso!")
except Exception as e:
    print(f"error {e}")


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
    print("latlong carregado com sucesso!")
except Exception as e:
    print(f"error {e}")

# Commit para salvar os dados no banco de dados
session.commit()

# Fechando a sessão
session.close()
