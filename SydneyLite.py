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



# import files
if user_directory != None:    #i.e.: use the directory given
    test_df_list, train_df_list = get_all_dataframes(user_directory)
else:    # point to my directory
    test_df_list, train_df_list = get_all_dataframes("./eastern_distrib")
