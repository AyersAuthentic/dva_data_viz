import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from datetime import date
from dash.dependencies import Input,Output, State
from urllib.request import urlopen
import json
import csv
import plotly.graph_objs as go




app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)



navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(html.H1("Prediction Application Demo",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])




body  = html.Div([
    dbc.Row( [dbc.Col(
        
    dbc.Row([
    html.Div([
        "Month",
        dcc.Dropdown(id="month", value=1,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Birth Year",
        dcc.Dropdown(id="birth_year", value=2,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Eductation",
        dcc.Dropdown(id="eeduc", value=3,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]])
    ]),
    html.Div([
        "Mortgage Last Month",
        dcc.Dropdown(id="mortlmth", value=4,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Mortgage Confidence",
        dcc.Dropdown(id="mortconf", value=6,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Income",
        dcc.Dropdown(id="income", value=7,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Type of Work",
        dcc.Dropdown(id="type_work",  value=2,
                         options=[{'label':x, 'value':x}
                                  for x in [i for i in range(10)]]),

    ]),
    html.Div([dbc.Button('Predict', id='predict_submit', n_clicks=0)], style={"text-align":"center"}),
    ])
    
    , style={"height": "50%"} ,lg=3),
    dbc.Col(dcc.Graph(id="bar_chart_pred", figure={}))])
   
])


app.layout = html.Div(id = 'parant', children = [navbar, body])

@app.callback(
    Output("bar_chart_pred", "figure"), 
    [Input("predict_submit", 'n_clicks'),
    State("month", "value"),
    State("birth_year", "value"),
    State("eeduc", "value"),
    State("mortlmth", "value"),
    State("mortconf", "value"),
    State("income", "value"),
    State("type_work", "value"),
    ])
def update_barchart(month, birth_year, eeduc,
                    mortlmth, mortconf, income,
                    typework, predict_submit):

    print("Button Clicked!!!!!!!")
    Features = ["eeduc", "mortlmth", "mortconf", "income","typework", "prediction", "CDC"]
    
    prediction = eeduc + mortlmth + mortconf + income + typework
    print(prediction)
    cdc = 75

    df = pd.DataFrame([["Educ", eeduc, cdc], ["Mortlmth", mortlmth, cdc], ["Mortconf", mortconf, cdc], 
                        ["Income", income, cdc],["Prediction", prediction, cdc],], columns=["Features", "Level", "CDC"])
    print(df)

    fig = px.bar(df, x = "Features", y="Level", color=df.CDC)
    fig.update_layout(margin={"r":0,"t":10,"l":0,"b":0})
    return fig



if __name__=='__main__':
    app.run_server(debug=True)