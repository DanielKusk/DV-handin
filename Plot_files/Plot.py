# -*- coding: utf-8 -*-

from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
from plotly.subplots import make_subplots

def deaths_line_plot(type):
    df = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df = df.drop(df[df.Dato == 'I alt'].index)
    fig = px.line(df, x='Dato', y='Antal_døde', title='COVID-19 deaths per day', labels=dict(Dato = 'Date', Antal_døde = 'Number of deaths'))
    if type == 'html':
        fig.update_xaxes(rangeslider_visible=True)
        fig.write_html("../Visualisations/deaths_line_plot.html", config= {'displaylogo': False})
        #plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/deaths_line_plot.png", scale=2)
    else:
        print('Invalid type given')
        
        
def death_and_cases_combo_plot(type):
    df_death = pd.read_csv('../Data/SSI/deaths_over_time.csv', sep=';')
    df_death = df_death.drop(df_death[df_death.Dato == 'I alt'].index)
        
    df_death.rename(columns = {'Dato' : 'Date'}, inplace = True)
    df_cases = pd.read_csv('../Data/SSI/Test_pos_over_time.csv', sep=';', decimal=',', thousands='.')
    df_cases = df_cases.drop(df_cases[df_cases.Date == 'I alt'].index)
    df_cases = df_cases.drop(df_cases[df_cases.Date == 'Antal personer'].index)
    df = df_death.merge(df_cases.set_index('Date'), how='right', on='Date')
    df = df.fillna(0)
    fig = make_subplots(2, 1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['Date'], y=df.Antal_døde, mode='lines', name='Deaths'), 1,1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df.NewPositive, mode='lines', name='New infections'), 2,1)
    fig.update_layout(title='New infections and deaths related to COVID-19 per day')
    if type == 'html':
        fig.write_html("../Visualisations/death_and_cases_combo_plot.html", config= {'displaylogo': False})
        plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/death_and_cases_combo_plot.png", scale=2)
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
        #plot(fig, config={'displaylogo': False})
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
        #plot(fig, config={'displaylogo': False})
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
    df = df.sort_values(by = 'Cumulated incidence', ascending = False)
    if region == 'Christiansø':
        df = df.drop(df[df.Region != region].index)
        fig = px.bar(df, x = 'Municipality', y='Cumulated incidence', title='Cumulated incidence of COVID-19 on ' + region + ' per 100 000 inhabitants')
    elif region in ['Hovedstaden','Midtjylland','Nordjylland','Sjælland','Syddanmark']:
        df = df.drop(df[df.Region != region].index)
        fig = px.bar(df, x = 'Municipality', y='Cumulated incidence', title='Cumulated incidence of COVID-19 in Region ' + region + ' per 100 000 inhabitants')
    elif region == 'all':
        df_grouped = df.groupby(['Region']).mean()
        df_grouped['Cumulated incidence'] = [round(i) for i in df_grouped['Cumulated incidence']]
        df_grouped = df_grouped.sort_values(by = 'Cumulated incidence', ascending = False)
        fig = px.bar(df_grouped, x=df_grouped.index, y='Cumulated incidence', title ='Cumulated incidence of COVID-19 per 100 000 inhabitants by region', labels={'x':'Region'})
    else:
        print('Invalid region given')
    if type == 'html':
        fig.write_html("../Visualisations/overall_incidence_bar_plot_" + region + ".html", config= {'displaylogo': False})
        #plot(fig, config={'displaylogo': False})
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
    fig = px.choropleth(df,geojson=df.geometry, color='Cumulated incidence', locations='Imdeks', projection='mercator', hover_data={'Imdeks': False}, hover_name="KOMNAVN", color_continuous_scale = 'Reds', title='Cumulated incidence of COVID-19 per 100 000 inhabitants by municipality')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":20})
    if type == 'html':
        fig.write_html("../Visualisations/overall_incidence_map.html", config= {'displaylogo': False})
        #plot(fig)
    elif type == 'png':
        fig.write_image("../Visualisations/overall_incidence_map.png", scale = 2)
    else:
        print('Invalid type given')

def cases_line_plot(type):
    df = pd.read_csv('../Data/SSI/Test_pos_over_time.csv', sep=';', decimal=',', thousands='.')
    df = df.drop(df[df.Date == 'I alt'].index)
    df = df.drop(df[df.Date == 'Antal personer'].index)
    fig = px.line(df, x='Date', y='NewPositive', title='Positive COVID-19 tests per day', labels=dict(NewPositive = 'People tested positive for COVID-19'))
    if type == 'html':
        fig.update_xaxes(rangeslider_visible=True)
        fig.write_html("../Visualisations/cases_line_plot.html", config= {'displaylogo': False})
        #plot(fig, config={'displaylogo': False})
    elif type == 'png':
        fig.write_image("../Visualisations/cases_line_plot.png", scale=2)
    else:
        print('Invalid type given')
        
def age_cases_bar_plot(type):
    df = pd.read_csv('../Data/SSI/Cases_by_age.csv', sep=';', decimal=',', thousands='.')
    df = df.drop(df[df.Aldersgruppe == 'I alt'].index)
    fig = px.bar(df, x = 'Aldersgruppe', y='Procent_positive', title='Positivity percentage of COVID-19 by age group', labels=dict(Aldersgruppe = 'Age group', Procent_positive = "Positivity percentage"))
    if type == 'html':
        fig.write_html("../Visualisations/age_cases_bar_plot.html", config= {'displaylogo': False})
        #plot(fig)
    elif type == 'png':
        fig.write_image("../Visualisations/age_cases_bar_plot.png", scale=2)
    else:
        print('Invalid type given')
        
def update_all():
    deaths_line_plot('html')
    deaths_line_plot('png')
    cumulated_deaths_line_plot('html')
    cumulated_deaths_line_plot('png')
    death_and_cases_combo_plot('html')
    death_and_cases_combo_plot('png')
    positivity_percentage_line_plot('html')
    positivity_percentage_line_plot('png')
    overall_incidence_map('html')
    overall_incidence_map('png')
    overall_incidence_bar_plot('Christiansø','html')
    overall_incidence_bar_plot('Christiansø','png')
    overall_incidence_bar_plot('Hovedstaden','html')
    overall_incidence_bar_plot('Hovedstaden','png')
    overall_incidence_bar_plot('Midtjylland','html')
    overall_incidence_bar_plot('Midtjylland','png')
    overall_incidence_bar_plot('Nordjylland','html')
    overall_incidence_bar_plot('Nordjylland','png')
    overall_incidence_bar_plot('Sjælland','html')
    overall_incidence_bar_plot('Sjælland','png')
    overall_incidence_bar_plot('Syddanmark','html')
    overall_incidence_bar_plot('Syddanmark','png')
    overall_incidence_bar_plot('all','html')
    overall_incidence_bar_plot('all','png')
    overall_incidence_map('html')
    overall_incidence_map('png')
    cases_line_plot('html')
    cases_line_plot('png')
    age_cases_bar_plot('html')
    age_cases_bar_plot('png')
    
update_all()