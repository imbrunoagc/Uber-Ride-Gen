from faker import Faker
import random
import pandas as pd

# Inicializando o faker
fake = Faker()

# Função para gerar viagens
def gerar_viagem():
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
def gerar_latlong(id_viagem):
    origem_lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
    origem_long = round(random.uniform(LONG_MIN, LONG_MAX), 6)
    destino_lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
    destino_long = round(random.uniform(LONG_MIN, LONG_MAX), 6)

    # Retornando 2 linhas, uma para origem e outra para destino
    return [
        {"id_viagem": id_viagem, "lat": origem_lat, "long": origem_long, "tipo": "origem"},
        {"id_viagem": id_viagem, "lat": destino_lat, "long": destino_long, "tipo": "destino"}
    ]

if __name__ == "__main__":
    
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

    # Exibindo as primeiras linhas de ambas as tabelas
    print("Tabela de Viagens:")
    print(df_viagens.head())
    print("\nTabela de Latitude/Longitude:")
    print(df_latlong_viagens.head())
