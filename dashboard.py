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

#Carregando as bades de dados:
df_drivers = pd.read_csv("data/drivers.csv", sep=",")
df_standings = pd.read_csv("data/driver_standings.csv", sep=",")
df_races = pd.read_csv("data/races.csv", sep=",")
df_results = pd.read_csv("data/results.csv", sep=",")

#Selecionando o piloto:
df_drivers['full_name'] = df_drivers['forename'] + ' ' + df_drivers['surname']
driver = st.sidebar.selectbox("Piloto", df_drivers["full_name"].unique(), index=None, placeholder="Selecione um piloto")

#Calculando o total de pontos:
if driver:
    driver_id = df_drivers[df_drivers['full_name'] == driver]['driverId'].iloc[0]
    driver_results = df_results[df_results['driverId'] == driver_id]
    total_points = driver_results['points'].sum()
else:
    total_points = 0

#Dados do piloto(Por enquanto só o total de pontos):
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total de Pontos", value=f"{total_points:.0f}")

#Gráfico de pontos por ano do piloto:
if driver:
    driver_points_by_year = (
        #Filtro para pegar apenas o ano em que o piloto correu:
        df_results[df_results['driverId'] == driver_id]
        #Coleta o ano da corrida:
        .merge(df_races[['raceId', 'year']], on='raceId')
        #Agrupa os dados por ano e soma os pontos das corridas:
        .groupby('year')['points']
        .sum()
        .reset_index()
    )

    #Criação do gráfico usando Plotly Express:
    fig = px.line(
        driver_points_by_year,
        x='year',
        y='points',
        title=f'Pontos por ano - {driver}',
        markers=True
    )
    #Atualização do gráfico:
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Pontos",
        showlegend=False
    )
    
    #Exibição do gráfico usando Streamlit:
    st.plotly_chart(fig, use_container_width=True)
