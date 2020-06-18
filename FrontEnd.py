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
    html.Div([], style={
      'background-color' : 'red',
      'padding' : '10px',
      'position' : 'fixed',
      'top' : '0px',
      'left' : '0px',
      'width' : '100%'
    }
    ),
    #left bar
    html.Div([dcc.Dropdown(id='drop_type', options=[
                {'label' : 'AR', 'value' : 'AR'},
                {'label' : 'ARIMA', 'value' : 'ARIMA'},
                {'label' : 'SARIMAX', 'value' : 'SARIMAX'}
                ], value='test')
    ],
     style={
       'height' : '100%',
       'width' : '200px',
       'position' : 'fixed',
       'z-index' : '1',
       'top' : '50px',
       'left' : '10px',
       'background-color' : 'grey',
       'overflow-x' : 'hidden',
       'padding-top' : '20px'
     }),
    #middle
    html.Div([#dcc.Graph(id='graph')
              dcc.Graph(id='graph')
    ], style={
      'margin-left' : '200px',
      'background-color' : 'blue',
      'padding' : '5%'
    }
    ),
    #bottom
    html.Div([
            html.P('this is the bottom')],

            style={'padding' : '1em',
                    'background-color' : 'green'}
            )

], style={
        'width': '80%',
        'height' : '80%',
        'padding' : '1em',
        'background-color' : 'yellow'
})





@app.callback(Output('graph', 'figure'),
                [Input('drop_type', 'value')]
                 #Input(, 'value')])
)
def choose(drop_type):
    if (drop_type == 'AR'):
        trace1 = go.Bar(x=[0,1,2,3,4], y=[1,1,1,1,1])
        trace2 = go.Bar(x=[0,1,2,3,4], y=[2,2,2,2,2])
    elif (drop_type == 'ARIMA'):
        trace1 = go.Bar(x=[0,1,2,3,4], y=[3,3,3,3,3])
        trace2 = go.Bar(x=[0,1,2,3,4], y=[4,4,4,4,4])
    elif (drop_type == 'SARIMAX'):
        trace1 = go.Bar(x=[0,1,2,3,4], y=[5,5,5,5,5])
        trace2 = go.Bar(x=[0,1,2,3,4], y=[6,6,6,6,6])
    else:
        trace1 = go.Bar(x=[0,1,2,3,4], y=[7,7,7,7,7])
        trace2 = go.Bar(x=[0,1,2,3,4], y=[8,8,8,8,8])
    return {
            'data' : [trace1, trace2],
            'type' : 'bar',
            'name' : drop_type,
            'layout' : go.Layout(title=drop_type, barmode='stack')
            }




app.run_server()#, use_reloader=False , debug=True
