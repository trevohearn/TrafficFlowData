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

app = dash.Dash(__name__)
app.layout = html.Div([ #container
    #top
    html.Div([], style={}
    ),
    #left bar
    html.Div([dcc.Dropdown(id='drop_type', options=[
                {'label' : 'AR', 'value' : 'AR'},
                {'label' : 'ARIMA', 'value' : 'ARIMA'},
                {'label' : 'SARIMAX', 'value' : 'SARIMAX'}
                ], value='test')
    ],
     style={'background-color' : 'red',
            'float' : 'left'
     }),
    #middle
    html.Div([#dcc.Graph(id='graph')
              html.P(id='graph')
    ], style={'border-color' : 'green'}
    ),
    #bottom
    html.Div([
            html.P('this is the bottom')],

            style={'padding' : '1em',
                    'background-color' : 'blue'}
            )

], style={
        'width': '80%',
        'height' : '80%',
        'padding' : '1em',
        'background-color' : 'red'
})





@app.callback(Output('graph', 'text'),
                [Input('drop_type', 'value')]
                 #Input(, 'value')])
)
def choose(drop_type):
    if (drop_type == 'AR'):
        return 'AR'
    elif (drop_type == 'ARIMA'):
        return 'ARIMA'
    elif (drop_type == 'SARIMAX'):
        return 'SARIMAX'
    else:
        return 'else'

app.run_server()#, use_reloader=False , debug=True
