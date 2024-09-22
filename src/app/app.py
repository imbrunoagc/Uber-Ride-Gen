import sys
import os
import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine
from datetime import datetime, time
import altair as alt

dir_current = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(dir_current, "..", "pipe"))
from generate_tables_fake import create_tables_fake


from configs.settings import setup_page
#from components.sidebar import sidebar
from components.footer import footer

# Configs of page
setup_page()

tab1, tab2 = st.tabs(["Rides", "Feedbacks"])

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
df_feedbacks = pd.read_sql_query('SELECT * FROM feedback_viagens', con=engine)

with tab1:

    db_viagens_latlong = df_viagem\
        .merge(df_latlong[
                    df_latlong['tipo'] == 'origem'][['id_viagem', 'lat', 'long']],
                        on='id_viagem')\
                            .rename(columns={'long':'lon'}).\
                                merge(df_feedbacks, on='id_viagem', how='left')

    #######################
    # Show Raw Data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df_viagem.shape)
        st.write(df_viagem)

    #######################
    # Columns header - Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Number of races",
        f"{df_viagem['id_viagem'].nunique():,.0f}".replace(",", ".")
    )

    total_km = df_viagem['distancia_km'].sum()
    col2\
        .metric("Total km driven",f'{total_km:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    total_price = df_viagem['preco_viagem'].sum()
    col3\
        .metric("Total price of races", f'R$ {total_price:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."))

    #######################
    # little transformations - DateTime

    df_viagem['data_viagem'] = pd.to_datetime(df_viagem['data_viagem'])
    df_viagem = df_viagem.sort_values(['data_viagem'], ascending=True)

    # Criar colunas separadas para ano, mês e hora
    df_viagem['date'] = df_viagem['data_viagem'].dt.date
    df_viagem['ano'] = df_viagem['data_viagem'].dt.year
    df_viagem['mes'] = df_viagem['data_viagem'].dt.month
    df_viagem['hora'] = df_viagem['data_viagem'].dt.hour

    #######################
    # Columns filter
    col1_filter_date, col2_filter_hour = st.columns(2)

    list_dates = df_viagem['date'].sort_values(ascending=True).unique()

    chosen_date = col1_filter_date.date_input(
        "Choose Your Date",
        value=list_dates[0],
        min_value=list_dates[0],
        max_value=list_dates[-1],
        format="MM.DD.YYYY"
    )

    # Slider para escolher intervalo de tempo
    appointment = col2_filter_hour.select_slider(
        "Choose Your Date and Hour:", 
        options=df_viagem['data_viagem'],
        value=(df_viagem['data_viagem'].min(), df_viagem['data_viagem'].max()),
        format_func=lambda x: x.strftime('%Y-%m-%d %H:%M')
    )

    start_datetime = appointment[0]
    end_datetime = appointment[1]


    #######################
    # Visual Graphics

    with col1_filter_date:
        agg_hour = df_viagem[
            (df_viagem['date'] == chosen_date)
            ].groupby('hora').agg(
            count_races=('id_viagem', 'count')
        ).reset_index()

        st.line_chart(data=agg_hour, x='hora', y=['count_races'])


    with col2_filter_hour:
        agg_month = df_viagem[
            (df_viagem['data_viagem'] >= start_datetime) & 
            (df_viagem['data_viagem'] <= end_datetime)
            ].groupby('mes').agg(
            count_races=('id_viagem', 'nunique')
        ).reset_index()

        st.bar_chart(data=agg_month, x='mes', y='count_races', x_label='Horarios de corrida', y_label='Quantidade de corridas', stack='layered')

    #######################
    # text content
        # Função para converter a classificação em estrelas
    def estrelas(classificacao):
        estrelas_cheias = int(classificacao)  # Número de estrelas cheias
        meia_estrela = 0 if classificacao % 1 == 0 else 1  # Verificar se há meia estrela
        estrelas_vazias = 5 - estrelas_cheias - meia_estrela  # Estrelas vazias
        
        return '⭐' * estrelas_cheias + '✨' * meia_estrela + '☆' * estrelas_vazias


    def generate_stars_to_dataframe(row) -> pd.DataFrame:
            return estrelas(row)

    with col1_filter_date:
        df_feedbacks_with_stars = df_feedbacks.copy()

        df_feedbacks_with_stars['stars'] = df_feedbacks_with_stars['classificacao'].apply(generate_stars_to_dataframe)
        agg_feedbacks = df_feedbacks_with_stars.groupby('stars')['classificacao']

        media_agg_feedbacks = agg_feedbacks.mean().reset_index(name='mean')
        mediana_agg_feedbacks = agg_feedbacks.median().reset_index(name='median')
        minimo_agg_feedbacks = agg_feedbacks.min().reset_index(name='min')
        maximo_agg_feedbacks = agg_feedbacks.max().reset_index(name='max')
        std_agg_feedbacks = agg_feedbacks.std().reset_index(name='std')
        contagem_agg_feedbacks = agg_feedbacks.count().reset_index(name='count')

        # Agora, vamos concatenar os DataFrames inteiros, alinhando pela coluna 'stars'
        medidas_feedback = pd.concat([
            media_agg_feedbacks,
            mediana_agg_feedbacks['median'],
            minimo_agg_feedbacks['min'],
            maximo_agg_feedbacks['max'],
            std_agg_feedbacks['std'],
            contagem_agg_feedbacks['count']
        ], axis=1)

        st.table(medidas_feedback)

    with col2_filter_hour:
        
        # criar um grafico de palavras no streamlit
        words_feedbacks = df_feedbacks_with_stars['feedback']

        #st.write(wc)
        # st.image(wc.to_array())
































with tab2:

    # Função para mostrar feedbacks limitados
    def mostrar_mais_feedbacks(df, contagem):
        # Exibir os feedbacks com as estrelas
        st.write("Feedbacks com classificação em estrelas:")
        
        # Validar se a contagem não excede o número de feedbacks
        if contagem > df.shape[0]:
            st.error("O número de linhas informado é maior que o número de feedbacks registrados.")
            return
        
        # Iterar sobre o DataFrame e exibir feedbacks limitados
        for i, row in df.iterrows():
            if i == contagem:
                break
            st.write(f"Viagem {row['id_viagem']} - Classificação: {row['classificacao']}")
            st.write(f"{estrelas(row['classificacao'])}")
            st.write(f"Feedback: {row['feedback']}")
            st.write("---")

    # Entrada para o número de feedbacks desejado
    number_feedbacks = st.number_input("Insira o número de feedbacks desejados:", min_value=1, max_value=df_feedbacks.shape[0])

    # Mostrar os feedbacks com base na entrada do usuário
    mostrar_mais_feedbacks(df_feedbacks, int(number_feedbacks))

# Footer
footer()