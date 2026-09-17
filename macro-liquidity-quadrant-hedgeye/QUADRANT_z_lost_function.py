# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 07:34:51 2024

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
from sklearn.linear_model import *

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
import xgboost
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
from xgboost import XGBRegressor
import pmdarima as pm


"""
######--- MODELOS ----######
"""

# Arima_M2SL
def Arima_M2SL(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, seasonal= True, m=12)
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]


# Arima_TOTRESNS
def Arima_TOTRESNS(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, seasonal= True, m=12)
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]




# ARIMA GDP
def ArimaGDP(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, seasonal=True, m=12)
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]



# ARIMA GDP
def ArimaGDPa(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, start_p=1, 
        start_q=1,
        test='adf', # use adftest to find optimal 'd'
        max_p=2, max_q=2, # maximum p and q
        m=1, # frequency of series (if m==1, seasonal is set to FALSE automatically)
        d=None,# let model determine 'd'
        seasonal= True, # No Seasonality for standard ARIMA
        trace = False, #logs 
        error_action='warn', #shows errors ('ignore' silences these)
        suppress_warnings=True,
        stepwise=True)
        
        
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]




# ARIMA CPI
def ArimaCPI(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, seasonal=True, m=12)
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]




# ARIMA CPIa
def ArimaCPIa(T, program_H, d):
        train = T[['date', d]].set_index('date')
        test = program_H[['date']].set_index('date')
        # Fit your model
        model = pm.auto_arima(train, start_p=1, 
        start_q=1,
        test='adf', # use adftest to find optimal 'd'
        max_p=2, max_q=2, # maximum p and q
        m=1, # frequency of series (if m==1, seasonal is set to FALSE automatically)
        d=None,# let model determine 'd'
        seasonal= True, # No Seasonality for standard ARIMA
        trace = False, #logs 
        error_action='warn', #shows errors ('ignore' silences these)
        suppress_warnings=True,
        stepwise=True)
        
        
        # make your forecasts
        pred = model.predict(test.shape[0])       
        prediccion_2  = pred.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]



"""
######################################################
"""

"""
# construcción de data con tasa anual tradicional
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
                  R[f'tasa_YoY_{col}'] = 0
                  for j in range(1, len(R)):
                      R[f'tasa_YoY_{col}'].iloc[j] = (R[col].iloc[j] - R[col].iloc[j-1]) / R[col].iloc[j-1]   
                  lista_1.append(R[['date', f'tasa_YoY_{col}']]) 
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



"""
######################################################
"""


