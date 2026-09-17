# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:10:30 2024

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


from A_lapso import fecha_0, fecha_1, periodo, date_list_w
from C_matriz_2 import F, T, program_HA, columna_A


X = T[columna_A]
y = T[['tasa_cpi']]

# regresión por mínimos cuadrados ponderados
mdl = sm.WLS(y, X).fit()

# results = wls_model.fit()
# results = mdl.fit()

parametros = pd.DataFrame(mdl.params)
parametros = parametros.reset_index()
parametros = parametros.rename(columns = {'index':'features',
                                          0:'weights'})

paramestro_suma = parametros['weights'].sum()

# mdl.summary()
y_pred =  mdl.predict(program_HA[columna_A])
y_pred = pd.DataFrame(y_pred)
program_HA['tasa_cpi_est'] = pd.DataFrame(y_pred)

program_HA = program_HA.rename(columns = {'tasa_cpi_est': 'tasa_cpi'})

# A = program_H[['date', 'cpi', 'cpi_est']]
# construir data real K1, y estimada K2

K1 = F[['date', 'tasa_cpi']][F['date']<= date_list_w['date'].max()]

K2 = pd.concat([T[['date', 'tasa_cpi']], program_HA[['date', 'tasa_cpi']]]).drop_duplicates(subset='date').reset_index(drop=True)
K2 = K2.rename(columns = {'tasa_cpi': 'tasa_cpi_est'})

DATA_R = K2.merge(K1, how = 'left', on = 'date')
DATA_R = DATA_R[DATA_R['date']>= fecha_1]


df = K2.merge(K1, how = 'left', on = 'date')

# 1. Creamos el DF trimestral con los promedios
df_trim = df.resample('QE', on='date')[['tasa_cpi_est', 'tasa_cpi']].mean().to_period('Q')

# 2. Calculamos las diferencias respecto al trimestre anterior
df_trim[['diff_est', 'diff_real']] = df_trim.diff()

# 3. Columna de validación de dirección
import numpy as np
df_trim['coincide_dir'] = np.where(df_trim['diff_est'] * df_trim['diff_real'] > 0, 'Sí', 'No')

print(df_trim.iloc[-1:])

# DATA_R.to_excel('cpi_US_month_03_2024_hasta_12_2024_True.xlsx', index= False)

# Other goods and services

# features hay 26
# https://www.bls.gov/news.release/cpi.t01.htm

# gráficos
# https://www.bls.gov/charts/consumer-price-index/consumer-price-index-by-category-line-chart.htm


# ver estas features
# https://www.bls.gov/cpi/tables/supplemental-files/home.htm