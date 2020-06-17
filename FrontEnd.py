#Trevor O'Hearn
#6/17/20
#Front end for Traffic Flow Data Project
#Intent:
#Drop down lists of different time series analyses
#Shows different graphs from the analyses using plotly

#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#plotly
import plotly.graph_objects as go

app.layout = html.Div([ #container
    #top
    html.Div([], style={}
    ),
    #middle
    html.Div([

    ], style={}
    ),
    #bottom
    html.Div([
            html.p('this is the bottom')],

            style={'padding' : '1em',
                    'background-color' : 'blue'}
            )

], style={
        'width': '80%'',
        'height' : '80%'',
        'padding' : '1em',
        'background-color' : 'red'
})
