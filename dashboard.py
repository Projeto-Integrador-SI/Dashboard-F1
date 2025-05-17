#Observação: Eu optei por colocar as variáveis em inglês pra ficar mais facil de entender já que a base de dados está em inglês.

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
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
df_seasons = pd.read_csv("data/seasons.csv", sep=",")
df_lap_times = pd.read_csv("data/lap_times.csv", sep=",")

#Criando o menu de seleção
with st.sidebar:
    category = option_menu(
        menu_title=None,
        options=["Piloto", "Equipe", "Corridas"],
        icons=["person", "people", "flag"],
        menu_icon="cast",
        orientation="vertical",
        styles={
            "nav-link-selected": {"background-color": "#FF0000"},
        }
    )

df_drivers['full_name'] = df_drivers['forename'] + ' ' + df_drivers['surname']

if category == "Piloto":

    col1, col2 = st.columns([3, 8])
    with col1:
        #Organiza os pilotos por ordem de vitórias (Isso é mais por "estética" para aparecer os pilotos principais primeiro)
        drive_order = (
            df_drivers.merge(
                df_results[df_results['position'] == '1']
                .groupby('driverId')
                .size()
                .reset_index(name='wins'),
                on='driverId', 
                how='left' #Mantém todos os pilotos mesmo que não tenham vitórias
            )
            .fillna({'wins': 0})
            .sort_values('wins', ascending=False)
            ['full_name']
            .tolist()
        )

        #Seleção do piloto:
        driver = st.selectbox(
            "Piloto",
            drive_order,
            index=None,
            placeholder="Selecione um piloto",
        )

    #Coletando as informações do piloto selecionado:
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

        total_podiums = df_results[
            (df_results['driverId'] == driver_id) & 
            (df_results['position'].isin(['1', '2', '3']))
        ].shape[0]
    else:
        total_points = 0
        total_wins = 0
        total_podiums = 0
        driver_nationality = '-'

    #Mostra as informações do piloto:
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total de Pontos", value=f"{total_points:.0f}")
    with col2:
        st.metric(label="Vitórias", value=total_wins)
    with col3:
        st.metric(label="Pódios", value=total_podiums)
    with col4:
        st.metric(label="Nacionalidade", value=driver_nationality)
    
    #Gráfico de pontos por ano do piloto (Alterei para um gráfico de barras):
    if driver:
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
            title=f'Pontuação por Ano',
            color_discrete_sequence=['#FF0000']
        )
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Pontos",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, key="points_chart")
        
        #Calculando a porcentagem de corridas pontuadas
        total_races = len(driver_results)
        scoring_races = len(driver_results[driver_results['points'] > 0])
        non_scoring_races = total_races - scoring_races
        scoring_percentage = (scoring_races / total_races) * 100 if total_races > 0 else 0
        
        scoring_data = pd.DataFrame({
            'Status': ['Corridas pontuando', 'Corridas sem pontos'],
            'Quantidade': [scoring_races, non_scoring_races]
        })
        
        #Gráfico de corridas pontuadas e corridas sem pontos:
        fig2 = px.pie(
            scoring_data,
            values='Quantidade',
            names='Status',
            title=f'Porcentagem de Corridas Pontuando',
            hole=0.4,
            color_discrete_sequence=['#FF0000', '#f7bebe']
        )
        
        fig2.update_traces(
            textposition='none',
            textinfo='none'
        )
        
        fig2.add_annotation(
            text=f'{scoring_percentage:.1f}%',
            x=0.5,
            y=0.5,
            showarrow=False,
            font_size=20
        )
        
        #Calculando a porcentagem de vitórias:
        wins = len(driver_results[driver_results['position'] == '1'])
        non_wins = total_races - wins
        win_percentage = (wins / total_races) * 100 if total_races > 0 else 0

        wins_data = pd.DataFrame({
            'Status': ['Vitórias', 'Outras posições'],
            'Quantidade': [wins, non_wins]
        })
        
        fig3 = px.pie(
            wins_data,
            values='Quantidade',
            names='Status',
            title=f'Porcentagem de Vitórias',
            hole=0.4,
            color_discrete_sequence=['#f7bebe', '#FF0000']
        )
        
        fig3.update_traces(
            textposition='none',
            textinfo='none'
        )
        
        fig3.add_annotation(
            text=f'{win_percentage:.1f}%',
            x=0.5,
            y=0.5,
            showarrow=False,
            font_size=20
        )
        
        #Organizando os gráficos lado a lado:

        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(fig2, use_container_width=True, key="percentage_chart")
        
        with col2:
            st.plotly_chart(fig3, use_container_width=True, key="wins_percentage_chart")

if category == "Corridas":
    race_year = df_seasons['year']
    race_year_ordered = race_year.sort_values(ascending=False)

    # Organiza a quantidade e o tamanho das colunas
    col1, col2 = st.columns([5,10])
    with col1:
        # Selectbox do ano da corrida
        year = st.selectbox(
            "Ano",
            race_year_ordered,
            index=None,
            placeholder="Selecione o ano da corrida"
        )

    if year:
        with col2:
            # Filtro para mostrar apenas as corridas que aconteceram no ano selecionado
            selected_year_race = df_races[df_races['year'] == year]['name']

            # Selectbox da corrida
            race = st.selectbox(
                "Corrida",
                selected_year_race,
                index=None,
                placeholder="Selecione uma corrida"
            )

    if year and race:
        # Coleta o ID da corrida selecionada
        race_id = df_races[(df_races['year'] == year) & (df_races['name'] == race)]['raceId'].iloc[0]

        # Filtra pelo vencedor da corrida e coleta o nome dele
        winner_name = (
            df_results[
                (df_results['raceId'] == race_id) & 
                (df_results['position'] == '1')
            ]
            .merge(
                df_drivers[['driverId', 'full_name']], 
                on='driverId'
            ).iloc[0]['full_name']
        )

        col1, col2 = st.columns([2,8])

        with col1:
            st.metric(label="Vencedor", value=winner_name)

        # Filtra as voltas pelo ID da corrida
        race_lap_data = df_lap_times[df_lap_times['raceId'] == race_id]
        
        # Adiciona a abreviação do piloto
        race_lap_data = race_lap_data.merge(
            df_drivers[['driverId', 'code']], 
            on='driverId', 
            how='left'
        )

        # Cria o gráfico de linhas
        fig = px.line(
            race_lap_data,
            x='lap',
            y='position',
            color='code',
            title=f'Posição dos pilotos por volta - {race} {year}',
            labels={
                'lap': 'Voltas',
                'position': 'Posição',
                'code': 'Piloto'
            }
        )

        # Customização do gráfico
        fig.update_layout(
            yaxis_range=[20, 1],  # Inverte o eixo Y
            showlegend=True,
            legend_title_text='Pilotos',
            height=700
        )

        # Mostra o gráfico na tela
        st.plotly_chart(fig, use_container_width=True, key="lap_chart")

