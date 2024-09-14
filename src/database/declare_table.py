from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Criando o declarative base
Base = declarative_base()

# Definindo o modelo para a tabela de viagens
class Viagem(Base):
    __tablename__ = 'viagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viagem = Column(String, unique=True, nullable=False)
    nome_motorista = Column(String, nullable=False)
    nome_passageiro = Column(String, nullable=False)
    data_viagem = Column(DateTime, nullable=False)
    distancia_km = Column(Float, nullable=False)
    preco_viagem = Column(Float, nullable=False)

# Definindo o modelo para a tabela de latitude e longitude
class LatLongViagem(Base):
    __tablename__ = 'latlong_viagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_viagem = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)