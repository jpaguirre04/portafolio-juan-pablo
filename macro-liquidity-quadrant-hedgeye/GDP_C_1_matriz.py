# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:39:36 2024

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
import pmdarima as pm

# https://www.geeksforgeeks.org/weighted-least-squares-regression-in-python/

from B_1_lost_function import ArimaGDP1, ArimaGDP2, ArimaGDP3, ArimaGDP4, ArimaGDP5
from B_1_lost_function import ArimaGDP6, ArimaGDP7, ArimaGDP8, ArimaGDP9, ArimaGDP10
from B_1_lost_function import ArimaGDP11, ArimaGDP12, ArimaGDP13, ArimaGDP14, ArimaGDP15
from B_1_lost_function import ArimaGDP16, ArimaGDP17

from A_lapso import fecha_0, fecha_1, periodo, date_list_w
from B_4_base import L # , df_differenced2


"""
# FUNCION DE PREDICCIÓN !!!
"""


def funcion_ARIMA(D, d, fecha):
       T = D[D['date'] < fecha]
       # print(T.columns)
       # print(T)
       f = {'date' : [fecha]}
       program_H = pd.DataFrame(f)
       program_H['date'] = pd.to_datetime(program_H['date'])
       # T = T.set_index('date')
       # T = T.tail(72)
       season = 'True'
       
       if d == 'item1':
           pred = ArimaGDP1(T, program_H, d, season = season)
       elif d == 'item2':
           pred = ArimaGDP2(T, program_H, d, season = season)
       elif d == 'item3':
           pred = ArimaGDP3(T, program_H, d, season = season)
       elif d == 'item4':
           pred = ArimaGDP4(T, program_H, d, season = season)
       elif d == 'item5':
           pred = ArimaGDP5(T, program_H, d, season = season)
       elif d == 'item6':
           pred = ArimaGDP6(T, program_H, d, season = season)
       elif d == 'item7':
           pred = ArimaGDP7(T, program_H, d, season = season)
       elif d == 'item8':
           pred = ArimaGDP8(T, program_H, d, season = season)
       elif d == 'item9':
           pred = ArimaGDP9(T, program_H, d, season = season)
       elif d == 'item10':
           pred = ArimaGDP10(T, program_H, d, season = season)
       elif d == 'item11':
           pred = ArimaGDP11(T, program_H, d, season = season)
       elif d == 'item12':
           pred = ArimaGDP12(T, program_H, d, season = season)
       elif d == 'item13':
           pred = ArimaGDP13(T, program_H, d, season = season)
       elif d == 'item14':
           pred = ArimaGDP14(T, program_H, d, season = season)
       elif d == 'item15':
           pred = ArimaGDP15(T, program_H, d, season = season)
       elif d == 'item16':
           pred = ArimaGDP16(T, program_H, d, season = season)
       elif d == 'item17':
           pred = ArimaGDP17(T, program_H, d, season = season)
       
        
       # print(pred)
       program_H[d] = pred[0]
       # print(program_H[d])
       # T = T.reset_index()
       program_H = program_H[T.columns]
       # print(program_H)
       S = pd.concat([T, program_H]).drop_duplicates(subset='date').reset_index(drop=True)
       print(S)
       return S

"""
### seguir ###
"""



F = L.drop('item0',axis=1)


# F = df_differenced2.reset_index()

F['date'] = pd.to_datetime(F['date'])

lista_i = []
lista_ii = []
for d in F.columns[1:]:
      # "d" es la variable
      Di = F[['date', d]]
      # continue with "for" para fechas
      for t in date_list_w['date']:
          U = funcion_ARIMA(Di, d, t)
          lista_i.append(U)
          Di = U
          # inicio de la data
      lista_ii.append(Di)
      
      
      
lista_t = []      
for t in lista_ii:
    lista_t.append(t.iloc[:, [0, 1]])
    
    
from functools import reduce
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['date'],  how='outer'), lista_t)

# es para ver la diferencia nomas!!!
program_HG_estimado = date_list_w[['date']].merge(df_merged, how= 'left', on = 'date')
program_HG_real = date_list_w[['date']].merge(F, how= 'left', on = 'date')


