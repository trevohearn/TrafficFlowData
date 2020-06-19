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

import pandas as pd
from statsmodels.tsa.ar_model import AR, ARResults


df = pd.read_csv('test_df_w_timeshift.csv')
df['Date_IntervalStart'] = pd.to_datetime(df['Date_IntervalStart'])



app = dash.Dash(__name__)
app.layout = html.Div([ #container
    #top
    html.Div([html.H2('Traffic Flow Data',
                style={
                    'font-size' : '20px',
                    'padding-left' : '25%',
                    'padding-right' : '25%',
                    'text-align' : 'center'
                        }
                    )
    ], style={
      'background-color' : 'red',
      'padding' : '10px',
      'position' : 'fixed',
      'top' : '0px',
      'left' : '0px',
      'width' : '100%'
    }
    ),
    #left bar
    html.Div([
    html.P('Select a Start Date', style={'text-align' : 'center'}),
    dcc.Dropdown(id='startdate', value=df.index[0]),
    html.P('Select an End Date', style={'text-align' : 'center'}),
    dcc.Dropdown(id='enddate', value=df.index[-1]),
    html.P('Select a Model', style={'text-align' : 'center'}),
    dcc.Dropdown(id='drop_type', options=[
            {'label' : 'AR', 'value' : 'AR'},
            {'label' : 'ARIMA', 'value' : 'ARIMA'},
            {'label' : 'SARIMAX', 'value' : 'SARIMAX'}
            ], value='AR'),
    html.P('P', style={'text-align' : 'center'}),
    dcc.Input(id='pvalue', type='number', value=1, debounce=True),
    html.P('D', style={'text-align' : 'center'}),
    dcc.Input(id='dvalue', type='number', value=1, debounce=True),
    html.P('Q', style={'text-align' : 'center'}),
    dcc.Input(id='qvalue', type='number', value=1, debounce=True)
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
       'padding-top' : '20px',
       'padding-right' : '10px',
       'padding-left' : '10px'
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


def makeTrace(x, y):
    return go.Scatter(x=x, y=y)


@app.callback(Output('graph', 'figure'),
                [Input('drop_type', 'value'),
                Input('startdate', 'value'),
                Input('enddate', 'value')]
                 #Input(, 'value')])
)
def choose(drop_type, startdate, enddate):
    slicedf = df.loc[startdate : enddate]
    test_slice = df.loc[enddate:]
    endtime = list(pd.date_range(slicedf.index[-1], periods=24, freq='H'))[-1]
    x = [0,1,2,3,4]
    if (drop_type == 'AR'):
        m = AR(slicedf)
        mnolag = m.fit(method='mle', ic='aic')
        preds = mnolag.predict(start=slicedf.index[-1],end=endtime, dynamic=False).rename('AR PREDICTIONS')
        trace1 = makeTrace(preds.index, preds.values)
        trace2 = makeTrace(test_slice.index, test_slice.TotalVolume)
    elif (drop_type == 'ARIMA'):
        trace1 = makeTrace(x, [3,3,3,3,3])
        trace2 = makeTrace(x, [4,4,4,4,4])
    elif (drop_type == 'SARIMAX'):
        trace1 = makeTrace(x, [5,5,5,5,5])
        trace2 = makeTrace(x, [6,6,6,6,6])
    else:
        trace1 = makeTrace(x, [7,7,7,7,7])
        trace2 = makeTrace(x, [8,8,8,8,8])
    return {
            'data' : [trace1, trace2],
            'type' : 'scatter',
            'name' : drop_type,
            'layout' : go.Layout(title=drop_type, barmode='stack')
            }



app.run_server()#, use_reloader=False , debug=True
