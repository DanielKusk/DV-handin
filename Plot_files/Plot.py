# -*- coding: utf-8 -*-

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

def deaths_line_plot():
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Antal_døde > 100].index)
    print(df.head())
    fig = px.line(df, x='Dato', y='Antal_døde')
    fig.update_yaxes(range=[min(df.Antal_døde)-1, max(df.Antal_døde)+1])
    plot(fig)
    
deaths_line_plot()