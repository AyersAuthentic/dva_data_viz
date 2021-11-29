import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
from datetime import date
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    
    counties = json.load(response)


df = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/counties_with_fips.csv", dtype={"fips": str})
df_2 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/lock_clean.csv", dtype={"fips": str})
df_3 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/master_viz_test.csv")
df_4 = pd.read_csv("https://storage.googleapis.com/additional-data/data_viz_data/trends/master_viz_test_2.csv")
print(df.head(5))
print(df_2.head(5))
print(df_3.head(5))
print(df_4.head(5))
trends = ['WRKLOSS', 'KINDWORK', 'MORTLMTH', 'MORTCONF',
       'INCOME', 'CDCCOUNT', 'REMPCT', 'people_vaccinated',
       'people_vaccinated_per_hundred', 'people_fully_vaccinated',
       'people_fully_vaccinated_per_hundred', 'ANXIOUS', 'WORRY', 'DOWN',
       'cases_avg_per_100k']

month_year = ['01/2020', '02/2020', '03/2020', '04/2020', '05/2020', '06/2020', 
'07/2020', '08/2020', '09/2020', '10/2020', '11/2020', '12/2020',
'01/2021', '02/2021', '03/2021', '04/2021', '05/2021', '06/2021', 
'07/2021', '08/2021', '09/2021', '10/2021', '11/2021', '12/2021'
]

app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)


navbar = dbc.Navbar(id = 'navbar', children = [

        dbc.Col(html.H1("Covid Trends Analysis",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])



body = dbc.Container([

    dbc.Row([

        dcc.Dropdown(id='trends_dropdown_X', multi=False, value='people_vaccinated_per_hundred',
                     options=[{'label': x, 'value': x}
                              for x in trends],
                     ),
        dcc.Graph(id='covid_trends_X', figure={})

    ]),
    dbc.Row([

        dcc.Dropdown(id='trends_dropdown', multi=False, value='people_vaccinated_per_hundred',
                     options=[{'label': x, 'value': x}
                              for x in trends],
                     ),
        dcc.Dropdown(id='trends_dropdown_2', multi=False, value='10/2020',
                     options=[{'label': x, 'value': x}
                              for x in month_year],
                     ),
        dcc.Graph(id='covid_trends_1', figure={})

    ]),

    dbc.Row([
        dbc.Col([
dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=date(2020, 1, 21),
            max_date_allowed=date(2021, 9, 29),
            initial_visible_month=date(2020, 1, 21),
            date=date(2020, 1, 21)
        ),
            dcc.Graph(id='covid_graph_1', figure = {})
        ], #width={'size':6,'offset':1,'order':1}
            xs=12, sm=12, md=12, lg=6, xl=6
        ),
        dbc.Col([
            dcc.DatePickerSingle(
            id='my-date-picker-single_2',
            min_date_allowed=date(2020, 3, 15),
            max_date_allowed=date(2021, 9, 29),
            initial_visible_month=date(2020, 3, 15),
            date=date(2020, 3, 15)
            ),
            dcc.Graph(id='covid_lockdowns', figure = {})
        ], #width={'size':4,'offset':1,'order':2}
            xs=12, sm=12, md=12, lg=6, xl=6
        )
    ])

],fluid=False)

app.layout = html.Div(id = 'parent', children = [navbar, body])


# Callbacks


@app.callback(
    Output('covid_graph_1', 'figure'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime("%Y-%m-%d")

        dff = df[df['date'] == date_string]


        fig = px.choropleth(dff, geojson=counties, locations='fips', color='cases_avg_per_100k',
                           color_continuous_scale="Rainbow",
                           range_color=(dff['cases_avg_per_100k'].min(), dff['cases_avg_per_100k'].max()),
                           scope="usa",
                           labels={'cases_avg_per_100k':'Covid Case Avg Per 100K'}
                          )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        
        
        return fig


@app.callback(
    Output('covid_lockdowns', 'figure'),
    Input('my-date-picker-single_2', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime("%-m/%-d/%Y")
        print(date_string)

        dff = df_2[df_2['date'] == date_string]
        print(dff.head())


        fig = px.choropleth(dff, geojson=counties, locations='fips', color='lockdown',
                           color_continuous_scale="Rainbow",
                           range_color=(df_2['lockdown'].min(), df_2['lockdown'].max()),
                           scope="usa",
                           labels={'lockdown':'Level of Covid Lockdown'}
                          )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        
        
        return fig


@app.callback(
    Output('covid_trends_X', 'figure'),
    Input('trends_dropdown_X', 'value')
)
def update_graph(trend):
    print(trend)
    print(df_4.shape)

    dff = df_4[['year_month','STATE_CODE', trend]]
    print(dff)

    fig = px.choropleth(dff, locations='STATE_CODE', color=dff[trend],
                            color_continuous_scale="ylorbr",
                            range_color=(dff[trend].min(), dff[trend].max()),
                            locationmode="USA-states",
                            animation_group="year_month",
                            animation_frame="year_month",
                            scope="usa",
                            labels={trend : trend}
                            )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    return fig


@app.callback(
    Output('covid_trends_1', 'figure'),
    [Input('trends_dropdown', 'value'),
     Input('trends_dropdown_2', 'value')]

)
def update_graph(trend, month_year):
    print(month_year)
    print(df_3.shape)

    dff = df_3[df_3['month_year'] == month_year]
    print("selected")
    print(dff.head())

    dff = dff[['STATE_CODE', trend]]
    print(dff)

    fig = px.choropleth(dff, locations='STATE_CODE', color=dff[trend],
                        color_continuous_scale="ylorbr",
                        range_color=(dff[trend].min(), dff[trend].max()),
                        locationmode="USA-states",
                        scope="usa",
                        labels={trend: trend}
                        )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__=='__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False, host="0.0.0.0", port=8080)
