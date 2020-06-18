#Trevor O'Hearn
#6/18/2020
#Analysis for Sydney Traffic Data
#cleaned and analyzed for the FrontEnd

#imports
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
import seaborn as sns
import statsmodels.api as sm
import glob
# Load specific forecasting tools
from statsmodels.tsa.arima_model import ARMA, ARIMA
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.ar_model import AR,ARResults
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from sklearn.metrics import mean_squared_error
from matplotlib.pylab import rcParams
from pmdarima import auto_arima
# Ignore harmless warnings
import warnings
warnings.filterwarnings("ignore")


#methods
# function to get all of the files
def get_all_dataframes(path_to_data_folder):
    # give the path and this function will return all of the dataframes in a sorted list
    original_data = glob.glob(path_to_data_folder + "/*/*.csv",recursive=True)
    test_dataframe_list = []
    training_dataframe_list = []
    for item in original_data:
        with open(item) as f:
            df = pd.read_csv(f, parse_dates=[['Date', 'IntervalStart']], index_col = 'Date_IntervalStart')
            if "2020" in str(f):
                test_dataframe_list.append(df)
            else:
                training_dataframe_list.append(df)
    return test_dataframe_list, training_dataframe_list

# function to clean the dataframe list
def clean_dfs(dataframe_list):
    clean_dataframe_list = []
    for df in dataframe_list:
        df_C = df[df['TollPointID'] == 'C']
        df_grouped = pd.DataFrame(df_C.groupby('Date_IntervalStart').TotalVolume.sum())
        clean_dataframe_list.append(df_grouped)
    return clean_dataframe_list

def isBusiness(x, morning=6, evening=19):
    if x in range(morning, evening):
        return 1
    else:
        return 0

from statsmodels.tsa.stattools import adfuller
def stationarity_check(TS, window = 364 * 4, column = 'TotalVolume'):

    # Import adfuller
    from statsmodels.tsa.stattools import adfuller

    # Calculate rolling statistics
    roll_mean = TS.rolling(window=window, center=False).mean()
    roll_std = TS.rolling(window=window, center=False).std()

    # Perform the Dickey Fuller Test
    dftest = adfuller(TS[column])

    # Plot rolling statistics:
    fig = plt.figure(figsize=(12,6))
    #plt.plot(TS, color='blue',label='Original')
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

def test_stationarity(timeseries, window):

    #Determing rolling statistics
    rolmean = timeseries.rolling(window=window).mean()
    rolstd = timeseries.rolling(window=window).std()

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries.iloc[window:], color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)





# import files
if user_directory != None:    #i.e.: use the directory given
    test_df_list, train_df_list = get_all_dataframes(user_directory)
else:    # point to my directory
    test_df_list, train_df_list = get_all_dataframes("./eastern_distrib")


# training dataframes
clean_train_df_list = clean_dfs(train_df_list)
# test dataframes
clean_test_df_list = clean_dfs(test_df_list)

train_df = pd.concat(clean_df_list)
test_df = pd.concat(clean_test_df_list)

# resampling days in a new dataframe
train_df_days = train_df.resample('d').sum()

# resampling to the hour in the train dataframe
train_df = train_df.resample('H').sum()

train_df['week_diff'] = train_df['TotalVolume'] - train_df.TotalVolume.shift((7*24))

train_df.dropna(inplace=True)

train_df['ShiftDay'] = train_df['TotalVolume'].shift(periods=24)
train_df['ShiftWeek'] = train_df['TotalVolume'].shift(periods=7*24)
train_df['DiffWeek'] = train_df['TotalVolume'] - train_df['ShiftWeek']
test_df['ShiftWeek'] = test_df['TotalVolume'].shift(periods=7*24)
test_df['DiffWeek'] = test_df['TotalVolume'] - test_df['ShiftWeek']
test_df['ShiftWeek'].dropna().index[0] #2019-07-08 00:00:00
train_df['hour'] = train_df.index.hour
test_df['hour'] = test_df.index.hour
train_df['isBusinessHour'] = train_df['hour'].apply(isBusiness)
test_df['isBusinessHour'] = test_df['hour'].apply(isBusiness)
