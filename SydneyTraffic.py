# IMPORTS
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import statsmodels.api as sm
# Load specific forecasting tools
from statsmodels.tsa.ar_model import AR,ARResults
from statsmodels.tsa.seasonal import seasonal_decompose
# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")
folders = []
files = []
#folders
# ED_traffic-data_FY2019_Q1_csv
# ED_trips_2018-07.csv, ED_trips_2018-08.csv, ED_trips_2018-09.csv
# ED_traffic-data_FY2019_Q2_csv
# ED_trips_2018-10.csv	ED_trips_2018-11.csv	ED_trips_2018-12.csv
# ED_traffic-data_FY2019_Q3_csv
# ED_trips_2019-01.csv	ED_trips_2019-02.csv	ED_trips_2019-03.csv
# ED_traffic-data_FY2019_Q4_csv
# ED_trips_2019-04.csv	ED_trips_2019-05.csv	ED_trips_2019-06.csv

# FILES

quarter = ['ED_traffic-data_FY2019_Q3_csv',
           'ED_traffic-data_FY2019_Q4_csv',
           'ED_traffic-data_FY2019_Q1_csv',
           'ED_traffic-data_FY2019_Q2_csv']
files = ['ED_trips_2019-01.csv',
         'ED_trips_2019-02.csv',
         'ED_trips_2019-03.csv',
         'ED_trips_2019-04.csv',
         'ED_trips_2019-05.csv',
         'ED_trips_2019-06.csv',
         'ED_trips_2018-07.csv',
         'ED_trips_2018-08.csv',
         'ED_trips_2018-09.csv',
         'ED_trips_2018-10.csv',
         'ED_trips_2018-11.csv',
         'ED_trips_2018-12.csv']
dataframes = []
aug = 0
1,2,3, 4,5,6, 7,8,9, 10,11,12
for q in quarter:
    for z in range(3):
        print((aug * 3) + (z + 1))
        filename = q + '/' + files[(aug * 3) + (z)]
        print(filename)
        dataframes.append(
             pd.read_csv(filename)
             )
    aug += 1


dfs = clean_dfs(dataframes, 'Truck')
df_all = dfs[0].append(dfs[1])
dataframes[0].shape
dataf = dfs[0]
for d in dataframes[1:]:
    dataf = dataf.append(d)
dataf.shape

df_will = dataf[dataf['GantryLocation'] == 'William Street North-bound exit ramp']
df_wool = dataf[dataf['GantryLocation'] == 'Woolloomooloo Toll Plaza North-bound']

df_wool['Date'] = pd.to_datetime(df_wool['Date'] + 'T' + df_wool['IntervalStart'])
df_will['Date'] = pd.to_datetime(df_will['Date'] + 'T' + df_will['IntervalStart'])

df_wool.set_index(df_wool['Date'], inplace = True)
df_will.set_index('Date', inplace = True)
#CLEAN METHODS

def clean_dfs(dataframe_list, desired_vehicle):
    clean_dataframe_list = []
    cols_to_remove = ['AssetID', "FinancialQtrID", "Version", "GantryDirection", "GantryType",
                  "GantryGPSLatitude", "GantryGPSLongitude"]
    for dataframe in dataframe_list:
        dataframe.drop(columns = cols_to_remove, inplace=True)
        dataframe_only_desired_vehicle = dataframe[dataframe['VehicleClass'] == desired_vehicle]
        clean_dataframe_list.append(dataframe_only_desired_vehicle)
    return clean_dataframe_list


# Create a function to check for the stationarity of a given time series using rolling stats and DF test
# Collect and package the code from previous labs

def stationarity_check(TS, column = 'TotalVolume'):

    # Import adfuller
    from statsmodels.tsa.stattools import adfuller

    # Calculate rolling statistics
    roll_mean = TS.rolling(window=8, center=False).mean()
    roll_std = TS.rolling(window=8, center=False).std()

    # Perform the Dickey Fuller Test
    dftest = adfuller(TS[column])

    # Plot rolling statistics:
    fig = plt.figure(figsize=(12,6))
    plt.plot(TS, color='blue',label='Original')
    plt.plot(roll_mean, color='red', label='Rolling Mean')
    plt.plot(roll_std, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)

    # Print Dickey-Fuller test results
    print('Results of Dickey-Fuller Test: \n')

    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value',
                                             '#Lags Used', 'Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

    return None


# DECOMPOSITION

decomposition = seasonal_decompose(np.log(ts))
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid


# Plot gathered statistics
plt.figure(figsize=(12,8))
plt.subplot(411)
plt.plot(np.log(ts), label='Original', color='blue')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend', color='blue')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality', color='blue')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals', color='blue')
plt.legend(loc='best')
plt.tight_layout()


rolling_mean = df_will_DH['TotalVolume'].rolling(window=8, center=False).mean()
rolling_std = df_will_DH['TotalVolume'].rolling(window=8, center=False).std()

rolling_mean.dropna(inplace=True)
rolling_std.dropna(inplace=True)
