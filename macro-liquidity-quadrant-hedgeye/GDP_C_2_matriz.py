# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:35:22 2024

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

from A_lapso import date_list_w, fecha_1
from B_4_base import L
from C_1_matriz import F, df_merged


df_merged['item11'] = - df_merged['item11']
df_merged['item12'] = - df_merged['item12']


program_H = df_merged[df_merged['date']>= fecha_1]

# program_H.columns

# columna_A = program_H.columns[1:] 
DATA_R = L[['date', 'item0']].rename(columns = {'item0': 'gdpc1'})

program_H['suma'] = program_H[program_H.columns[1:]].sum(axis= 1)
program_HK = program_H[['date', 'suma']].merge(DATA_R, how = 'left', on = 'date')
program_HK['error'] = program_HK['gdpc1'] - program_HK['suma']




A1 = L[['date', 'item0']].rename(columns= {'item0': 'gdpc1'})[L['date']<= date_list_w['date'].max()]
A2 = L[['date', 'item0']].rename(columns= {'item0': 'gdpc1_est'})[L['date']< date_list_w['date'].min()]

R2 = program_HK[['date', 'suma']].rename(columns = {'suma':'gdpc1_est'})

T2 = pd.concat([A2, R2]).drop_duplicates(subset='date').reset_index(drop=True)


from B_1_lost_function import tasaYoY

tasa_real = tasaYoY(A1)
tasa_est = tasaYoY(T2)

TASA = tasa_est.merge(tasa_real, how= 'left', on = 'date')
TASA = date_list_w.merge(TASA, how = 'left', on = 'date')

"""
######--- OLS --#####
"""

"""
import statsmodels.api as sm
import numpy as np

# program_H.columns

B = T.merge(DATA_R, how ='left', on = 'date')

# columna_l = program_H.columns[1:]

columna_l = ['tasa_item1', 'tasa_item2', 'tasa_item3', 'tasa_item4',
             'tasa_item5', 'tasa_item6', 'tasa_item7', 'tasa_item8', 'tasa_item9',
             'tasa_item10', 'tasa_item11', 'tasa_item12', 'tasa_item13',
             'tasa_item14', 'tasa_item15', 'tasa_item16']


X = B[columna_l]
y = B.gdpc1
mdl = sm.OLS(y,X).fit()
# mdl.summary()
y_pred =  mdl.predict(program_H[columna_l])
y_pred = pd.DataFrame(y_pred)
program_H['gdpc1_est'] = pd.DataFrame(y_pred)

# program_H.columns

program_HA = program_H[['date', 'gdpc1_est']]

program_HA = program_HA.merge(DATA_R[['date', 'gdpc1']], how = 'left', on = 'date')

"""
