# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:31:17 2024

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


fechag = '2007-01-01 00:00:00'

"""
##################--- Real Personal Consumption Expenditures (PCECC96)  ---#####################
"""

# Real Personal Consumption Expenditures (PCECC96)

T0 = web.DataReader(['GDPC1',
                     
                     'PCDGCC96', 'PCNDGC96', 'PCESVC96', 
                     'B009RX1Q020SBEA', 'Y033RX1Q020SBEA', 'Y001RX1Q020SBEA', 'PRFIC1', 'CBIC1',
                     'A253RX1Q020SBEA', 'A646RX1Q020SBEA', 'A255RX1Q020SBEA', 'B656RX1Q020SBEA', 
                     'A824RX1Q020SBEA', 'A825RX1Q020SBEA', 'SLCEC1', 
                     
                     'A960RX1Q020SBEA'
                     ], 'fred', datetime(1970, 6, 1), datetime.now())

T0.columns =  ['item0', 
               
               'item1', 'item2', 'item3', 
               'item4', 'item5', 'item6', 'item7', 'item8',
               'item9', 'item10', 'item11', 'item12', 
               'item13', 'item14', 'item15', 
               
               'item16']

T0 = T0.reset_index()
T0 = T0.rename(columns = {'DATE': 'date'})
T0 = T0[T0['date']>= fechag]


T0['item11'] = - T0['item11']
T0['item12'] = - T0['item12']


T0['item0_est'] = T0[T0.columns[2:]].sum(axis=1)

T1 = T0[['date', 'item0', 'item0_est']]
T1 = T1[T1['item0_est']!= 0]

T1['error'] = T1['item0'] - T1['item0_est']

base = T0
base = base.drop(columns = 'item0_est')
A = base[['date']]

base['item11'] = - base['item11']
base['item12'] = - base['item12']
