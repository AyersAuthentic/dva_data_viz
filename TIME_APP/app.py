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
from urllib.request import urlopen
import json
import csv
import plotly.graph_objs as go


df = pd.read_csv('https://storage.googleapis.com/additional-data/CummulatedClean_Nov22_with_lock/0_CMaster2_HPS_CDC_CPS_Vaccinated_with_lock.csv')

states = df.STATE.unique()

states_list = list(states)
print(states_list)
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
                 for x in df.columns[7:]],
        value=['people_vaccinated_per_hundred','CDCCOUNT'],
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
    dff = df[df['STATE'].isin(selected_states)]
    print(dff.head())
    dff = dff[cols]
    corr_mat = dff.corr()
    print(corr_mat)
    fig = go.Figure(data=go.Heatmap(
                   z=corr_mat,
                   x=cols,
                   y=cols,
                   hoverongaps = False))

    return fig



if __name__=='__main__':
    # app.run_server(debug=False, host="0.0.0.0", port=8080)
    app.run_server(debug=True)