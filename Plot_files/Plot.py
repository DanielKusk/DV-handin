# -*- coding: utf-8 -*-

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def deaths_line_plot(type):
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Dato == 'I alt'].index)
    fig = px.line(df, x='Dato', y='Antal_døde', title='COVID-19 deaths per day', labels=dict(Dato = 'Date', Antal_døde = 'Number of deaths'))
    if type == 'html':
        fig.update_xaxes(rangeslider_visible=True)
        fig.write_html("../Visualisations/deaths_line_plot.html", config= {'displaylogo': False})
        plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/deaths_line_plot.png", scale=2)
    else:
        print('Invalid type given')
    
        
def cumulated_deaths_line_plot(type):
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Dato == 'I alt'].index)
    df['Akkumuleret'] = df.Antal_døde.cumsum()
    fig = px.line(df, x='Dato', y='Akkumuleret', title='Cumulated COVID-19 deaths per day', labels=dict(Dato = 'Date', Akkumuleret = 'Cumulated number of deaths'))
    if type == 'html':
        fig.update_xaxes(rangeslider_visible=True)
        fig.write_html("../Visualisations/cumulated_deaths_line_plot.html", config= {'displaylogo': False})
        plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/cumulated_deaths_line_plot.png", scale=2)
    else:
        print('Invalid type given')


deaths_line_plot('png')
#cumulated_deaths_line_plot('html')