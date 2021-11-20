import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
import dash_table
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    
    states = json.load(response)

state_dict = {"type": "FeatureCollection"}
state_dict["features"] = states


df = pd.read_csv("test_cases_per.csv", dtype={"fips": str})
df = df[['fips', 'new_case_per']]

print(df.head())
print(type(df['new_case_per'][0]))

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)



navbar = dbc.Navbar(id = 'navbar', children = [


        dbc.Col(html.H1("Covid Analysis Dashboard",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])


fig = px.choropleth(df, geojson=states, locations='fips', color='new_case_per',
                           color_continuous_scale="Viridis",
                           range_color=(0, 500),
                           scope="usa",
                           labels={'new_case_per':'cases per 100 thousand'}
                          )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


body = dbc.Container([

    dbc.Row([
        dcc.Graph(id='covid_graph_1', figure = fig),
    ])

])

app.layout = html.Div(id = 'parant', children = [navbar, body])


# Callbacks






if __name__=='__main__':
    app.run_server()