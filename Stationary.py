"""
    Program Name: Stationary.py
    Author:       Alyssa Fedgo
    Date:         May 24, 2021
    Project:      WiDS 2021 Texas
    Purpose:      Statistically model time series data with ARIMA
"""


import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from scipy import signal
import warnings

warnings.filterwarnings('ignore')


#Read in file

df=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Dataframe Outliers.csv',parse_dates=['Date_string'])

"""create the different coast data frames and make date an index"""

coast=df[df['region'] == 'Coast']
coast.index = coast.Date_string

east=df[df['region'] == 'East']
east.index = east.Date_string

far_west=df[df['region'] == 'Far West']
far_west.index = far_west.Date_string

north=df[df['region'] == 'North']
north.index = north.Date_string

north_central=df[df['region'] == 'North Central']
north_central.index = north_central.Date_string

south=df[df['region'] == 'South']
south.index = south.Date_string

south_central=df[df['region'] == 'South Central']
south_central.index = south_central.Date_string

west=df[df['region'] == 'West']
west.index = west.Date_string


adf_results=np.zeros((20,8),bool)
kpss_results=np.zeros((20,8),bool)
i=0
j=0


#test for stationary

def adf_test(timeseries):
    #Perform Dickey-Fuller test:
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput['Critical Value (%s)'%key] = value
    if dfoutput['Test Statistic'] > dfoutput['Critical Value (5%)']:
        adf_results[i][j]=True
    else: adf_results[i][j]=False
    print (dfoutput)

#define function for kpss test

#define KPSS
def kpss_test(timeseries):
    kpsstest = kpss(timeseries, regression='c',nlags="legacy")
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    if kpss_output['Test Statistic'] > kpss_output['Critical Value (5%)']:
        kpss_results[i][j]=True
    else: kpss_results[i][j]=False
    print (kpss_output)

#apply adf and kpss on the series

selected_cols=['ercotNew','Covid_Confirmed','Covid_Confirmed_Change','Covid_Death','Covid_Death_Change',
               'tempCNew','windspeedMilesNew','winddirDegreeNew','weatherCodeNew','precipMMNew',
               'humidityNew','visibilityNew','pressureNew','cloudcoverNew','HeatIndexCNew',
               'DewPointCNew','WindChillCNew','WindGustMilesNew','FeelsLikeCNew','uvIndexNew']


for cols in selected_cols:
    print ('Results of Dickey-Fuller Test: {} in Coast'.format(cols))
    adf_test(coast[cols])
    print ('Results of KPSS Test: {} in Coast'.format(cols))
    kpss_test(coast[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in East'.format(cols))
    adf_test(east[cols])
    print ('Results of KPSS Test: {} in East'.format(cols))
    kpss_test(east[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in Far West'.format(cols))
    adf_test(far_west[cols])
    print ('Results of KPSS Test: {} in Far West'.format(cols))
    kpss_test(far_west[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in North'.format(cols))
    adf_test(north[cols])
    print ('Results of KPSS Test: {} in North'.format(cols))
    kpss_test(north[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in North Central'.format(cols))
    adf_test(north_central[cols])
    print ('Results of KPSS Test: {} in North Central'.format(cols))
    kpss_test(north_central[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in South'.format(cols))
    adf_test(south[cols])
    print ('Results of KPSS Test: {} in South'.format(cols))
    kpss_test(south[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in South Central'.format(cols))
    adf_test(south_central[cols])
    print ('Results of KPSS Test: {} in South Central'.format(cols))
    kpss_test(south_central[cols])
    j+=1
    print ('Results of Dickey-Fuller Test: {} in West'.format(cols))
    adf_test(west[cols])
    print ('Results of KPSS Test: {} in West'.format(cols))
    kpss_test(west[cols])
    j=0
    i+=1

#Differencing if KPSS shows not stationary or detrending if ADF shows not stationary

x=0
for col in selected_cols:
    if (kpss_results[x][0]==True):
        coast[col + "Diff"] = coast[col].diff()
    elif (adf_results[x][0]==True and kpss_results[x][0]==False):
        coast[col+"Diff"] = signal.detrend(coast[col].values)
    else: coast[col+"Diff"]=coast[col]

    if (kpss_results[x][1]==True):
        east[col+"Diff"] = east[col].diff()
    elif (adf_results[x][1]==True and kpss_results[x][1]==False):
        east[col+"Diff"] = signal.detrend(east[col].values)
    else: east[col+"Diff"]=east[col]

    if (kpss_results[x][2]==True):
        far_west[col+"Diff"] = far_west[col].diff()
    elif (adf_results[x][2]==True and kpss_results[x][2]==False):
        far_west[col+"Diff"] = signal.detrend(far_west[col].values)
    else: far_west[col+"Diff"]=far_west[col]
  
    if (kpss_results[x][3]==True):
        north[col+"Diff"] = north[col].diff()
    elif (adf_results[x][3]==True and kpss_results[x][3]==False):
        north[col+"Diff"] = signal.detrend(north[col].values)
    else: north[col+"Diff"]=north[col]

    if (kpss_results[x][4]==True):
        north_central[col+"Diff"] = north_central[col].diff()
    elif (adf_results[x][4]==True and kpss_results[x][4]==False):
        north_central[col+"Diff"] = signal.detrend(north_central[col].values)
    else: north_central[col+"Diff"]=north_central[col]

    if (kpss_results[x][5]==True):
        south[col+"Diff"] = south[col].diff()
    elif (adf_results[x][5]==True and kpss_results[x][5]==False):
        south[col+"Diff"] = signal.detrend(south[col].values)
    else: south[col+"Diff"]=south[col]

    if (kpss_results[x][6]==True):
        south_central[col+"Diff"] = south_central[col].diff()
    elif (adf_results[x][6]==True and kpss_results[x][6]==False):
        south_central[col+"Diff"] = signal.detrend(south_central[col].values)
    else: south_central[col+"Diff"]=south_central[col]

    if (kpss_results[x][7]==True):
        west[col+"Diff"] = west[col].diff()
    elif (adf_results[x][7]==True and kpss_results[x][7]==False):
        west[col+"Diff"] = signal.detrend(west[col].values)
    else:
        west[col+"Diff"]=west[col]
    x=x+1



print(adf_results)
print(kpss_results)

#Convert to data frame

adf_df = pd.DataFrame(adf_results)
kpss_df = pd.DataFrame(kpss_results)

#Combine to make full data frame

frames=[coast,east,far_west,north,north_central,south,south_central,west]
df_new=pd.concat(frames)

# Fill in nulls

cols=['Date_string','region','gdp','density','ercotNewDiff','Covid_ConfirmedDiff','Covid_Confirmed_ChangeDiff',
          'Covid_DeathDiff','Covid_Death_ChangeDiff','tempCNewDiff','windspeedMilesNewDiff','winddirDegreeNewDiff',
          'weatherCodeNewDiff','precipMMNewDiff','humidityNewDiff','visibilityNewDiff','pressureNewDiff',
          'cloudcoverNewDiff','HeatIndexCNewDiff','DewPointCNewDiff','WindChillCNewDiff','WindGustMilesNewDiff',
          'FeelsLikeCNewDiff','uvIndexNewDiff']


for i in cols:
  df_new[i]=df_new[i].fillna(0)
    
# Export to csv

df_new.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Dataframe Stationary.csv')
adf_df.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\ADF.csv')
kpss_df.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\KPSS.csv')
    
   
    



