# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:46:58 2024

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



# ARIMA GDP1
def ArimaGDP1(T1, program_H1, d, season):
        train1 = T1[['date', d]].set_index('date')
        test1 = program_H1[['date']].set_index('date')
        # Fit your model
        model1 = pm.auto_arima(train1, seasonal =season, m=12)
        # make your forecasts
        pred1 = model1.predict(test1.shape[0])       
        prediccion_1  = pred1.to_frame()
        prediccion_1 = prediccion_1.reset_index()
        prediccion_1 = prediccion_1.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_1[d]



# ARIMA GDP2
def ArimaGDP2(T2, program_H2, d, season):
        train2 = T2[['date', d]].set_index('date')
        test2 = program_H2[['date']].set_index('date')
        # Fit your model
        model2 = pm.auto_arima(train2, seasonal =season, m=12)
        # make your forecasts
        pred2 = model2.predict(test2.shape[0])       
        prediccion_2  = pred2.to_frame()
        prediccion_2 = prediccion_2.reset_index()
        prediccion_2 = prediccion_2.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_2[d]




# ARIMA GDP3
def ArimaGDP3(T3, program_H3, d, season):
        train3 = T3[['date', d]].set_index('date')
        test3 = program_H3[['date']].set_index('date')
        # Fit your model
        model3 = pm.auto_arima(train3, seasonal =season, m=12)
        # make your forecasts
        pred3 = model3.predict(test3.shape[0])       
        prediccion_3  = pred3.to_frame()
        prediccion_3 = prediccion_3.reset_index()
        prediccion_3 = prediccion_3.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_3[d]




# ARIMA GDP4
def ArimaGDP4(T4, program_H4, d, season):
        train4 = T4[['date', d]].set_index('date')
        test4 = program_H4[['date']].set_index('date')
        # Fit your model
        model4 = pm.auto_arima(train4, seasonal =season, m=12)
        # make your forecasts
        pred4 = model4.predict(test4.shape[0])       
        prediccion_4  = pred4.to_frame()
        prediccion_4 = prediccion_4.reset_index()
        prediccion_4 = prediccion_4.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_4[d]



# ARIMA GDP5
def ArimaGDP5(T5, program_H5, d, season):
        train5 = T5[['date', d]].set_index('date')
        test5 = program_H5[['date']].set_index('date')
        # Fit your model
        model5 = pm.auto_arima(train5, seasonal =season, m=12)
        # make your forecasts
        pred5 = model5.predict(test5.shape[0])       
        prediccion_5  = pred5.to_frame()
        prediccion_5 = prediccion_5.reset_index()
        prediccion_5 = prediccion_5.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_5[d]



# ARIMA GDP6
def ArimaGDP6(T6, program_H6, d, season):
        train6 = T6[['date', d]].set_index('date')
        test6 = program_H6[['date']].set_index('date')
        # Fit your model
        model6 = pm.auto_arima(train6, seasonal =season, m=12)
        # make your forecasts
        pred6 = model6.predict(test6.shape[0])       
        prediccion_6  = pred6.to_frame()
        prediccion_6 = prediccion_6.reset_index()
        prediccion_6 = prediccion_6.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_6[d]


# ARIMA GDP7
def ArimaGDP7(T7, program_H7, d, season):
        train7 = T7[['date', d]].set_index('date')
        test7 = program_H7[['date']].set_index('date')
        # Fit your model
        model7 = pm.auto_arima(train7, seasonal =season, m=12)
        # make your forecasts
        pred7 = model7.predict(test7.shape[0])       
        prediccion_7  = pred7.to_frame()
        prediccion_7 = prediccion_7.reset_index()
        prediccion_7 = prediccion_7.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_7[d]



# ARIMA GDP8
def ArimaGDP8(T8, program_H8, d, season):
        train8 = T8[['date', d]].set_index('date')
        test8 = program_H8[['date']].set_index('date')
        # Fit your model
        model8 = pm.auto_arima(train8, seasonal =season, m=12)
        # make your forecasts
        pred8 = model8.predict(test8.shape[0])       
        prediccion_8  = pred8.to_frame()
        prediccion_8 = prediccion_8.reset_index()
        prediccion_8 = prediccion_8.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_8[d]



# ARIMA GDP1
def ArimaGDP9(T9, program_H9, d, season):
        train9 = T9[['date', d]].set_index('date')
        test9 = program_H9[['date']].set_index('date')
        # Fit your model
        model9 = pm.auto_arima(train9, seasonal =season, m=12)
        # make your forecasts
        pred9 = model9.predict(test9.shape[0])       
        prediccion_9  = pred9.to_frame()
        prediccion_9 = prediccion_9.reset_index()
        prediccion_9 = prediccion_9.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_9[d]



# ARIMA GDP10
def ArimaGDP10(T10, program_H10, d, season):
        train10 = T10[['date', d]].set_index('date')
        test10 = program_H10[['date']].set_index('date')
        # Fit your model
        model10 = pm.auto_arima(train10, seasonal =season, m=12)
        # make your forecasts
        pred10 = model10.predict(test10.shape[0])       
        prediccion_10  = pred10.to_frame()
        prediccion_10 = prediccion_10.reset_index()
        prediccion_10 = prediccion_10.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_10[d]


# ARIMA GDP11
def ArimaGDP11(T11, program_H11, d, season):
        train11 = T11[['date', d]].set_index('date')
        test11 = program_H11[['date']].set_index('date')
        # Fit your model
        model11 = pm.auto_arima(train11, seasonal =season, m=12)
        # make your forecasts
        pred11 = model11.predict(test11.shape[0])       
        prediccion_11  = pred11.to_frame()
        prediccion_11 = prediccion_11.reset_index()
        prediccion_11 = prediccion_11.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_11[d]



# ARIMA GDP12
def ArimaGDP12(T12, program_H12, d, season):
        train12 = T12[['date', d]].set_index('date')
        test12 = program_H12[['date']].set_index('date')
        # Fit your model
        model12 = pm.auto_arima(train12, seasonal =season, m=12)
        # make your forecasts
        pred12 = model12.predict(test12.shape[0])       
        prediccion_12  = pred12.to_frame()
        prediccion_12 = prediccion_12.reset_index()
        prediccion_12 = prediccion_12.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_12[d]


# ARIMA GDP13
def ArimaGDP13(T13, program_H13, d, season):
        train13 = T13[['date', d]].set_index('date')
        test13 = program_H13[['date']].set_index('date')
        # Fit your model
        model13 = pm.auto_arima(train13, seasonal =season, m=12)
        # make your forecasts
        pred13 = model13.predict(test13.shape[0])       
        prediccion_13  = pred13.to_frame()
        prediccion_13 = prediccion_13.reset_index()
        prediccion_13 = prediccion_13.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_13[d]
    


# ARIMA GDP14
def ArimaGDP14(T14, program_H14, d, season):
        train14 = T14[['date', d]].set_index('date')
        test14 = program_H14[['date']].set_index('date')
        # Fit your model
        model14 = pm.auto_arima(train14, seasonal =season, m=12)
        # make your forecasts
        pred14 = model14.predict(test14.shape[0])       
        prediccion_14  = pred14.to_frame()
        prediccion_14 = prediccion_14.reset_index()
        prediccion_14 = prediccion_14.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_14[d]
    
    

# ARIMA GDP15
def ArimaGDP15(T15, program_H15, d, season):
        train15 = T15[['date', d]].set_index('date')
        test15 = program_H15[['date']].set_index('date')
        # Fit your model
        model15 = pm.auto_arima(train15, seasonal =season, m=12)
        # make your forecasts
        pred15 = model15.predict(test15.shape[0])       
        prediccion_15  = pred15.to_frame()
        prediccion_15 = prediccion_15.reset_index()
        prediccion_15 = prediccion_15.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_15[d]
    



# ARIMA GDP16
def ArimaGDP16(T16, program_H16, d, season):
        train16 = T16[['date', d]].set_index('date')
        test16 = program_H16[['date']].set_index('date')
        # Fit your model
        model16 = pm.auto_arima(train16, seasonal =season, m=12)
        # make your forecasts
        pred16 = model16.predict(test16.shape[0])       
        prediccion_16  = pred16.to_frame()
        prediccion_16 = prediccion_16.reset_index()
        prediccion_16 = prediccion_16.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_16[d]



# ARIMA GDP17
def ArimaGDP17(T17, program_H17, d, season):
        train17 = T17[['date', d]].set_index('date')
        test17 = program_H17[['date']].set_index('date')
        # Fit your model
        model17 = pm.auto_arima(train17, seasonal =season, m=12)
        # make your forecasts
        pred17 = model17.predict(test17.shape[0])       
        prediccion_17  = pred17.to_frame()
        prediccion_17 = prediccion_17.reset_index()
        prediccion_17 = prediccion_17.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_17[d]



# ARIMA GDP18
def ArimaGDP18(T18, program_H18, d, season):
        train18 = T18[['date', d]].set_index('date')
        test18 = program_H18[['date']].set_index('date')
        # Fit your model
        model18 = pm.auto_arima(train18, seasonal =season, m=12)
        # make your forecasts
        pred18 = model18.predict(test18.shape[0])       
        prediccion_18  = pred18.to_frame()
        prediccion_18 = prediccion_18.reset_index()
        prediccion_18 = prediccion_18.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_18[d]



# ARIMA GDP19
def ArimaGDP19(T19, program_H19, d, season):
        train19 = T19[['date', d]].set_index('date')
        test19 = program_H19[['date']].set_index('date')
        # Fit your model
        model19 = pm.auto_arima(train19, seasonal =season, m=12)
        # make your forecasts
        pred19 = model19.predict(test19.shape[0])       
        prediccion_19  = pred19.to_frame()
        prediccion_19 = prediccion_19.reset_index()
        prediccion_19 = prediccion_19.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_19[d]



# ARIMA GDP20
def ArimaGDP20(T20, program_H20, d, season):
        train20 = T20[['date', d]].set_index('date')
        test20 = program_H20[['date']].set_index('date')
        # Fit your model
        model20 = pm.auto_arima(train20, seasonal =season, m=12)
        # make your forecasts
        pred20 = model20.predict(test20.shape[0])       
        prediccion_20  = pred20.to_frame()
        prediccion_20 = prediccion_20.reset_index()
        prediccion_20 = prediccion_20.rename(columns = {0 : d,
                                                      'index': 'date'})
        return prediccion_20[d]




"""
##################################################
# construcción de data con tasa anual tradicional
##################################################
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
                  R[f'tasa_{col}'] = 0
                  for j in range(1, len(R)):
                      R[f'tasa_{col}'].iloc[j] = (R[col].iloc[j] - R[col].iloc[j-1]) / R[col].iloc[j-1]   
                  lista_1.append(R[['date', f'tasa_{col}']]) 
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
###############################################
# construcción de data con tasa mensual mensual
###############################################
"""


def tasaQoQ(B):
       def tasa(E, col):
            lista_1 = []
            E[f'tasa_QoQ_{col}'] = 0
            for k in range(1, len(E)):
                gr = (E[col].iloc[k] - E[col].iloc[k-1]) / E[col].iloc[k-1]
                # E[f'tasa_QoQ_{col}'].iloc[k] = ((1 + gr)**4) - 1
                E[f'tasa_QoQ_{col}'].iloc[k] = gr
            lista_1.append(E[['date', f'tasa_QoQ_{col}']])
            C = pd.concat(lista_1).drop_duplicates(subset='date').reset_index(drop=True)
            C = C.sort_values(by=['date'])
            return C

       lista_g = []
       for g in B.columns[1:]:
                 lista_g.append(tasa(B[['date', g]], g))     


       DATA_QoQ = reduce(lambda left, right:     # Merge three pandas DataFrames
                            pd.merge(left , right,
                                     on = ["date"]),
                            lista_g)

       return DATA_QoQ