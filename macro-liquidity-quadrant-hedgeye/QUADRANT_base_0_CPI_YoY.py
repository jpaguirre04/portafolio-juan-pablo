# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 19:09:05 2024

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
from dateutil.relativedelta import relativedelta
from typing import Tuple

import scipy as sc
import math

# CPIAUCSL
# CPIAUCNS

"""
##########################
# 1.-  Other goods and services
# Consumer Price Index for All Urban Consumers: Other Goods and Services in U.S. City Average (CPIOGSSL)    [2.821]
##########################
"""

IPC = web.DataReader(['CPIAUCNS'], 'fred', datetime(1970, 6, 1), datetime.now())
IPC.columns =  ['cpi']
IPC = IPC.reset_index()

DATA_0 = IPC


fecha_0 = '2005-01-01 00:00:00'
# fecha_0 = '2005-12-01 00:00:00'
DATA_0 = DATA_0[DATA_0['DATE']>= fecha_0]
DATA_0 = DATA_0.rename(columns = {'DATE': 'date'})



"""
####--- GENERACIÓN DE LAS TASAS ---####
"""

from z_lost_function import tasaYoY

DATA_T = tasaYoY(DATA_0)
DATA_T = DATA_T[DATA_T['tasa_YoY_cpi'] != 0]


"""
####--- fecha de la data a estimar ---####
"""

from datetime import datetime
import pandas as pd

periodo = 5

# date_after_month = datetime.today()+ relativedelta(months=1)
fecha_1 = datetime.strptime("2024-11-01", "%Y-%m-%d")

DATA_CPI = DATA_T


"""
####--- crear nueva data a estimar ---####
"""
from datetime import datetime

# start_date = pd.to_datetime('now')
# periods means how many dates you want
date_list_w = pd.date_range(fecha_1, periods= periodo, freq='MS')
date_list_w = [pd.to_datetime(e) for e in date_list_w]
date_list_w = pd.DataFrame(date_list_w)
date_list_w = date_list_w.rename(columns= {0: 'date'})
date_list_w['date'] = pd.to_datetime(date_list_w['date'])


from dateutil.relativedelta import relativedelta
fecha = date_list_w['date'].min() - relativedelta(months= periodo)

# start_date = pd.to_datetime('now')
# periods means how many dates you want
date_list = pd.date_range(fecha, periods= periodo, freq='MS')
date_list = [pd.to_datetime(e) for e in date_list]
date_list = pd.DataFrame(date_list)
date_list = date_list.rename(columns= {0: 'date'})
date_list['date'] = pd.to_datetime(date_list['date'])