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
dcc.Slider(
        id='month', min=0, max=20,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=1,
    ),
      #  dcc.Dropdown(id="month", value=1,
      #                   options=[{'label':x, 'value':x}
     #                           for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Birth Year",
    dcc.Slider(
        id='birth_year', min=0, max=20,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=2,
    ),
        #dcc.Dropdown(id="birth_year", value=2,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Eductation",
    dcc.Slider(
        id='eeduc', min=0, max=20,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=3,
    ),
        #dcc.Dropdown(id="eeduc", value=3,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]])
    ]),
    html.Div([
        "Mortgage Last Month",
    dcc.Slider(
        id='mortlmth', min=0, max=10,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=4,
    ),
        #dcc.Dropdown(id="mortlmth", value=4,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Mortgage Confidence",
    dcc.Slider(
        id='mortconf', min=0, max=10,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=6,
    ),
        #dcc.Dropdown(id="mortconf", value=6,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Income",
    dcc.Slider(
        id='income', min=0, max=10,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=7,
    ),
        #dcc.Dropdown(id="income", value=7,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]]),
    ]),
    html.Div([
        "Type of Work",
    dcc.Slider(
        id='type_work', min=0, max=10,step=1,
        marks={
        0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20'
        },
        value=2,
    ),
        #dcc.Dropdown(id="type_work",  value=2,
         #                options=[{'label':x, 'value':x}
          #                        for x in [i for i in range(10)]]),

    ]),
    #html.Div([dbc.Button('Predict', id='predict_submit', n_clicks=0, size='lg', style={"background":"#3e1e4f", "color":"#fff", "border-color":"#3e1e4f", "min-width":"240px" })], style={"text-align":"center", "padding":"15px" }),
    ])
    
    #, style={"height": "50%"}
    , width={'size':3,'offset':1,'order':1}#xs=12, sm=12, md=12, lg=3, xl=3
        ),
    dbc.Col(dcc.Graph(id="bar_chart_pred", figure={}), width={'size':6,'offset':1,'order':2} #xs=12, sm=12, md=12, lg=7, xl=7
         )])
   
])


app.layout = html.Div(id = 'parant', children = [navbar, body])

@app.callback(
    Output("bar_chart_pred", "figure"), 
    [#Input("predict_submit", 'n_clicks'),
    Input("month", "value"),
    Input("birth_year", "value"),
    Input("eeduc", "value"),
    Input("mortlmth", "value"),
    Input("mortconf", "value"),
    Input("income", "value"),
    Input("type_work", "value"),
    ])
def update_barchart(month, birth_year, eeduc,
                    mortlmth, mortconf, income,
                    typework): #predict_submit

    print("Button Clicked!!!!!!!")
    Features = ["eeduc", "mortlmth", "mortconf", "income","typework", "prediction", "CDC"]
    
    prediction = eeduc + mortlmth + mortconf + income + typework
    print(prediction)
    cdc = 75
    print("vipul")
    df = pd.DataFrame([[0,"Educ", 0, cdc],[1,"Educ", eeduc, cdc],[0,"Mortlmth", 0, cdc], [1,"Mortlmth", mortlmth, cdc], [0,"Mortconf", 0, cdc], [1,"Mortconf", mortconf, cdc],
                        [0,"Income", 0, cdc], [1,"Income", income, cdc],[0,"Prediction", 0, cdc],[1,"Prediction", prediction, cdc],], columns=["Pos","Features", "Level", "CDC"])
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
            'axis': {'range': [None, 40], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': 'cyan'},
                {'range': [20, 25], 'color': 'red'},
                {'range': [25, 40], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})

    return fig


if __name__=='__main__':
    app.run_server(debug=True)

