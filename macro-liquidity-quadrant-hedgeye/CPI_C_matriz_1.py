# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:53:14 2024

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

# https://www.geeksforgeeks.org/weighted-least-squares-regression-in-python/

from A_lapso import fecha_00, fecha_0, fecha_1, periodo, date_list_w

# Commodities less food and beverages
# CUSR0000SACL11

# All items less food and energy
# cambiar CPIAUCNS por CPILFESL.



"""
CUSR0000SAH3 reemplazó a 
CUURA000SAH31
CUUR0000SEHP
"""

M = web.DataReader(['CUSR0000SAF11', 'CUSR0000SEFV', 'CUSR0000SEFW', 'CUSR0000SEFX', 'CUSR0000SEHA',
                    'CUSR0000SEHB', 'CUSR0000SEHC', 'CUUR0000SEHD', 'CUSR0000SAH2',  'CUSR0000SAH3',
                    'CUSR0000SAA1', 'CUSR0000SAA2', 'CUSR0000SEAE', 'CUSR0000SAA2',
                    'CUSR0000SEAE', 'CUSR0000SEAF', 'CUSR0000SAT1', 'CUSR0000SETG', 'CUSR0000SAM1',
                    'CUSR0000SAM2', 'CPIRECSL', 'CUSR0000SEEA', 'CUSR0000SEEB', 'CUSR0000SAE2',
                    'CUSR0000SEGA', 'CUSR0000SAG1', 'CUSR0000SACL11', 'CUSR0000SANL11', 'CUSR0000SACL1E',
                    'CUSR0000SASLE',
                    'CPIAUCNS'], 'fred', datetime(1970, 6, 1), datetime.now())



M.columns =  ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10',
              'item11', 'item12', 'item13', 'item14', 'item15', 'item16', 'item17', 'item18', 'item19',
              'item20', 'item21', 'item22', 'item23', 'item24', 'item25', 'item26', 'item27', 'item28',
              'item29', 'item30', 'cpi']
M = M.reset_index()
M = M.rename(columns = {'DATE': 'date'})
R = M[['date', 'cpi']]

tabla_corr = M.corr()

DATA_T = M[M['date'] > fecha_00]
DATA_T = DATA_T.ffill()


F  = DATA_T
from B_lost_functions import tasaYoY

lista_f = []
for f in F.columns[1:]:
          lista_f.append(tasaYoY(F[['date', f]]))
          
          
from functools import reduce    
DATA_Y = reduce(lambda left, right:     # Merge three pandas DataFrames
                     pd.merge(left , right,
                              on = ["date"]),
                     lista_f)          

DATA_Y = DATA_Y[DATA_Y['tasa_cpi'] != 0]
# DATA_Y = DATA_Y[DATA_Y['date'] != '2025-10-01']
