# -*- coding: utf-8 -*-

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def deaths_line_plot():
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Dato == 'I alt'].index)
    fig = px.line(df, x='Dato', y='Antal_døde', title='COVID-19 deaths per day', labels=dict(Dato = 'Date', Antal_døde = 'Number of deaths'))
    #fig.update_yaxes(range=[min(df.Antal_døde)-1, max(df.Antal_døde)+1])
    plot(fig)
    fig.write_html("../Visualisations/deaths_line_plot.html")
        
def cumulated_deaths_line_plot():
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Dato == 'I alt'].index)
    df['Akkumuleret'] = df.Antal_døde.cumsum()
    fig = px.line(df, x='Dato', y='Akkumuleret', title='Cumulated COVID-19 deaths per day', labels=dict(Dato = 'Date', Akkumuleret = 'Cumulated number of deaths'))
    #fig.update_xaxes(range=[min(df.Dato), max(df.Dato)])
    #fig.update_yaxes(range=[min(df.Antal_døde)-10, max(df.Akkumuleret)+10])
    plot(fig)
    fig.write_html("../Visualisations/cumulated_deaths_line_plot.html")

deaths_line_plot()
cumulated_deaths_line_plot()