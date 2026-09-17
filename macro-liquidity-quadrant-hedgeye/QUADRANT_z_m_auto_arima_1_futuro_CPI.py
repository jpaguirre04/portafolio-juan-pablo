# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 19:14:03 2024

@author: Juan Pablo Aguirre
"""

# Import Dependancies
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from sklearn.linear_model import LinearRegression

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import *

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
# import lightgbm as lgb
import xgboost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
import pmdarima as pm
from pmdarima.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

from base_0_CPI_YoY import DATA_CPI
from z_lost_function import ArimaCPI, ArimaCPIa

"""
####--- importar fecha y data a estimar ---####
"""
from base_0_CPI_YoY import fecha_1, date_list_w

"""
####--- fin ---####
"""

# FUNCION DE PREDICCIÓN !!!
def funcion_ARIMA(D, d, fecha):
       T = D[D['date'] < fecha]
       # print(T.columns)
       # print(T)
       f = {'date' : [fecha]}
       program_H = pd.DataFrame(f)
       program_H['date'] = pd.to_datetime(program_H['date'])
       pred = ArimaCPI(T, program_H, d)
       program_H[d] = pred
       # print(program_H[d])
       T = T[['date',  d]]
       program_H = program_H[T.columns]
       S = pd.concat([T, program_H]).drop_duplicates(subset='date').reset_index(drop=True)
       print(S)
       return S


"""
### seguir ###
"""

F = DATA_CPI
# del F['ipc_real']
F['date'] = pd.to_datetime(F['date'])

lista_i = []
lista_ii = []
for d in F.columns[1:2]:
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

# "u" es la data a proyectar
u = df_merged
u = u[u['date']>= fecha_1]


u_real = date_list_w.merge(F, how = 'left', on = 'date')

lista_T = []
for col in u.columns[1:]:
     u[f"{col}_est"] = u[col]
     hola = u[['date', f"{col}_est"]].merge(u_real[['date', col]], how = 'left', on = 'date')
     hola[f'error_{col}'] =   hola[col] - hola[f"{col}_est"]    
     # lista_T.append(hola[['date', f"{col}_est", col, f'error_{col}']])
     lista_T.append(hola[['date', col, f"{col}_est",  f'error_{col}']])


df_TOTAL_Arima_futuro_cpi = reduce(lambda  left,right: pd.merge(left,right,on=['date'],  how='outer'), lista_T)

BASE_EST_CPI =  df_TOTAL_Arima_futuro_cpi[['date', 'tasa_YoY_cpi_est']].rename(columns = {'tasa_YoY_cpi_est' : 'tasa_YoY_cpi'})


# drop_duplicates(subset='registro_unico').reset_index(drop=True)
U_T_CPI = pd.concat([DATA_CPI[DATA_CPI['date']< fecha_1], BASE_EST_CPI]).drop_duplicates(subset='date').reset_index(drop=True)

# df_TOTAL_Arima_futuro_cpi.to_excel('hola_ver_1.xlsx', index= False)

