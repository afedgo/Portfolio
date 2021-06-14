"""
    Program: FeatureSelection.py
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
    model='SARIMA'
elif choice==2:
    p=5
    q=1
    p_=3
    q_=0
    s_p=2
    s_d=1
    s_q=0
    model='ARIMA'
elif choice==3:
    p=3
    q=1
    p_=1
    q_=2
    s_p=2
    s_d=1
    s_q=0
    model='ARIMA'
elif choice==4:
    p=5
    q=1
    p_=2
    q_=0
    s_p=2
    s_d=1
    s_q=0
    model='SARIMA'
elif choice==5:
    p=4
    q=4
    p_=3
    q_=1
    s_p=2
    s_d=1
    s_q=0
    model='ARIMA'
elif choice==6:
    p=5
    q=1
    p_=2
    q_=0
    s_p=2
    s_d=1
    s_q=0
    model='SARIMA'
elif choice==7:
    p=5
    q=1
    p_=3
    q_=1
    s_p=0
    s_d=1
    s_q=1
    model='ARIMA'
else:
    p=3
    q=1
    p_=3
    q_=0
    s_p=2
    s_d=1
    s_q=0
    model='ARIMA'

region_choice=region_dict[choice]

df_region=df[df['region']==region_choice]
df_region.set_index(['date'],inplace=True)

size = int(len(df_region['ercotNew']))-168
y_train=df_region[['ercotNew']][0:size]
y_test=df_region[['ercotNew']][size:]

#DewPointCNew lowered the RMSE the most in Coast. Taken out of features and added in model
#pressureNew lowered the RMSE the most in East. Taken out of features and added in model
#humidityNew lowered the RMSE the most in Far West. Taken out of features and added in model
features=['windspeedMilesNew','winddirDegreeNew','precipMMNew','cloudcoverNew','HeatIndexCNew',
          'DewPointCNew','WindGustMilesNew','pressureNew', 'FeelsLikeCNew',
          'visibilityNew','weatherCodeNew','tempCNew','WindChillCNew','humidityNew']

min_rmse=5000
var_rmse='empty'
    
if model=='SARIMA':
    short_y_train=y_train.tail(8766)
    

    for col in features:
        x_train=df_region[0:size].tail(8766)[[col]]
        x_test=df_region[size:][[col]]

        mod = sm.tsa.statespace.SARIMAX(short_y_train,order=(p_,1,q_),seasonal_order=(s_p,s_d,s_q,24),
                                exog=x_train, enforce_stationarity=False, enforce_invertibility=False)
        results=mod.fit()
        pred_uc = results.get_forecast(steps=168,exog=x_test)
        forecast = pred_uc.predicted_mean
        rmse = sqrt(mean_squared_error(y_test, forecast))
        if rmse< min_rmse:
            min_rmse=rmse
            var_rmse=col
        print('SARIMA model MSE ({}):{}'.format(col,rmse))
    print('min rmse model ({}):{}'.format(var_rmse,min_rmse))

else:

    for col in features:
        x_train=df_region[0:size][['uvIndexNew',col]]
        x_test=df_region[size:][['uvIndexNew',col]]

        mod = ARIMA(y_train,order=(p,0,q),
                                exog=x_train)
        results=mod.fit()
        pred_uc = results.get_forecast(steps=168,exog=x_test)
        forecast = pred_uc.predicted_mean
        rmse = sqrt(mean_squared_error(y_test, forecast))
        if rmse< min_rmse:
            min_rmse=rmse
            var_rmse=col
        print('ARIMA model MSE ({}):{}'.format(col,rmse))
    print('min rmse model ({}):{}'.format(var_rmse,min_rmse))



a_file=open("rmse features selection.csv","a",newline='')
writer=csv.writer(a_file)

writer.writerow([region_choice + ' ' + var_rmse + str(min_rmse)])

a_file.close()
