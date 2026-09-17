# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 07:33:56 2024

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

from B_lost_functions import Arima1, Arima2, Arima3, Arima4, Arima5, Arima6
from B_lost_functions import Arima7, Arima8, Arima9, Arima10, Arima11, Arima12
from B_lost_functions import Arima13, Arima14, Arima15, Arima16, Arima17, Arima18
from B_lost_functions import Arima19, Arima20, Arima21, Arima22, Arima23, Arima24
from B_lost_functions import Arima25, Arima26, Arima27, Arima28, Arima29, Arima30
from B_lost_functions import Arima31


from A_lapso import fecha_0, fecha_1, periodo, date_list_w
from C_matriz_1 import DATA_Y


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
       seasonal = 'False'
       
       if d == 'tasa_item1':
           pred = Arima1(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item2':
           pred = Arima2(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item3':
           pred = Arima3(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item4':
           pred = Arima4(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item5':
           pred = Arima5(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item6':
           pred = Arima6(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item7':
           pred = Arima7(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item8':
           pred = Arima8(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item9':
           pred = Arima9(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item10':
           pred = Arima10(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item11':
           pred = Arima11(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item12':
           pred = Arima12(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item13':
           pred = Arima13(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item14':
           pred = Arima14(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item15':
           pred = Arima15(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item16':
           pred = Arima16(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item17':
           pred = Arima17(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item18':
           pred = Arima18(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item19':
           pred = Arima19(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item20':
           pred = Arima20(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item21':
           pred = Arima21(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item22':
           pred = Arima22(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item23':
           pred = Arima23(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item24':
           pred = Arima24(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item25':
           pred = Arima25(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item26':
           pred = Arima26(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item27':
           pred = Arima27(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item28':
           pred = Arima28(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item29':
           pred = Arima29(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item30':
           pred = Arima30(T, program_H, d, seasonal = seasonal)
       elif d == 'tasa_item31':
           pred = Arima31(T, program_H, d, seasonal = seasonal)
           
    
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

F = DATA_Y
# del F['ipc_real']
F['date'] = pd.to_datetime(F['date'])

lista_i = []
lista_ii = []
for d in F.columns[1:-1]:
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

program_HA = df_merged[df_merged['date']>= fecha_1]

# program_HR = date_list_w.merge(F, how = 'left', on = 'date')
# program_HR = program_HR[program_HA.columns]

columna_A = program_HA.columns[1:] 
T = F[F['date']< fecha_1]
