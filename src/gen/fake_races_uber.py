from faker import Faker
import random
import pandas as pd
from typing import Dict, List, Union, Any
from datetime import datetime

from parameters import positive_feedbacks, neutral_feedbacks, negative_feedbacks

# Inicializando o faker
fake = Faker('pt_BR')

# Função para gerar viagens
def gerar_viagem() -> Dict[str, Any]:
    id_viagem = fake.uuid4()
    return {
        "id_viagem": id_viagem,
        "nome_motorista": fake.name(),
        "nome_passageiro": fake.name(),
        "data_viagem": fake.date_time_this_year(),
        "distancia_km": round(random.uniform(1, 30), 2),
        "preco_viagem": round(random.uniform(5, 100), 2)
    }

# Limites geográficos aproximados para o Brasil
LAT_MIN, LAT_MAX = -33.75, 5.25
LONG_MIN, LONG_MAX = -73.99, -34.79

# Função para gerar latitudes e longitudes associadas às viagens
def gerar_latlong(id_viagem: str) -> List[Dict[str, Union[str, float]]]:
    origem_lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
    origem_long = round(random.uniform(LONG_MIN, LONG_MAX), 6)
    destino_lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
    destino_long = round(random.uniform(LONG_MIN, LONG_MAX), 6)

    # Retornando 2 linhas, uma para origem e outra para destino
    return [
        {"id_viagem": id_viagem, "lat": origem_lat, "long": origem_long, "tipo": "origem"},
        {"id_viagem": id_viagem, "lat": destino_lat, "long": destino_long, "tipo": "destino"}
    ]


def gerar_feedback(id_viagem: str):
    rating = round(random.uniform(1, 5), 1)  # Nota de 1 a 5, com uma casa decimal
    
    # Seleciona feedback com base na avaliação
    if rating >= 4:
        feedback = random.choice(positive_feedbacks)
    elif rating >= 3:
        feedback = random.choice(neutral_feedbacks)
    else:
        feedback = random.choice(negative_feedbacks)
        
    return [
        {"id_viagem": id_viagem, "rating": rating, "feedback": feedback}
    ]
    
if __name__ == "__main__":
    
    # Gerando as tabelas
    numero_de_viagens = 1000

    # Gerando a tabela de viagens
    viagens = [gerar_viagem() for _ in range(numero_de_viagens)]
    df_viagens = pd.DataFrame(viagens)
    df_viagens.to_excel("data\\db_excel\\viagens.xlsx", index=False)

    # Gerando a tabela de latitude/longitude
    latlong_viagens = []
    for viagem in viagens:
        latlong_viagens.extend(gerar_latlong(viagem['id_viagem']))

    df_latlong_viagens = pd.DataFrame(latlong_viagens)
    df_latlong_viagens.to_excel("data\\db_excel\\latlong_viagens.xlsx", index=False)

    classificacao = []
    for viagem in viagens:
        classificacao.extend(gerar_feedback(viagem['id_viagem']))
        
    df_classificacao_estrelas = pd.DataFrame(classificacao)
    df_classificacao_estrelas.to_excel("data\\db_excel\\classificacao.xlsx", index=False)

    # Exibindo as primeiras linhas de ambas as tabelas
    print("Tabela de Viagens:")
    print(df_viagens.head())
    print("\nTabela de Latitude/Longitude:")
    print(df_latlong_viagens.shape)
    print(df_latlong_viagens.columns)
