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

from numpy import radians, cos, sin
import plotly.graph_objects as go
import pickle

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)

navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(html.H1("Prediction Application Demo",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])

# Dropdown Options Descriptions (Front Facing)
income = ["Less than $25,000",
          "$25,000 - $34,999",
          "$35,000 - $49,999",
          "$50,000 - $74,999",
          "$75,000 - $99,999",
          "$100,000 - $149,999",
          "$150,000 - $199,999",
          "$200,000 and above"]

workloss = ["No",
            "Yes"]

mortconf = ["Not at all confident",
            "Slightly confident",
            "Moderately confident",
            "Highly confident",
            "Payment is/will be deferred"]

mortlmth = ["Yes",
            "No"]

lockdown = ["0",
            "1",
            "2",
            "3",
            "4",
            "5"]

body = html.Div([
    dbc.Row([dbc.Col(
        dbc.Row([
            html.Div([
                "Did you pay last month's mortgage or rent?",
                dcc.Dropdown(id="mortlmth",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(mortlmth)]),
            ]),
            html.Div([
                "Are you confident that you will pay your mortgage/rent next month?",
                dcc.Dropdown(id="mortconf",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(mortconf)]),
            ]),
            html.Div([
                "Income",
                dcc.Dropdown(id="income",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(income)]),
            ]),
            html.Div([
                "Lockdown Level",
                dcc.Dropdown(id="lockdown",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(lockdown)]),
            ]),
            html.Div([
                "Have you experienced recent household job loss?",
                dcc.Dropdown(id="workloss",
                             options=[{'label': value, 'value': indx}
                                      for indx, value in enumerate(workloss)]),

            ]),
        ])

        , style={"height": "50%"}, lg=3),
        dbc.Col(dcc.Graph(id="bar_chart_pred", figure={}))])
])

app.layout = html.Div(id='parent', children=[navbar, body])


@app.callback(
    Output("bar_chart_pred", "figure"),
     [Input("income", "value"),
     Input("workloss", "value"),
     Input("mortconf", "value"),
     Input("mortlmth", "value"),
     Input("lockdown", "value"),
     ])
def update_barchart(income, wrkloss, mortconf, mortlmth, lockdown):

    features = np.array([income, wrkloss, mortconf, mortlmth, lockdown])
    features[features == None] = 0  # Convert Nones to 0, for when the dropdown option is not selected
    print(features)

    with open('../models/mental_health_rgr.pickle', 'rb') as handle:
        rgr = pickle.load(handle)

    print(f'features: {features}')
    print(type(features))

    # Check if all zeros. If so, prediction = 0
    is_all_zero = not np.any(features)
    if is_all_zero:
        prediction = 0
    else:
        prediction = rgr.predict([features])
        prediction = prediction.item()
        print(f'Prediction: {prediction}')

    cdc = 75

    df = pd.DataFrame([["income", income, cdc],
                       ["wrkloss", wrkloss, cdc],
                       ["Mortconf", mortconf, cdc],
                       ["Mortlmth", mortlmth, cdc],
                       ["Lockdown", lockdown, cdc],
                       ["Prediction", prediction, cdc]],
                      columns=["Features", "Level", "CDC"])

    print(df)
    """
    fig = px.bar(df, x = "Features", y="Level"
            #,animation_group = "Features"
            #,animation_frame = "Pos"
                 , color="Level"
                 ,range_y=[0,25]
                 )
    fig.update_layout(margin={"r":0,"t":10,"l":0,"b":0})
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Depression Meter", 'font': {'size': 24}},
        delta={'reference': 20, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 7.5], 'color': 'cyan'},
                {'range': [7.5, 10], 'color': 'red'},
                {'range': [25, 40], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})

    return fig


if __name__=='__main__':
    app.run_server(debug=True)

