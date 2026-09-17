# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:03:55 2024

@author: Juan Pablo Aguirre
"""

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

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import xgboost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn import preprocessing


from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from typing import Tuple

import scipy as sc
import math

import pandas as pd
from functools import reduce

# Personal Consumption Expenditures (PCE)
# Leading Indicators OECD: Reference Series: Gross Domestic Product (GDP):
# Normalised for United States (USALORSGPNOSTSAM)

# Indicadores principales OCDE: Serie de referencia: Producto 
# interno bruto (PIB): normalizado para Estados Unidos

# gdpc1 fred
# https://www.kaggle.com/code/hariharanloganathan/homellcproject-hari#Building-Machine-Learning-model-that-influenced-home-prices-over-past-21-years-from-2020---2021

# https://www.kaggle.com/code/sordatainesdelacruz/analysis-of-us-gasoline-prices-dataprep

# CPIAUCNS   pci

# https://www.bea.gov/
data = web.DataReader(['PCE', 'GDPC1'], 'fred', datetime(1960, 6, 1), datetime.now())
data.columns = ['pce',  'gdp']
data = data.reset_index()
data = data.rename(columns = {'DATE' : 'date'})

data['pce'] = data['pce'].fillna(method= 'ffill')

fecha_X = '2005-01-01 00:00:00'
data = data[data['date']>= fecha_X]

W = data[['date', 'gdp']]
T= data[['date', 'gdp']]
T['gdp'] = T['gdp'].astype('float64')


T['gdp'] = T['gdp'].astype('float64')

TOC = T[['date', 'gdp']]
T = T.dropna()
from z_lost_function import tasaYoY

based = tasaYoY(T)
based = based[based['tasa_YoY_gdp'] != 0]


TOC = TOC.merge(based, how = 'left', on = 'date')
TOC = TOC[['date', 'tasa_YoY_gdp']]

TOC['tasa_YoY_gdp'].interpolate(method = 'polynomial', order= 2, inplace = True)
TOC = TOC.dropna()

DATA_T = TOC


"""
####--- fecha de la data a estimar ---####
"""
from datetime import datetime
import pandas as pd

periodo = 8

# date_after_month = datetime.today()+ relativedelta(months=1)
fecha_1 = datetime.strptime("2024-08-01", "%Y-%m-%d")

DATA_GDP = DATA_T

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

# stack overflow  sarimax
# https://www.kaggle.com/code/brendanartley/time-series-forecasting-w-arima-sarima
