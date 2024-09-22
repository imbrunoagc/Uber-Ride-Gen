# Uber-Ride-Gen

## Objetivo
O **Uber-Ride-Gen** é um projeto criado para gerar dados falsos (faker) de corridas de Uber e visualizá-los graficamente através de uma aplicação Streamlit. Este projeto é útil para simular e analisar dados de transporte de passageiros em diferentes cenários.

## Stack

[![My Skills](https://skillicons.dev/icons?i=vscode,python,sqlite,github,faker,streamlit&perline=7)](https://skillicons.dev)

## Estrutura do Projeto
O projeto é dividido em três tabelas principais:

### Tabela 1: `viagens`
Contém informações detalhadas sobre cada corrida gerada.

| Coluna          | Descrição                      |
|-----------------|--------------------------------|
| `id_viagem`     | Identificador único da viagem. |
| `nome_motorista`| Nome do motorista.             |
| `nome_passageiro`| Nome do passageiro.           |
| `data_viagem`   | Data e hora da viagem.         |
| `distancia_km`  | Distância percorrida (em km).  |
| `preco_viagem`  | Preço da corrida.              |

### Tabela 2: `latlong_viagens`
Armazena as coordenadas geográficas relacionadas às viagens, permitindo o cruzamento entre origem e destino.

| Coluna          | Descrição                                      |
|-----------------|------------------------------------------------|
| `id_viagem`     | Identificador da viagem (para cruzamento).      |
| `lat`           | Latitude (origem ou destino).                  |
| `long`          | Longitude (origem ou destino).                 |
| `tipo`          | Tipo da coordenada: "origem" ou "destino".     |

### Tabela 3: `feedback_viagens`
Armazena os feedbacks dos usuários sobre as viagens, incluindo uma classificação numérica e comentários textuais.

| Coluna          | Descrição                                         |
|-----------------|---------------------------------------------------|
| `id_viagem`     | Identificador da viagem (para cruzamento).        |
| `classificacao` | Classificação da viagem (números de 1 a 5, float).|
| `feedback`      | Longitude (origem ou destino).                    |

## Funcionalidades
1. **Geração de Dados Faker**: Utiliza a biblioteca Faker para criar dados realistas de corridas de Uber, incluindo nomes de motoristas, passageiros, preços e distâncias.
2. **Geolocalização**: Geração de coordenadas de latitude e longitude limitadas ao Brasil para origem e destino das viagens.
3. **Visualizações Gráficas**: Através do Streamlit, são geradas visualizações interativas dos dados de viagem, como gráficos de preço médio por distância, corridas por dia, e mapa das rotas.

## Requisitos
- **Python 3.10.8+**
- **Bibliotecas**:
  - `poetry`
  - `pandas`
  - `faker`
  - `streamlit`
  - `matplotlib`
  - `geopy` (para manipulação de coordenadas geográficas)

## Como instalar o projeto
1. Clone o repositório:
```bash
git clone https://github.com/imbrunoagc/Uber-Ride-Gen.git
```

2. Instale o Poetry em sua máquina:
```bash
pip install poetry
```

3. Ative o ambiente virtual venv
```bash
poetry shell
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como executar a geração de dados Fake e Armazenamento em SQLite
1. Execute o ETL:
```bash
poetry run python src/pipe/generate_tables_fake.py
```

## Como executar o StreamLit
1. Execute o Streamlit:
```bash
poetry run streamlit run src/app/app.py
```