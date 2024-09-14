from sqlalchemy import create_engine

# Conectar ao SQLite em memória
engine = create_engine('sqlite:///database_uber.db', echo=True)
print("Conexão com SQLite estabelecida.")

# ORM
from sqlalchemy.orm import declarative_base # Declarative base orm do meu banco de dados
from sqlalchemy import Column, Integer, String # Datetype