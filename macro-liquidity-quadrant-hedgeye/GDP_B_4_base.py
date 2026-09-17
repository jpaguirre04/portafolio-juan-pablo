# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:45:00 2024

@author: Juan Pablo Aguirre
"""


import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import r2_score, mean_squared_error
import pandas_datareader.data as web
import pandas_datareader
from pandas_datareader import wb
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import *

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import xgboost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

from datetime import datetime, timedelta, date
from typing import Tuple

import scipy as sc
import math
import statsmodels.api as sm

from B_3_base import base, fechag, A


L = web.DataReader(['CPIAUCNS'], 'fred', datetime(1970, 6, 1), datetime.now())
L.columns =  ['cpi']
L = L.reset_index()
L = L.rename(columns = {'DATE': 'date'})
L = L[L['date']>=  A['date'].min()]

L = L[['date']].merge(base, how = 'left', on = 'date')

L = L[L['date']<= A['date'].max()]


L['item0'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item1'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item2'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item3'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item4'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item5'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item6'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item7'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item8'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item9'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item10'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item11'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item12'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item13'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item14'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item15'].interpolate(method = 'polynomial', order= 2, inplace = True)
L['item16'].interpolate(method = 'polynomial', order= 2, inplace = True)




"""
#####--- comprobar la estacionaridad con ADF ---#####
"""

"""
df = L.set_index('date')
df = df.drop('item0',axis=1)
# 9. Verifique la estacionariedad y haga que la serie temporal sea estacionaria



# Import Statsmodels
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

def adfuller_test(series, signif=0.05, name='', verbose=False):
    # Perform ADFuller to test for Stationarity of given series and print report
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
    print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
    print(f' Significance Level    = {signif}')
    print(f' Test Statistic        = {output["test_statistic"]}')
    print(f' No. Lags Chosen       = {output["n_lags"]}')

    for key,val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= signif:
        print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
        print(f" => Series is Stationary.")
    else:
        print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        print(f" => Series is Non-Stationary.") 



# ADF Test on each column
for name, column in df.iteritems():
    adfuller_test(column, name=column.name)
    print('\n')

# 1st difference
df_differenced = df.diff().dropna()

# ADF Test on each column of 1st Differences Dataframe
for name, column in df_differenced.iteritems():
    adfuller_test(column, name=column.name)
    print('\n')

# Second Differencing
df_differenced2 = df_differenced.diff().dropna()

# ADF Test on each column of 2nd Differences Dataframe
for name, column in df_differenced2.iteritems():
    adfuller_test(column, name=column.name)
    print('\n')




# https://www.machinelearningplus.com/time-series/vector-autoregression-examples-python/
# 14. Invierte la transformación para obtener el pronóstico real.
def invert_transformation(df_train, df_forecast, second_diff=False):
    # Revert back the differencing to get the forecast to original scale.
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        # Roll back 2nd Diff
        if second_diff:
            df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1] - df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
        # Roll back 1st Diff
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()
    return df_fc



DF_Train = df_differenced2.reset_index('date')
df_train = DF_Train[DF_Train['date'] < date_list_w['date'].min()]
df_train = df_train.set_index('date')


DF_MERGE = date_list_w.merge(df_merged, how = 'left', on = 'date')
DF_MERGE = DF_MERGE.set_index('date')

df_results = invert_transformation(df_train= df_train, df_forecast= DF_MERGE, second_diff=True)


# L1= df_differenced.fillna(df.iloc[0,0]).cumsum()


df_train['item1'].iloc[-1]

df_train['item1'].iloc[-2]

DF_MERGE['item1'].cumsum()



A1 = (df_train['item1'].iloc[-1] - df_train['item1'].iloc[-2]) + DF_MERGE['item1'].cumsum()

A2 = df_train['item1'].iloc[-1] + A1.cumsum()

"""



# google: stationary  lags consum() python pandas
# https://stackoverflow.com/questions/66559618/differencing-time-series-create-stationary-time-series-pandas

# google: lags diff() cumsum() python pandas
# https://www.geeksforgeeks.org/python-pandas-dataframe-cumsum/
# https://stackoverflow.com/questions/73302817/pandas-cumsum-on-lag-differenced-dataframe


