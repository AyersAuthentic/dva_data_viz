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


app = dash.Dash(external_stylesheets = [ dbc.themes.COSMO],)



navbar = dbc.Navbar(id = 'navbar', children = [


        dbc.Col(html.H1("Covid Analysis Dashboard",
                        className='text-center text-primary mb=4'
        ), width=12)
    
])

app.layout = html.Div(id = 'parant', children = [navbar])



if __name__=='__main__':
    app.run_server()