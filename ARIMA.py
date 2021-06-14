"""
    Program: ARIMA.py
    Author:  Alyssa Fedgo
    Date:    05-29-2021
    Purpose: Use ARIMA and VARs models to predict electric load
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

df=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Dataframe Outliers.csv')



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

if choice==1:
    p=3
    q=2
    p_=3
    q_=1
    s_p=1
    s_d=1
    s_q=1
elif choice==2:
    p=5
    q=1
    p_=3
    q_=0
    s_p=2
    s_d=1
    s_q=0
elif choice==3:
    p=3
    q=1
    p_=1
    q_=2
    s_p=2
    s_d=1
    s_q=0
elif choice==4:
    p=5
    q=1
    p_=2
    q_=0
    s_p=2
    s_d=1
    s_q=0
elif choice==5:
    p=4
    q=4
    p_=3
    q_=1
    s_p=2
    s_d=1
    s_q=0
elif choice==6:
    p=5
    q=1
    p_=2
    q_=0
    s_p=2
    s_d=1
    s_q=0
elif choice==7:
    p=5
    q=1
    p_=3
    q_=1
    s_p=0
    s_d=1
    s_q=1
else:
    p=3
    q=1
    p_=3
    q_=0
    s_p=2
    s_d=1
    s_q=0  

region_choice=region_dict[choice]

region_df=df[df['region']==region_choice]


series_region=region_df[['date','ercotNew']]

series_short=region_df.groupby('region').tail(8766)[['date','ercotNew']]

series_region.set_index(['date'],inplace=True)
series_short.set_index(['date'],inplace=True)


# split into train and test sets

size_a = int(len(series_region['ercotNew']))-168
size_b = int(len(series_short['ercotNew']))-168


tra_a = series_region['ercotNew'][0:size_a]
tes_a = series_region['ercotNew'][size_a:len(series_region)]


tra_b = series_short['ercotNew'][0:size_b]
tes_b = series_short['ercotNew'][size_b:]

tr_end=tes_a.index.min()
te_end=tes_a.index.max()




model = ARIMA(series_region, order=(p,0,q))
model_fit = model.fit()
pred = model_fit.get_prediction(start=tr_end, dynamic=False)
y_forecasted = pred.predicted_mean
rmse = sqrt(mean_squared_error(tes_a, y_forecasted))

print('ARIMA model MSE:{}'.format(rmse))


model = ARIMA(tra_a, order=(p,0,q))
model_fit = model.fit()
pred_uc = model_fit.get_forecast(steps=168)
forecast = pred_uc.predicted_mean
rmse2 = sqrt(mean_squared_error(tes_a, forecast))
print('ARIMA model MSE:{}'.format(rmse2))




mod = sm.tsa.statespace.SARIMAX(series_short,order=(p_,1,q_),seasonal_order=(s_p,s_d,s_q,24),
                                enforce_stationarity=False, enforce_invertibility=False)

results=mod.fit()
pred = results.get_prediction(start=tr_end, dynamic=False)
y_forecasted = pred.predicted_mean
rmse3 = sqrt(mean_squared_error(tes_b, y_forecasted))

print('SARIMA model MSE:{}'.format(rmse3))

mod = sm.tsa.statespace.SARIMAX(tra_b,order=(p_,1,q_),seasonal_order=(s_p,s_d,s_q,24),
                                enforce_stationarity=False, enforce_invertibility=False)

results=mod.fit()
pred_uc = results.get_forecast(steps=168)
forecast = pred_uc.predicted_mean
rmse4 = sqrt(mean_squared_error(tes_b, forecast))

print('SARIMA model MSE:{}'.format(rmse4))



a_file=open("rmse ARIMA.csv","a",newline='')
writer=csv.writer(a_file)

writer.writerow([region_choice + ' ' + str(rmse) + " " + str(rmse2)+ " " + str(rmse3)+ " " + str(rmse4)])

a_file.close()
