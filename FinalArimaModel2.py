"""
    Program: FinalArimaModel.py
    Author:  Alyssa Fedgo
    Date:    06-07-2021
    Purpose: Feature Selection
"""

import pandas as pd
from matplotlib import pyplot
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import csv
import pmdarima as pm
import warnings


warnings.filterwarnings('ignore')

#input data and split into region and then test and train

df=pd.read_csv('Dataframe Outliers.csv')
df_forecast=pd.read_csv('Weather Test.csv')

coast=df[df['region']=='Coast']
coast.set_index(['date'],inplace=True)
coast_test=df_forecast[df_forecast['region']=='Coast']
coast_test.set_index(['date'],inplace=True)
coast_y_train=coast[['ercotNew']].tail(13149)
coast_x_train=coast[['DewPointCNew']].tail(13149)
coast_x_test=coast_test[['DewPointCNew']]

east=df[df['region']=='East']
east.set_index(['date'],inplace=True)
east_test=df_forecast[df_forecast['region']=='East']
east_test.set_index(['date'],inplace=True)
east_y_train=east[['ercotNew']]
east_x_train=east[['pressureNew']]
east_x_test=east_test[['pressureNew']]

far_west=df[df['region']=='Far West']
far_west.set_index(['date'],inplace=True)
far_west_test=df_forecast[df_forecast['region']=='Far West']
far_west_test.set_index(['date'],inplace=True)
far_west_y_train=far_west[['ercotNew']]
far_west_x_train=far_west[['humidityNew','WindGustMilesNew']]
far_west_x_test=far_west_test[['humidityNew','WindGustMilesNew']]

north=df[df['region']=='North']
north.set_index(['date'],inplace=True)
north_test=df_forecast[df_forecast['region']=='North']
north_test.set_index(['date'],inplace=True)
north_y_train=north[['ercotNew']].tail(13149)
north_x_train=north[['humidityNew']].tail(13149)
north_x_test=north_test[['humidityNew']]

north_central=df[df['region']=='North Central']
north_central.set_index(['date'],inplace=True)
north_central_test=df_forecast[df_forecast['region']=='North Central']
north_central_test.set_index(['date'],inplace=True)
north_central_y_train=north_central[['ercotNew']]
north_central_x_train=north_central[['humidityNew','FeelsLikeCNew','WindChillCNew','tempCNew',
                                     'weatherCodeNew','visibilityNew']]
north_central_x_test=north_central_test[['humidityNew','FeelsLikeCNew','WindChillCNew','tempCNew',
                                     'weatherCodeNew','visibilityNew']]

south=df[df['region']=='South']
south.set_index(['date'],inplace=True)
south_test=df_forecast[df_forecast['region']=='South']
south_test.set_index(['date'],inplace=True)
south_y_train=south[['ercotNew']].tail(13149)
south_x_train=south[['pressureNew','HeatIndexCNew']].tail(13149)
south_x_test=south_test[['pressureNew','HeatIndexCNew']]

south_central=df[df['region']=='South Central']
south_central.set_index(['date'],inplace=True)
south_central_test=df_forecast[df_forecast['region']=='South Central']
south_central_test.set_index(['date'],inplace=True)
south_central_y_train=south_central[['ercotNew']]
south_central_x_train=south_central[['FeelsLikeCNew']]
south_central_x_test=south_central_test[['FeelsLikeCNew']]

west=df[df['region']=='West']
west.set_index(['date'],inplace=True)
west_test=df_forecast[df_forecast['region']=='West']
west_test.set_index(['date'],inplace=True)
west_y_train=west[['ercotNew']]
west_x_train=west[['uvIndexNew']]
west_x_test=west_test[['uvIndexNew']]




#ARIMA/SARIMA models for each region


mod = sm.tsa.statespace.SARIMAX(coast_y_train,order=(1,1,1),seasonal_order=(1,1,1,24),
                                exog=coast_x_train, enforce_stationarity=False, enforce_invertibility=False)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=coast_x_test)
forecast1 = pred_uc.predicted_mean

coast_fore=pd.DataFrame({'Date':forecast1.index,'Coast':forecast1.values})

print('Coast')


mod = ARIMA(east_y_train,order=(5,0,1),exog=east_x_train)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=east_x_test)
forecast2 = pred_uc.predicted_mean


east_fore=pd.DataFrame({'Date':forecast2.index,'East':forecast2.values})

print('East')


mod = ARIMA(far_west_y_train,order=(3,0,1),exog=far_west_x_train)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=far_west_x_test)
forecast3 = pred_uc.predicted_mean

far_west_fore=pd.DataFrame({'Date':forecast3.index,'Far_West':forecast3.values})

print('FW')



mod = sm.tsa.statespace.SARIMAX(north_y_train,order=(2,1,0),seasonal_order=(2,1,0,24),
                                exog=north_x_train, enforce_stationarity=False, enforce_invertibility=False)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=north_x_test)
forecast4 = pred_uc.predicted_mean

north_fore=pd.DataFrame({'Date':forecast4.index,'North':forecast4.values})


print('North')


mod = ARIMA(north_central_y_train,order=(4,0,4),exog=north_central_x_train)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=north_central_x_test)
forecast5 = pred_uc.predicted_mean

north_central_fore=pd.DataFrame({'Date':forecast5.index,'North_Central':forecast5.values})

print('NC')

mod = sm.tsa.statespace.SARIMAX(south_y_train,order=(2,1,0),seasonal_order=(2,1,0,24),
                                exog=south_x_train, enforce_stationarity=False, enforce_invertibility=False)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=south_x_test)
forecast6 = pred_uc.predicted_mean

south_fore=pd.DataFrame({'Date':forecast6.index,'South':forecast6.values})


print('South')


mod = ARIMA(south_central_y_train,order=(5,0,1),exog=south_central_x_train)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=south_central_x_test)
forecast7 = pred_uc.predicted_mean

south_central_fore=pd.DataFrame({'Date':forecast7.index,'South_Central':forecast7.values})


print('SC')


mod = ARIMA(west_y_train,order=(3,0,1),exog=west_x_train)

results=mod.fit()
pred_uc = results.get_forecast(steps=193,exog=west_x_test)
forecast8 = pred_uc.predicted_mean

west_fore=pd.DataFrame({'Date':forecast8.index,'West':forecast8.values})
print('West')

# compile the list of dataframes you want to merge
data_frames = [coast_fore, east_fore, far_west_fore,north_fore, north_central_fore, south_fore,
               south_central_fore,west_fore]
df_merged =  pd.merge(coast_fore,east_fore,on=['Date'],how='inner')
df_merged2 =  pd.merge(df_merged,far_west_fore,on=['Date'],how='inner')
df_merged3 =  pd.merge(df_merged2,north_fore,on=['Date'],how='inner')
df_merged4 =  pd.merge(df_merged3,north_central_fore,on=['Date'],how='inner')
df_merged5 =  pd.merge(df_merged4,south_fore,on=['Date'],how='inner')
df_merged6 =  pd.merge(df_merged5,south_central_fore,on=['Date'],how='inner')
df_merged7 =  pd.merge(df_merged6,west_fore,on=['Date'],how='inner')



df_merged7.to_csv('Submission.csv')
