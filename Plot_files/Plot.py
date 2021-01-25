# -*- coding: utf-8 -*-

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import json
import geopandas as gpd

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

def positivity_percentage_line_plot(type):
    df = pd.read_csv('../Data/SSI/Test_pos_over_time.csv', sep=';', decimal=',', thousands='.')
    fig = px.line(df, x='Date', y='PosPct', title='COVID-19 positivity percentage per day', labels=dict(PosPct = 'Positivity percentage'))
    df = df.drop(df[df.Date == 'I alt'].index)
    df = df.drop(df[df.Date == 'Antal personer'].index)
    if type == 'html':
        fig.update_xaxes(rangeslider_visible=True)
        fig.write_html("../Visualisations/positivity_percentage_line_plot.html", config= {'displaylogo': False})
        plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/positivity_percentage_line_plot.png", scale=2)
    else:
        print('Invalid type given')
        
def get_region_by_name(municipality):
    df = pd.read_csv('../Data/regions.csv', sep=',')
    return df.Region[df.Municipality == municipality].to_string(index=False)

def get_region_by_code(municipality):
    df = pd.read_csv('../Data/regions.csv', sep=',')
    return df.Region[df.Municipality_id == municipality].to_string(index=False)
        
def overall_incidence_bar_plot(region, type):
    df = pd.read_csv('../Data/SSI/Municipality_test_pos.csv', sep=';', decimal=',', thousands='.')
    df['Region'] = [get_region_by_code(i) for i in df['Kommune_(id)']]
    df.rename(columns={'Kommune_(id)' : 'Municipality id', 'Kommune_(navn)':'Municipality', 'Kumulativ_incidens_(per_100000)' : 'Cumulated incidence'}, inplace=True)
    df = df.drop(df[df.Region != region].index)
    df = df.sort_values(by = 'Cumulated incidence', ascending = False)
    fig = px.bar(df, x = 'Municipality', y='Cumulated incidence', title='Cumulated incidence of COVID-19 in Region ' + region + ' per 100 000 inhabitants')
    if type == 'html':
        fig.write_html("../Visualisations/overall_incidence_bar_plot_" + region + ".html", config= {'displaylogo': False})
        plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/overall_incidence_bar_plot_" + region + ".png", scale = 2)
    else:
        print('Invalid type given')

def get_incidence_by_name(municipality):
    df = pd.read_csv('../Data/SSI/Municipality_test_pos.csv', sep=';', decimal=',', thousands='.')
    df.rename(columns={'Kommune_(id)' : 'Municipality_id', 'Kommune_(navn)':'Municipality', 'Kumulativ_incidens_(per_100000)' : 'Incidence'}, inplace=True)
    return int(df.Incidence[df.Municipality == municipality])

def get_incidence_by_code(municipality):
    df = pd.read_csv('../Data/SSI/Municipality_test_pos.csv', sep=';', decimal=',', thousands='.')
    df.rename(columns={'Kommune_(id)' : 'Municipality_id', 'Kommune_(navn)':'Municipality', 'Kumulativ_incidens_(per_100000)' : 'Incidence'}, inplace=True)
    return int(df.Incidence[df.Municipality_id == municipality])

def overall_incidence_map(type):
    df = gpd.read_file('../Data/Map/kommuner.geojson')
    df['Cumulated incidence'] = [get_incidence_by_code(int(i)) for i in df['KOMKODE']]
    df['Imdeks'] = [i for i in df.index]
    fig = px.choropleth(df,geojson=df.geometry, color='Cumulated incidence', locations='Imdeks', projection='mercator', hover_data={'Imdeks': False}, hover_name="KOMNAVN", color_continuous_scale = 'Reds', title='Cumulated incidence of COVID-19 by municipality')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":20})
    if type == 'html':
        fig.write_html("../Visualisations/overall_incidence_map.html", config= {'displaylogo': False})
        plot(fig)
    elif type == 'png':
        fig.write_image("../Visualisations/overall_incidence_map.png", scale = 2)
    else:
        print('Invalid type given')

        
overall_incidence_map('png')


# def incidence_bar_plot(start_time, end_time, fig_type):
#     df_cases = pd.read_csv('../Data/SSI/Municipality_cases_time_series.csv', sep=';', decimal=',', thousands='.')
#     df_pop = pd.read_csv('../Data/SSI/Municipality_test_pos.csv', sep=';', decimal=',', thousands='.')
#     df = pd.DataFrame(dict(date = df_cases.date_sample, cases = df_cases))
#     print(df)
    #if time == 'week':'
    #    
    #elif time == 'day':
    #
    #else:
        #print('Invalid timeframe given')
    

# def incidence_map(time, fig_type):
#     df_cases = pd.read_csv('../Data/SSI/Municipality_cases_time_series.csv', sep=';', decimal=',', thousands='.')
#     df_pop = pd.read_csv('../Data/SSI/Municipality_test_pos.csv', sep=';', decimal=',', thousands='.')
#     print(df_pop)


#overall_incidence_bar_plot('Christiansø','html')
#overall_incidence_bar_plot('Christiansø','png')

# incidence_bar_plot('','')
    
#deaths_line_plot('html')
#cumulated_deaths_line_plot('html')
#positivity_percentage_line_plot('html')

#deaths_line_plot('png')
#cumulated_deaths_line_plot('png')
#positivity_percentage_line_plot('png')