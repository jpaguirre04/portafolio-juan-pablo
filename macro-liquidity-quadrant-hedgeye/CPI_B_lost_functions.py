# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:02:45 2024

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


import warnings

# Esto suprime todas las FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)


import pmdarima
import pmdarima as pm
import arch

# https://www.geeksforgeeks.org/weighted-least-squares-regression-in-python/


# pronósticos para las variables independientes o características
# ocho variables en series de tiempo 

"""
###--- MODELOS ARIMA ---#### 
"""

def Arima1(T1, program_H1, d, seasonal):
        train1 = T1[['date', d]].set_index('date')
        test1 = program_H1[['date']].set_index('date')
        # Fit your model
        model1 = pm.auto_arima(train1, seasonal =seasonal, m=12)
        # make your forecasts
        pred1 = model1.predict(test1.shape[0])       
        prediccion_1  = pred1.to_frame()
        prediccion_1 = prediccion_1.reset_index()
        prediccion_1 = prediccion_1.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_1[d]


def Arima2(T2, program_H2, d, seasonal):
        train2 = T2[['date', d]].set_index('date')
        test2 = program_H2[['date']].set_index('date')
        # Fit your model
        model2 = pm.auto_arima(train2, seasonal=seasonal, m=12)
        # make your forecasts
        pred2 = model2.predict(test2.shape[0])       
        prediccion_2  = pred2.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]


def Arima3(T3, program_H3, d, seasonal):
        train3 = T3[['date', d]].set_index('date')
        test3 = program_H3[['date']].set_index('date')
        # Fit your model
        model3 = pm.auto_arima(train3, seasonal=seasonal, m=12)
        # make your forecasts
        pred3 = model3.predict(test3.shape[0])       
        prediccion_3  = pred3.to_frame()
        prediccion_3 = prediccion_3.reset_index()
        prediccion_3 = prediccion_3.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_3[d]


def Arima4(T4, program_H4, d, seasonal):
        train4 = T4[['date', d]].set_index('date')
        test4 = program_H4[['date']].set_index('date')
        # Fit your model
        model4 = pm.auto_arima(train4, seasonal=seasonal, m=12)
        # make your forecasts
        pred4 = model4.predict(test4.shape[0])       
        prediccion_4  = pred4.to_frame()
        prediccion_4 = prediccion_4.reset_index()
        prediccion_4 = prediccion_4.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_4[d]



def Arima5(T5, program_H5, d, seasonal):
        train5 = T5[['date', d]].set_index('date')
        test5 = program_H5[['date']].set_index('date')
        # Fit your model
        model5 = pm.auto_arima(train5, seasonal=seasonal, m=12)
        # make your forecasts
        pred5 = model5.predict(test5.shape[0])       
        prediccion_5 = pred5.to_frame()
        prediccion_5 = prediccion_5.reset_index()
        prediccion_5 = prediccion_5.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_5[d]



def Arima6(T6, program_H6, d, seasonal):
        train6 = T6[['date', d]].set_index('date')
        test6 = program_H6[['date']].set_index('date')
        # Fit your model
        model6 = pm.auto_arima(train6, seasonal=seasonal, m=12)
        # make your forecasts
        pred6 = model6.predict(test6.shape[0])       
        prediccion_6 = pred6.to_frame()
        prediccion_6 = prediccion_6.reset_index()
        prediccion_6 = prediccion_6.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_6[d]



def Arima7(T7, program_H7, d, seasonal):
        train7 = T7[['date', d]].set_index('date')
        test7 = program_H7[['date']].set_index('date')
        # Fit your model
        model7 = pm.auto_arima(train7, seasonal=seasonal, m=12)
        # make your forecasts
        pred7 = model7.predict(test7.shape[0])       
        prediccion_7 = pred7.to_frame()
        prediccion_7 = prediccion_7.reset_index()
        prediccion_7 = prediccion_7.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_7[d]


def Arima8(T8, program_H8, d, seasonal):
        train8 = T8[['date', d]].set_index('date')
        test8 = program_H8[['date']].set_index('date')
        # Fit your model
        model8 = pm.auto_arima(train8, seasonal=seasonal, m=12)
        # make your forecasts
        pred8 = model8.predict(test8.shape[0])       
        prediccion_8 = pred8.to_frame()
        prediccion_8 = prediccion_8.reset_index()
        prediccion_8 = prediccion_8.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_8[d]


def Arima9(T9, program_H9, d, seasonal):
        train9 = T9[['date', d]].set_index('date')
        test9 = program_H9[['date']].set_index('date')
        # Fit your model
        model9 = pm.auto_arima(train9, seasonal=seasonal, m=12)
        # make your forecasts
        pred9 = model9.predict(test9.shape[0])       
        prediccion_9 = pred9.to_frame()
        prediccion_9 = prediccion_9.reset_index()
        prediccion_9 = prediccion_9.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_9[d]



def Arima10(T10, program_H10, d, seasonal):
        train10 = T10[['date', d]].set_index('date')
        test10 = program_H10[['date']].set_index('date')
        # Fit your model
        model10 = pm.auto_arima(train10, seasonal=seasonal, m=12)
        # make your forecasts
        pred10 = model10.predict(test10.shape[0])       
        prediccion_10  = pred10.to_frame()
        prediccion_10 = prediccion_10.reset_index()
        prediccion_10 = prediccion_10.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_10[d]



def Arima11(T11, program_H11, d, seasonal):
        train11 = T11[['date', d]].set_index('date')
        test11 = program_H11[['date']].set_index('date')
        # Fit your model
        model11 = pm.auto_arima(train11, seasonal=seasonal, m=12)
        # make your forecasts
        pred11 = model11.predict(test11.shape[0])       
        prediccion_11  = pred11.to_frame()
        prediccion_11 = prediccion_11.reset_index()
        prediccion_11 = prediccion_11.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_11[d]


def Arima12(T12, program_H12, d, seasonal):
        train12 = T12[['date', d]].set_index('date')
        test12 = program_H12[['date']].set_index('date')
        # Fit your model
        model12 = pm.auto_arima(train12, seasonal=seasonal, m=12)
        # make your forecasts
        pred12 = model12.predict(test12.shape[0])       
        prediccion_12  = pred12.to_frame()
        prediccion_12 = prediccion_12.reset_index()
        prediccion_12 = prediccion_12.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_12[d]



def Arima13(T13, program_H13, d, seasonal):
        train13 = T13[['date', d]].set_index('date')
        test13 = program_H13[['date']].set_index('date')
        # Fit your model
        model13 = pm.auto_arima(train13, seasonal=seasonal, m=12)
        # make your forecasts
        pred13 = model13.predict(test13.shape[0])       
        prediccion_13  = pred13.to_frame()
        prediccion_13 = prediccion_13.reset_index()
        prediccion_13 = prediccion_13.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_13[d]



def Arima14(T14, program_H14, d, seasonal):
        train14 = T14[['date', d]].set_index('date')
        test14 = program_H14[['date']].set_index('date')
        # Fit your model
        model14 = pm.auto_arima(train14, seasonal=seasonal, m=12)
        # make your forecasts
        pred14 = model14.predict(test14.shape[0])       
        prediccion_14  = pred14.to_frame()
        prediccion_14 = prediccion_14.reset_index()
        prediccion_14 = prediccion_14.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_14[d]



def Arima15(T15, program_H15, d, seasonal):
        train15 = T15[['date', d]].set_index('date')
        test15 = program_H15[['date']].set_index('date')
        # Fit your model
        model15 = pm.auto_arima(train15, seasonal=seasonal, m=12)
        # make your forecasts
        pred15 = model15.predict(test15.shape[0])       
        prediccion_15  = pred15.to_frame()
        prediccion_15 = prediccion_15.reset_index()
        prediccion_15 = prediccion_15.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_15[d]


def Arima16(T16, program_H16, d, seasonal):
        train16 = T16[['date', d]].set_index('date')
        test16 = program_H16[['date']].set_index('date')
        # Fit your model
        model16 = pm.auto_arima(train16, seasonal=seasonal, m=12)
        # make your forecasts
        pred16 = model16.predict(test16.shape[0])       
        prediccion_16  = pred16.to_frame()
        prediccion_16 = prediccion_16.reset_index()
        prediccion_16 = prediccion_16.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_16[d]


def Arima17(T17, program_H17, d, seasonal):
        train17 = T17[['date', d]].set_index('date')
        test17 = program_H17[['date']].set_index('date')
        # Fit your model
        model17 = pm.auto_arima(train17, seasonal=seasonal, m=12)
        # make your forecasts
        pred17 = model17.predict(test17.shape[0])       
        prediccion_17  = pred17.to_frame()
        prediccion_17 = prediccion_17.reset_index()
        prediccion_17 = prediccion_17.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_17[d]


def Arima18(T18, program_H18, d, seasonal):
        train18 = T18[['date', d]].set_index('date')
        test18 = program_H18[['date']].set_index('date')
        # Fit your model
        model18 = pm.auto_arima(train18, seasonal=seasonal, m=12)
        # make your forecasts
        pred18 = model18.predict(test18.shape[0])       
        prediccion_18  = pred18.to_frame()
        prediccion_18 = prediccion_18.reset_index()
        prediccion_18 = prediccion_18.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_18[d]


def Arima19(T19, program_H19, d, seasonal):
        train19 = T19[['date', d]].set_index('date')
        test19 = program_H19[['date']].set_index('date')
        # Fit your model
        model19 = pm.auto_arima(train19, seasonal=seasonal, m=12)
        # make your forecasts
        pred19 = model19.predict(test19.shape[0])       
        prediccion_19  = pred19.to_frame()
        prediccion_19 = prediccion_19.reset_index()
        prediccion_19 = prediccion_19.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_19[d]



def Arima20(T20, program_H20, d, seasonal):
        train20 = T20[['date', d]].set_index('date')
        test20 = program_H20[['date']].set_index('date')
        # Fit your model
        model20 = pm.auto_arima(train20, seasonal=seasonal, m=12)
        # make your forecasts
        pred20 = model20.predict(test20.shape[0])       
        prediccion_20  = pred20.to_frame()
        prediccion_20 = prediccion_20.reset_index()
        prediccion_20 = prediccion_20.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_20[d]


def Arima21(T21, program_H21, d, seasonal):
        train21 = T21[['date', d]].set_index('date')
        test21 = program_H21[['date']].set_index('date')
        # Fit your model
        model21 = pm.auto_arima(train21, seasonal=seasonal, m=12)
        # make your forecasts
        pred21 = model21.predict(test21.shape[0])       
        prediccion_21  = pred21.to_frame()
        prediccion_21 = prediccion_21.reset_index()
        prediccion_21 = prediccion_21.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_21[d]


def Arima22(T22, program_H22, d, seasonal):
        train22 = T22[['date', d]].set_index('date')
        test22 = program_H22[['date']].set_index('date')
        # Fit your model
        model22 = pm.auto_arima(train22, seasonal=seasonal, m=12)
        # make your forecasts
        pred22 = model22.predict(test22.shape[0])       
        prediccion_22  = pred22.to_frame()
        prediccion_22 = prediccion_22.reset_index()
        prediccion_22 = prediccion_22.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_22[d]



def Arima23(T23, program_H23, d, seasonal):
        train23 = T23[['date', d]].set_index('date')
        test23 = program_H23[['date']].set_index('date')
        # Fit your model
        model23 = pm.auto_arima(train23, seasonal=seasonal, m=12)
        # make your forecasts
        pred23 = model23.predict(test23.shape[0])       
        prediccion_23  = pred23.to_frame()
        prediccion_23 = prediccion_23.reset_index()
        prediccion_23 = prediccion_23.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_23[d]


def Arima24(T24, program_H24, d, seasonal):
        train24 = T24[['date', d]].set_index('date')
        test24 = program_H24[['date']].set_index('date')
        # Fit your model
        model24 = pm.auto_arima(train24, seasonal=seasonal, m=12)
        # make your forecasts
        pred24 = model24.predict(test24.shape[0])       
        prediccion_24  = pred24.to_frame()
        prediccion_24 = prediccion_24.reset_index()
        prediccion_24 = prediccion_24.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_24[d]



def Arima25(T25, program_H25, d, seasonal):
        train25 = T25[['date', d]].set_index('date')
        test25 = program_H25[['date']].set_index('date')
        # Fit your model
        model25 = pm.auto_arima(train25, seasonal=seasonal, m=12)
        # make your forecasts
        pred25 = model25.predict(test25.shape[0])       
        prediccion_25  = pred25.to_frame()
        prediccion_25 = prediccion_25.reset_index()
        prediccion_25 = prediccion_25.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_25[d]



def Arima26(T26, program_H26, d, seasonal):
        train26 = T26[['date', d]].set_index('date')
        test26 = program_H26[['date']].set_index('date')
        # Fit your model
        model26 = pm.auto_arima(train26, seasonal=seasonal, m=12)
        # make your forecasts
        pred26 = model26.predict(test26.shape[0])       
        prediccion_26  = pred26.to_frame()
        prediccion_26 = prediccion_26.reset_index()
        prediccion_26 = prediccion_26.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_26[d]




def Arima27(T27, program_H27, d, seasonal):
        train27 = T27[['date', d]].set_index('date')
        test27 = program_H27[['date']].set_index('date')
        # Fit your model
        model27 = pm.auto_arima(train27, seasonal=seasonal, m=12)
        # make your forecasts
        pred27 = model27.predict(test27.shape[0])       
        prediccion_27  = pred27.to_frame()
        prediccion_27 = prediccion_27.reset_index()
        prediccion_27 = prediccion_27.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_27[d]



def Arima28(T28, program_H28, d, seasonal):
        train28 = T28[['date', d]].set_index('date')
        test28 = program_H28[['date']].set_index('date')
        # Fit your model
        model28 = pm.auto_arima(train28, seasonal=seasonal, m=12)
        # make your forecasts
        pred28 = model28.predict(test28.shape[0])       
        prediccion_28  = pred28.to_frame()
        prediccion_28 = prediccion_28.reset_index()
        prediccion_28 = prediccion_28.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_28[d]



def Arima29(T29, program_H29, d, seasonal):
        train29 = T29[['date', d]].set_index('date')
        test29 = program_H29[['date']].set_index('date')
        # Fit your model
        model29 = pm.auto_arima(train29, seasonal=seasonal, m=12)
        # make your forecasts
        pred29 = model29.predict(test29.shape[0])       
        prediccion_29  = pred29.to_frame()
        prediccion_29 = prediccion_29.reset_index()
        prediccion_29 = prediccion_29.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_29[d]



def Arima30(T30, program_H30, d, seasonal):
        train30 = T30[['date', d]].set_index('date')
        test30 = program_H30[['date']].set_index('date')
        # Fit your model
        model30 = pm.auto_arima(train30, seasonal=seasonal, m=12)
        # make your forecasts
        pred30 = model30.predict(test30.shape[0])       
        prediccion_30  = pred30.to_frame()
        prediccion_30 = prediccion_30.reset_index()
        prediccion_30 = prediccion_30.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_30[d]



def Arima31(T31, program_H31, d, seasonal):
        train31 = T31[['date', d]].set_index('date')
        test31 = program_H31[['date']].set_index('date')
        # Fit your model
        model31 = pm.auto_arima(train31, seasonal=seasonal, m=12)
        # make your forecasts
        pred31 = model31.predict(test31.shape[0])       
        prediccion_31  = pred31.to_frame()
        prediccion_31 = prediccion_31.reset_index()
        prediccion_31 = prediccion_31.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_31[d]




"""
# tasa  YoY  trimestral año a año
"""


def tasaYoY(A):
     def tasa(E, col):
         E['date'] = pd.to_datetime(E['date'])
         E['month'] = E['date'].dt.month
         E['year'] = E['date'].dt.year 

         lista_1 = []
         for i in E['month'].unique():
                  R = E[E['month'] == i]
                  R.reset_index()
                  R[f'tasa_{col}'] = 0
                  for j in range(1, len(R)):
                      R[f'tasa_{col}'].iloc[j] = (R[col].iloc[j] - R[col].iloc[j-1]) / R[col].iloc[j-1]   
                  lista_1.append(R[['date', f'tasa_{col}']]) 
         C = pd.concat(lista_1).drop_duplicates(subset='date').reset_index(drop=True)
         C = C.sort_values(by=['date'])
         return C

     lista_g = []
     for g in A.columns[1:]:
               lista_g.append(tasa(A[['date', g]], g))     

     from functools import reduce    
     DATA_YoY = reduce(lambda left, right:     # Merge three pandas DataFrames
                          pd.merge(left , right,
                                   on = ["date"]),
                          lista_g)
     return DATA_YoY

