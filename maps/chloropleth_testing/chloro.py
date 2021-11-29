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


df = pd.read_csv("cases_per_100.csv", dtype={"fips": str})

df = df[df['state'] != 'NYC']

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)



navbar = dbc.Navbar(id = 'navbar', children = [


        dbc.Col(html.H1("Covid Analysis Dashboard",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])

month_years = ['01/2020', '02/2020', '03/2020', '04/2020', '05/2020', '06/2020', 
'07/2020', '08/2020', '09/2020', '10/2020', '11/2020', '12/2020',
'01/2021', '02/2021', '03/2021', '04/2021', '05/2021', '06/2021', 
'07/2021', '08/2021', '09/2021', '10/2021', '11/2021', '12/2021'
]


body = dbc.Container([

    dbc.Row([
        dcc.Graph(id='covid_graph_1', figure = {}),
        dcc.Dropdown(id='covid_graph_1_drop', multi=False, value='10/2020',
                         options=[{'label':x, 'value':x}
                                  for x in month_years],
                         )
    ])

])

app.layout = html.Div(id = 'parent', children = [navbar, body])


# Callbacks

@app.callback(
    Output('covid_graph_1', 'figure'),
    Input('covid_graph_1_drop', 'value')
)
def update_graph(month_year):
    dff = df[df['month_year']==month_year]

    fig = px.choropleth(dff, locations='state', color='new_case_per',
                           color_continuous_scale="ylorbr",
                           range_color=(dff['new_case_per'].min(), dff['new_case_per'].max()),
                           locationmode="USA-states",
                           scope="usa",
                           labels={'new_case_per':'New Cases Per 100 Thousand'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    
    return fig






if __name__=='__main__':
    app.run_server()