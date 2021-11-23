import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from datetime import date
from dash.dependencies import Input,Output
import dash_table
from urllib.request import urlopen
import json
import csv
import plotly.graph_objs as go


df = pd.read_csv('https://storage.googleapis.com/additional-data/newCummulatedClean/new_CMaster_HPS_CDC_CPS_NYC_Vaccinated.csv')

states = df.STATE_CODE.unique()
states_list = list(states)
states_list.pop(-20)
print(states_list)
states_with_all = states_list.copy()
states_with_all.append('ALL')
print(states_with_all)

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)




navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(html.H1("Data Correlations Heatmap Analysis",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])




body  = html.Div([
    html.P("Attributes Included:"),
    dcc.Checklist(
        id='attributes',
        options=[{'label': x, 'value': x} 
                 for x in df.columns],
        value=['people_vaccinated_per_hundred','cases_avg_per_100k'],
    ),
    dcc.Dropdown(id='state_drop', multi=True, value='CA',
                    options=[{'label':x, 'value':x}
                            for x in states_with_all],
                    ),
    dcc.Graph(id="graph", figure={}),
])


app.layout = html.Div(id = 'parant', children = [navbar, body])

@app.callback(
    Output("graph", "figure"), 
    [Input("attributes", "value"),
    Input("state_drop", "value")])
def filter_heatmap(cols, states):
    selected_states = []
    if 'ALL' in states:
        selected_states = states_list
    else:
        if isinstance(states, list):
            selected_states = states
        else:
            selected_states = [states]

    print(selected_states)
    dff = df[df['STATE_CODE'].isin(selected_states)]
    print(dff.head())
    dff = dff[cols]
    corr_mat = dff.corr()
    fig = go.Figure(data=go.Heatmap(
                   z=corr_mat,
                   x=cols,
                   y=cols,
                   hoverongaps = False))

    return fig




if __name__=='__main__':
    app.run_server(host="0.0.0.0", debug=True)
