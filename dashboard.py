import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Formula 1 | Dashboard',
    page_icon='images/f1_logo.png',
    layout='wide'
)

col1, col2 = st.columns([1, 10])
with col1:
    st.image('images/f1_logo.png', width=100)
with col2:
    st.markdown('# DASHBOARD', unsafe_allow_html=True)

df_drivers = pd.read_csv("data/drivers.csv", sep=",")
df_standings = pd.read_csv("data/driver_standings.csv", sep=",")
df_races = pd.read_csv("data/races.csv", sep=",")
df_results = pd.read_csv("data/results.csv", sep=",")

# Create full name column
df_drivers['full_name'] = df_drivers['forename'] + ' ' + df_drivers['surname']
driver = st.sidebar.selectbox("Piloto", df_drivers["full_name"].unique(), index=None, placeholder="Selecione um piloto")

# Filter and sum points for selected driver across all races
if driver:
    driver_id = df_drivers[df_drivers['full_name'] == driver]['driverId'].iloc[0]
    # Get all results for the selected driver
    driver_results = df_results[df_results['driverId'] == driver_id]
    # Calculate total points
    total_points = driver_results['points'].sum()
else:
    total_points = 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total de Pontos", value=f"{total_points:.0f}")


# Create points per year graph
if driver:
    # Merge results with races to get year information
    driver_points_by_year = (
        df_results[df_results['driverId'] == driver_id]
        .merge(df_races[['raceId', 'year']], on='raceId')
        .groupby('year')['points']
        .sum()
        .reset_index()
    )
    
    # Create line chart
    fig = px.line(
        driver_points_by_year,
        x='year',
        y='points',
        title=f'Pontos por ano - {driver}',
        markers=True
    )
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Pontos",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
