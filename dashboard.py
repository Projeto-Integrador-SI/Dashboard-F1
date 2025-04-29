#Observação: Eu optei por colocar as variáveis em inglês pra ficar mais facil de entender já que a base de dados está em inglês.

import streamlit as st
import pandas as pd
import plotly.express as px

#Configurações da página
st.set_page_config(
    page_title='Formula 1 | Dashboard',
    page_icon='images/f1_logo.png',
    layout='wide'
)

#Cabeçalho:
col1, col2 = st.columns([1, 10])
with col1:
    st.image('images/f1_logo.png', width=100)
with col2:
    st.markdown('# DASHBOARD', unsafe_allow_html=True)

#Carregando as bases de dados:
df_drivers = pd.read_csv("data/drivers.csv", sep=",")
df_standings = pd.read_csv("data/driver_standings.csv", sep=",")
df_races = pd.read_csv("data/races.csv", sep=",")
df_results = pd.read_csv("data/results.csv", sep=",")
df_constructors = pd.read_csv("data/constructors.csv", sep=",")

#Criando o menu de seleção
df_drivers['full_name'] = df_drivers['forename'] + ' ' + df_drivers['surname']
category = st.sidebar.selectbox("Categoria", ["Piloto", "Equipe"], index=None, placeholder="Selecione uma categoria")

#Coletando as informações do piloto selecionado:
if category == "Piloto":
    driver = st.sidebar.selectbox("Piloto", df_drivers["full_name"].unique(), index=None, placeholder="Selecione um piloto")
    if driver:
        driver_info = df_drivers[df_drivers['full_name'] == driver].iloc[0]
        driver_id = driver_info['driverId']
        driver_nationality = driver_info['nationality']
        
        driver_results = df_results[df_results['driverId'] == driver_id]
        total_points = driver_results['points'].sum()
        
        total_wins = df_results[
            (df_results['driverId'] == driver_id) & 
            (df_results['position'] == '1')
        ].shape[0]
    else:
        total_points = 0
        total_wins = 0
        driver_nationality = '-'
    

#Mostra as informação do piloto:
if category == "Piloto":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Pontos", value=f"{total_points:.0f}")
    with col2:
        st.metric(label="Vitórias", value=total_wins)
    with col3:
        st.metric(label="Nacionalidade", value=driver_nationality)

#Gráfico de pontos por ano do piloto (Alterei para um gráfico de barras):
if category == "Piloto" and driver:
    driver_points_by_year = (
        df_results[df_results['driverId'] == driver_id]
        .merge(df_races[['raceId', 'year']], on='raceId')
        .groupby('year')['points']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        driver_points_by_year,
        x='year',
        y='points',
        title=f'Pontos por ano - {driver}',
    )
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Pontos",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

#Observações: Ainda falta mostrar mais gráficos baseados nos dados dos pilotos e criar a parte das equipes.