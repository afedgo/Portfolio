"""
    Program: ModelTesting.py
    Author:  Alyssa Fedgo
    Date:    June 3, 2021
    Purpose: Find the best multivariate model for ERCOT data
    """

#import required packages
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from numpy import log
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm

region_dict={
  1:'Coast',
  2:'East',
  3:'Far West',
  4:'North',
  5:'North Central',
  6:'South',
  7:'South Central',
  8:'West'
  }

choice=int(input("""Enter number choice for region: \n 1 for Coast \n 2 for East \n 3 for Far West \n 4 for North \n 5 for North Central \n 6 for South \n 7 for South Central \n 8 for West \n """))

#read the data
in_df = pd.read_csv("Dataframe Outliers.csv", parse_dates=['date'])

region_choice=region_dict[choice]

region_df=in_df[in_df['region']==region_choice]

df = region_df.tail(750)
df['ercot']=df['ercotNew'].astype(int)

full=region_df[['date','ercotNew']]

short=df[['date','ercot']]




model = pm.auto_arima(full[['ercotNew']], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=5, max_q=5, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)

print(model.summary())



# Seasonal - fit stepwise auto-ARIMA

smodel = pm.auto_arima(short[['ercot']], start_p=1, start_q=1,
                           test='adf',
                           max_p=3, max_q=3, m=24,
                           start_P=0, seasonal=True,
                           d=None, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
 
smodel.summary()








