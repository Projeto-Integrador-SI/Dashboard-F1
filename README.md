# 🏎️ Formula 1 | Dashboard

Este projeto é um **Dashboard Interativo da Fórmula 1** desenvolvido com **Streamlit**, **Plotly** e **Pandas**, que permite visualizar estatísticas e análises de desempenho de pilotos, equipes e corridas ao longo dos anos.

## 🚀 Funcionalidades

📈 Análise de desempenho dos **pilotos**:
  - Informações do piloto selecionado:
    
      - Total de pontos, Vitórias, Pódios e Nacionalidade
      - Gráficos de pontuação anual
      - Proporção de vitórias e corridas pontuadas

📈 Análise de desempenho das **equipes**:
  - Visão geral da melhores equipes
  - Informações da equipe selecionada:
    
      - Total de pontos, Vitórias, Pódios e Nacionalidade
      - Gráficos de pontuação anual
      - Proporção de vitórias e corridas pontuadas

📈 Análise de **corridas específicas**:
  - Identificação do pole position e vencedor
  - Evolução da posição dos pilotos por volta

## 🔧 Tecnologias e Ferramentas

| Ferramenta         | Versão Sugerida |
|--------------------|------------------|
| Python             | >= 3.9           |
| Streamlit          | >= 1.43.2        |
| Plotly             | >= 6.0.1        |
| Pandas             | >= 2.2.3         |

## 🗂️ Dados Utilizados

O projeto utiliza dados históricos de Fórmula 1 provenientes de datasets públicos. As principais bases são:

- **drivers.csv** — Informações dos pilotos.
- **driver_standings.csv** — Classificação dos pilotos por corrida.
- **races.csv** — Informações das corridas, incluindo ano e nome.
- **results.csv** — Resultados de cada piloto em cada corrida.
- **constructors.csv** — Informações das equipes (construtores).
- **seasons.csv** — Anos das temporadas.
- **lap_times.csv** — Tempos e posições dos pilotos volta a volta.
- **constructor_results.csv** — Resultados das equipes por corrida.

✅ **Por que esses dados são exibidos?**

Eles foram escolhidos para fornecer uma visão completa do desempenho ao longo das temporadas, tanto dos pilotos quanto das equipes, permitindo análises de vitórias, pódios, constância em pontuação e comparativos por ano.

## 👨‍💻 Autores

Projeto desenvolvido por: Guilherme Dias, João Pedro, Yago Amorim, Gabriel Camargo, Igor Rueda e Jônatas Avelar
