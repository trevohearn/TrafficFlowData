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
from statsmodels.tsa.arima_model import ARMA, ARIMA

#internal methods
def getLabels(dates):
    labels = []
    for d in dates:
        labels.append({'label' : d, 'value' : d})
    return labels



df = pd.read_csv('test_df_w_timeshift.csv')
df['Date_IntervalStart'] = pd.to_datetime(df['Date_IntervalStart'])
df.set_index('Date_IntervalStart', inplace=True)
startdates = df.index[0]


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
      'z-index' : '1',
      'top' : '0px',
      'left' : '0px',
      'width' : '100%'
    }
    ),
    #left bar
    html.Div([
    html.P('Select a Start Date', style={'text-align' : 'center'}),
    dcc.Dropdown(id='startdate', options=getLabels(df.index[0:-11]), value=df.index[0]),
    html.P('Select an End Date', style={'text-align' : 'center'}),
    dcc.Dropdown(id='enddate', options=getLabels(df.index[1:-10]), value=df.index[-11]),
    html.P('Select a Model', style={'text-align' : 'center'}),
    dcc.Dropdown(id='drop_type', options=[
            {'label' : 'AR', 'value' : 'AR'},
            {'label' : 'ARIMA', 'value' : 'ARIMA'},
            {'label' : 'SARIMAX', 'value' : 'SARIMAX'}
            ], value='AR'),
    html.P('P', style={'text-align' : 'center'}),
    dcc.Input(id='pvalue', type='number', value=2, debounce=True),
    html.P('D', style={'text-align' : 'center'}),
    dcc.Input(id='dvalue', type='number', value=1, debounce=True),
    html.P('Q', style={'text-align' : 'center'}),
    dcc.Input(id='qvalue', type='number', value=2, debounce=True)
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
        'background-color' : 'yellow'
})


def makeTrace(x, y, name):
    return go.Scatter(x=x, y=y, name=name)

#return statistical results from ARResults
def getTableResults():
    return None

@app.callback(Output('graph', 'figure'),
                [Input('drop_type', 'value'),
                Input('startdate', 'value'),
                Input('enddate', 'value'),
                Input('pvalue', 'value'),
                Input('dvalue', 'value'),
                Input('qvalue', 'value')]
                 #Input(, 'value')])
)
def choose(drop_type, startdate, enddate, pvalue, dvalue, qvalue):
    print(drop_type)
    print('----------------------------')
    print(startdate)
    print(type(startdate))
    print('----------------------------')
    print(enddate)
    print(type(enddate))
    slicedf = df.loc[startdate : enddate]
    print('----------------------------')
    print(len(slicedf.index))
    test_slice = df.loc[enddate:]
    endtime = list(pd.date_range(slicedf.index[-1], periods=24, freq='H'))[-1]
    x = [0,1,2,3,4]
    if (drop_type == 'AR'):
        m = AR(slicedf['TotalVolume'])
        mnolag = m.fit(method='mle', ic='aic')
        preds = mnolag.predict(start=slicedf.index[-11],end=endtime, dynamic=False).rename('AR PREDICTIONS')
        trace1 = makeTrace(preds.index, preds.values, 'Predicitons')
        trace2 = makeTrace(test_slice.index, test_slice.TotalVolume, 'Testing Data')
        half = (slicedf.shape[0] // 100)
        trace3 = makeTrace(slicedf.index[half:], slicedf['TotalVolume'].values[half:], 'Selected Data')
    elif (drop_type == 'ARIMA'):
        m = ARIMA(slicedf['TotalVolume'], order=(pvalue, dvalue, qvalue))
        mfit = m.fit(method='mle')
        preds = mfit.predict(start=test_slice.index[0], end=test_slice.index[-1], dynamic=False)
        trace1 = makeTrace(preds.index, preds.values, 'Predictions')
        trace2 = makeTrace(test_slice.index, test_slice.TotalVolume, 'Testing Data')
        half = (slicedf.shape[0] // 100)
        trace3 = makeTrace(slicedf.index[half:], slicedf['TotalVolume'].values[half:], 'Selected Data')
    elif (drop_type == 'SARIMAX'):
        trace1 = makeTrace(x, [5,5,5,5,5], '5', 'Predictions')
        trace2 = makeTrace(x, [6,6,6,6,6], '6', 'Testing Data')
        half = (slicedf.shape[0] // 100)
        trace3 = makeTrace(slicedf.index[half:], slicedf['TotalVolume'].values[half:], 'Selected Data')
    else:
        trace1 = makeTrace(x, [7,7,7,7,7], '7', 'Predictions')
        trace2 = makeTrace(x, [8,8,8,8,8], '8', 'Testing Data')
        half = (slicedf.shape[0] // 100)
        trace3 = makeTrace(slicedf.index[half:], slicedf['TotalVolume'].values[half:], 'Selected Data')
    return {
            'data' : [trace1, trace2, trace3],
            'type' : 'scatter',
            'name' : drop_type,
            'layout' : go.Layout(title=drop_type, barmode='stack')
            }



app.run_server()#, use_reloader=False , debug=True
