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
from fbprophet import Prophet

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


app = dash.Dash('Time-Series Analysis Comparison')

# Color Palette:
# https://www.color-hex.com/color-palettes/
# #'background-color' : '011f4b',
# #'background-color' : '03396c',
# #'background-color' : '005b96',
# #'background-color' : '6497b1',
# #'background-color' : 'b3cde0',
# use three main colors with a fouth for small styles
# add color layouts for types of models shown

# morning blue
# 9ecbc8	(158,203,200)
# 008684	(0,134,132)
# 005e78	(0,94,120)
# 384f6b	(56,79,107)
# 273347	(39,51,71)


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
      'background-color' : '#011f4b',
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
    html.P('Number of Prediction Points', style={'text-align' : 'center'}),
    dcc.Input(id='points', type='number', value=(24 * 7), debounce=True),
    html.P('P', style={'text-align' : 'center'}),
    dcc.Input(id='pvalue', type='number', value=2, debounce=True),
    html.P('D', style={'text-align' : 'center'}),
    dcc.Input(id='dvalue', type='number', value=1, debounce=True),
    html.P('Q', style={'text-align' : 'center'}),
    dcc.Input(id='qvalue', type='number', value=2, debounce=True),
    html.P('Floor', style={'text-align' : 'center'}),
    dcc.Input(id='floor', type='number', value=0, debounce=True),
    html.P('Cap', style={'text-align' : 'center'}),
    dcc.Input(id='cap', type='number', value=2000, debounce=True)
    ],
     style={
       'height' : '100%',
       'width' : '200px',
       'position' : 'fixed',
       'z-index' : '1',
       'top' : '50px',
       'left' : '10px',
       'background-color' : '005b96',
       #'background-color' : '#03396c',
       'overflow-x' : 'hidden',
       'padding-top' : '20px',
       'padding-right' : '10px',
       'padding-left' : '10px'
     }),
    #middle
    html.Div([#dcc.Graph(id='graph')
              dcc.Graph(id='graph'),
              dcc.Graph(id='graph2'),
              dcc.Graph(id='graph3')
    ], style={
      'margin-left' : '200px',
      'background-color' : '#6497b1',
      'padding' : '5%'
    }
    ),
    #bottom
    html.Div([
            html.P('this is the bottom')],

            style={'padding' : '1em',
                    'background-color' : '#005b96'}
            )

], style={
        'background-color' : '#b3cde0'
})


def makeTrace(x, y, name):
    return go.Scatter(x=x, y=y, name=name)

#return statistical results from ARResults
def getTableResults():
    return None

#add callbacks for seperate functionality
#efficiency increase

# get statistical results from fbprophet
# refer to jupyter notebook
def getFBProphetResults():
    return None

#return statistical results from lstm model
#refer to jupyter notebook
def getLSTMResults():
    return None



@app.callback(Output('graph', 'figure'),
                [Input('drop_type', 'value'),
                Input('startdate', 'value'),
                Input('enddate', 'value'),
                Input('pvalue', 'value'),
                Input('dvalue', 'value'),
                Input('qvalue', 'value'),
                Input('points', 'value')
                ]
                 #Input(, 'value')])
)
def choose(drop_type, startdate, enddate, pvalue, dvalue, qvalue, points):
    # print(drop_type)
    # print('----------------------------')
    # print(startdate)
    # print(type(startdate))
    # print('----------------------------')
    # print(enddate)
    # print(type(enddate))
    slicedf = df.loc[startdate : enddate]
    # print('----------------------------')
    # print(len(slicedf.index))
    test_slice = df.loc[enddate:]
    endtime = list(pd.date_range(slicedf.index[-1], periods=points, freq='H'))[-1]
    x = [0,1,2,3,4]
    trace1 = None
    trace2 = None
    trace3 = None
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
        preds = mfit.predict(start=test_slice.index[0], end=endtime, dynamic=False)
        trace1 = makeTrace(preds.index, preds.values, 'Predictions')
        trace2 = makeTrace(test_slice.index, test_slice.TotalVolume, 'Testing Data')
        half = (slicedf.shape[0] // 400)
        trace3 = makeTrace(slicedf.index[points // 2:], slicedf['TotalVolume'].values[points // 2:], 'Selected Data')
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

#graph 2 is FBProphet Graph
@app.callback(Output('graph2', 'figure'),
                [Input('startdate', 'value'),
                Input('enddate', 'value'),
                Input('points', 'value'),
                Input('floor', 'value'),
                Input('cap', 'value')
                ]

)
# points - how many values to predict going forward
# forecast['ds'] - datestamp
# forecast['yhat'] - pred points
# forecast columns :
# Index(['ds', 'trend', 'cap', 'yhat_lower', 'yhat_upper', 'trend_lower',
#        'trend_upper', 'additive_terms', 'additive_terms_lower',
#        'additive_terms_upper', 'daily', 'daily_lower', 'daily_upper', 'weekly',
#        'weekly_lower', 'weekly_upper', 'yearly', 'yearly_lower',
#        'yearly_upper', 'multiplicative_terms', 'multiplicative_terms_lower',
#        'multiplicative_terms_upper', 'yhat'],
#       dtype='object')
def graph2(startdate, enddate, points, floor, cap):
    print('into graph 2')
    #redefine df to set up for fbprophet
    curdf = pd.read_csv('test_df_w_timeshift.csv')
    #set date string to timestamp
    curdf['Date_IntervalStart'] = pd.to_datetime(curdf['Date_IntervalStart'])
    curdf.rename(columns={'Date_IntervalStart' : 'ds', 'TotalVolume' : 'y'}, inplace=True)
    curdf.dropna(inplace=True)
    #curdf.drop(columns=['week_timeshift'], inplace=True)

    curdf.set_index('ds', inplace=True)
    curdf = curdf[startdate : enddate]
    df_p_hourly = curdf.resample('H').sum()
    df_p_hourly.reset_index(inplace=True)
    m = Prophet(daily_seasonality=True, yearly_seasonality = True, weekly_seasonality = True)
    m.fit(df_p_hourly[['ds', 'y']])
    future = m.make_future_dataframe(periods=points, freq='H')
    future['floor'] = floor
    future['cap'] = cap
    forecast = m.predict(future)
    trace1 = makeTrace(df_p_hourly['ds'].values, df_p_hourly['y'].values, 'Selected Data')
    trace2 = makeTrace(forecast['ds'].values, forecast['yhat'].values, 'Predictions')
    #plot with plotly and integrate into dash

    #date range for predictions
    #list(pd.date_range(dframe.index[-1], periods=points, freq='H'))
    return {
            'data' : [trace1, trace2],#, trace2, trace3],
            'type' : 'scatter',
            'name' : 'FBProphet',
            'layout' : go.Layout(title='FBProphet', barmode='stack')
            }

#helper method for FBProphet callback
def getProphetFrame(frame):

    return m
    #fbFrame = frame.copy()


#LSTM prediction graph
#set up LSTM predictions depending on points
@app.callback(Output('graph3', 'figure'),
                [Input('startdate', 'value'),
                Input('enddate', 'value'),
                Input('points', 'value')
                ]
)# points - how many values to predict going forward
def graph3(startdate, enddate, points):
    dframe = df[startdate : enddate]
    #date range for predictions
    list(pd.date_range(dframe.index[-1], periods=points, freq='H'))
    return None


#create second graph to show fbprophet results
#create third graph to show LSTM results
#add functionality to edit LSTM parameters

app.run_server()#, use_reloader=False , debug=True
