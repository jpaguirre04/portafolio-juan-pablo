# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 11:43:39 2024

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

# importar sólo una fecha_1
from base_0_GDP_YoY import fecha_1

from z_m_auto_arima_1_futuro_GDP import U_T_GPD
from z_m_auto_arima_1_futuro_CPI import U_T_CPI 


# agrupar por trimestre
from datetime import datetime
fecha_2 = datetime.strptime("2003-10-01", "%Y-%m-%d")

"""
# CONSTRUIR TASA TRIMESTRAL PARA GDP
"""
U_T_GPD = U_T_GPD[U_T_GPD['date']>= fecha_2]
U_T_GPD['year'] = U_T_GPD['date'].dt.year
U_T_GPD['quarter'] = U_T_GPD['date'].dt.quarter

U_T_GPD['tasa_YoY_gdp'] = round(100 * U_T_GPD['tasa_YoY_gdp'], 2)

# filtrar o escocger las fechas mínimas trimestrales
e = U_T_GPD.groupby(['year', 'quarter'])['date'].min()
e = e.reset_index()
e = e[['date']]

tabla_gdp = e.merge(U_T_GPD, how = 'left', on = 'date')

tabla_gdp['year'] = tabla_gdp['year'].astype(str)
tabla_gdp['quarter'] = tabla_gdp['quarter'].astype(str)


tabla_gdp['year']= tabla_gdp['year'].str.slice(2,4)

tabla_gdp['clave_o'] = tabla_gdp['quarter']+"T"+tabla_gdp['year']
tabla_gdp = tabla_gdp[['clave_o', 'tasa_YoY_gdp']]


"""
# CONSTRUIR TASA TRIMESTRAL PARA CPI
"""

U_T_CPI = U_T_CPI[U_T_CPI['date']>= fecha_2]
U_T_CPI['year'] = U_T_CPI['date'].dt.year
U_T_CPI['quarter'] = U_T_CPI['date'].dt.quarter

U_T_CPI['tasa_YoY_cpi'] =  round(100 * U_T_CPI['tasa_YoY_cpi'], 2)

tabla_cpi = U_T_CPI.groupby(['year', 'quarter'])['tasa_YoY_cpi'].mean()

tabla_cpi = tabla_cpi.reset_index()
# tabla_m2sl.columns

tabla_cpi['year'] = tabla_cpi['year'].astype(str)
tabla_cpi['quarter'] = tabla_cpi['quarter'].astype(str)

tabla_cpi['year']= tabla_cpi['year'].str.slice(2,4)


tabla_cpi['clave_o'] = tabla_cpi['quarter']+"T"+tabla_cpi['year']
tabla_cpi = tabla_cpi[['clave_o', 'tasa_YoY_cpi']]
tabla_cpi['tasa_YoY_cpi'] = round(tabla_cpi['tasa_YoY_cpi'], 2)


"""
#####---- empezar a contruir los ejes axis -----######
"""


TABLA = tabla_gdp.merge(tabla_cpi, how= 'left', on = 'clave_o')

TABLA['diff_cpi'] = 0
TABLA['diff_gdp'] = 0
TABLA['d'] = 0
lista_1 = []
lista_2 = []

import math
import numpy as np

for k in range(1, len(TABLA)):
         TABLA['diff_cpi'].iloc[k] =   TABLA['tasa_YoY_cpi'].iloc[k] - TABLA['tasa_YoY_cpi'].iloc[k-1]
         TABLA['diff_gdp'].iloc[k] =   TABLA['tasa_YoY_gdp'].iloc[k] - TABLA['tasa_YoY_gdp'].iloc[k-1]
         TABLA['d'].iloc[k] =   np.sqrt((TABLA['tasa_YoY_gdp'].iloc[k])**(2) + (TABLA['tasa_YoY_cpi'].iloc[k])**(2))
         

x = TABLA[['clave_o', 'tasa_YoY_cpi', 'tasa_YoY_gdp', 'diff_cpi', 'diff_gdp', 'd']]
"""
x = x[x['diff_cpi'] != 0]
x = x[x['diff_gdp'] != 0]
"""
x = x[x['d']!= 0]
g = x

# g.to_excel('tabla_historica_sp500.xlsx', index= False)

x = x.rename(columns = {'diff_gdp' : 'Y',
                        'diff_cpi' : 'X'})

x = x.dropna()

o = x[['clave_o', 'X', 'Y', 'd']]
o['cuadrante'] = 0

o.loc[(o['X']<=0) & (o['Y']>0), 'cuadrante'] = 1
o.loc[(o['X']>=0) & (o['Y']>0), 'cuadrante'] = 2
o.loc[(o['X']>=0) & (o['Y']<0), 'cuadrante'] = 3
o.loc[(o['X']<=0) & (o['Y']<0), 'cuadrante'] = 4

gd = o[['clave_o', 'cuadrante', 'd']]

x.columns
o.columns 

a = x[['clave_o', 'tasa_YoY_cpi', 'tasa_YoY_gdp', 'X', 'Y']].merge(o[['clave_o', 'cuadrante']], how = 'left', on = 'clave_o')
a['cuadrante']  = a['cuadrante'].astype(str)



"""
#####---- VALIDACIÓN -----######
"""

from base_0_GDP_YoY import DATA_GDP
from base_0_CPI_YoY import DATA_CPI

"""
# GDP real 
"""
DATA_GDP['year'] = DATA_GDP['date'].dt.year
DATA_GDP['quarter'] = DATA_GDP['date'].dt.quarter

DATA_GDP['tasa_YoY_gdp'] = round(100 * DATA_GDP['tasa_YoY_gdp'], 2)

# filtrar o escoger las fechas mínimas trimestrales
s = DATA_GDP.groupby(['year', 'quarter'])['date'].min()
s = s.reset_index()
s = s[['date']]

tablak_gdp = s.merge(DATA_GDP, how = 'left', on = 'date')

tablak_gdp['year'] = tablak_gdp['year'].astype(str)
tablak_gdp['quarter'] = tablak_gdp['quarter'].astype(str)


tablak_gdp['year']= tablak_gdp['year'].str.slice(2,4)

tablak_gdp['clave_o'] = tablak_gdp['quarter']+"T"+tablak_gdp['year']
tablak_gdp = tablak_gdp[['clave_o', 'tasa_YoY_gdp']]


"""
# CPI real
"""
DATA_CPI['year'] = DATA_CPI['date'].dt.year
DATA_CPI['quarter'] = DATA_CPI['date'].dt.quarter

DATA_CPI['tasa_YoY_cpi'] =  round(100* DATA_CPI['tasa_YoY_cpi'], 2)

tablak_cpi = DATA_CPI.groupby(['year', 'quarter'])['tasa_YoY_cpi'].mean()

tablak_cpi = tablak_cpi.reset_index()
# tabla_m2sl.columns

tablak_cpi['year'] = tablak_cpi['year'].astype(str)
tablak_cpi['quarter'] = tablak_cpi['quarter'].astype(str)

tablak_cpi['year']= tablak_cpi['year'].str.slice(2,4)


tablak_cpi['clave_o'] = tablak_cpi['quarter']+"T"+tablak_cpi['year']
tablak_cpi = tablak_cpi[['clave_o', 'tasa_YoY_cpi']]


TABLAK = tablak_cpi.merge(tablak_gdp, how= 'left', on = 'clave_o')

TABLAK['diff_cpi'] = 0
TABLAK['diff_gdp'] = 0
TABLAK['d'] = 0

lista_1 = []
lista_2 = []

import math
import numpy as np

for k in range(1, len(TABLAK)):
         TABLAK['diff_cpi'].iloc[k] =   TABLAK['tasa_YoY_cpi'].iloc[k] - TABLAK['tasa_YoY_cpi'].iloc[k-1]
         TABLAK['diff_gdp'].iloc[k] =   TABLAK['tasa_YoY_gdp'].iloc[k] - TABLAK['tasa_YoY_gdp'].iloc[k-1]
         TABLAK['d'].iloc[k] =   np.sqrt((TABLAK['tasa_YoY_gdp'].iloc[k])**(2) + (TABLAK['tasa_YoY_cpi'].iloc[k])**(2))
         

z = TABLAK[['clave_o', 'diff_cpi', 'diff_gdp', 'd']]
z = z[z['d'] != 0]
gi = z

z = z.rename(columns = {'diff_gdp' : 'Y',
                        'diff_cpi' : 'X'})

# z = z.dropna()

u = z[['clave_o', 'X', 'Y']]
u['cuadrante_real'] = 0

u.loc[(u['X']<=0) & (u['Y']>0), 'cuadrante_real'] = 1
u.loc[(u['X']>=0) & (u['Y']>0), 'cuadrante_real'] = 2
u.loc[(u['X']>0) & (u['Y']<0), 'cuadrante_real'] = 3
u.loc[(u['X']<0) & (u['Y']<0), 'cuadrante_real'] = 4

gii = u[['clave_o', 'cuadrante_real']]
gii['cuadrante_real'] = gii['cuadrante_real'].astype(str)


a = a.merge(gii, how = 'left', on = 'clave_o')


# a.to_excel('2024_integrar_2T24_1T25.xlsx', index= False)


# 893 

# a.to_excel('2004_integrar_4T04_1T05.xlsx', index= False)
# a.to_excel('2005_integrar_1T05_2T05.xlsx', index= False)
# a.to_excel('2005_integrar_2T05_3T05.xlsx', index= False)
# a.to_excel('2005_integrar_3T05_4T05.xlsx', index= False)
# a.to_excel('2005_integrar_4T05_1T06.xlsx', index= False)
# a.to_excel('2006_integrar_1T06_2T06.xlsx', index= False)
# a.to_excel('2006_integrar_2T06_3T06.xlsx', index= False)
# a.to_excel('2006_integrar_3T06_4T06.xlsx', index= False)
# a.to_excel('2006_integrar_4T06_1T07.xlsx', index= False)
# a.to_excel('2007_integrar_1T07_2T07.xlsx', index= False)
# a.to_excel('2007_integrar_2T07_3T07.xlsx', index= False)
# a.to_excel('2007_integrar_3T07_4T07.xlsx', index= False)
# a.to_excel('2007_integrar_4T07_1T08.xlsx', index= False)
# a.to_excel('2008_integrar_1T08_2T08.xlsx', index= False)
# a.to_excel('2008_integrar_2T08_3T08.xlsx', index= False)
# a.to_excel('2008_integrar_3T08_4T08.xlsx', index= False)
# a.to_excel('2008_integrar_4T08_1T09.xlsx', index= False)
# a.to_excel('2009_integrar_1T09_2T09.xlsx', index= False)
# a.to_excel('2009_integrar_2T09_3T09.xlsx', index= False)
# a.to_excel('2009_integrar_3T09_4T09.xlsx', index= False)
# a.to_excel('2009_integrar_4T09_1T10.xlsx', index= False)
# a.to_excel('2010_integrar_1T10_2T10.xlsx', index= False)
# a.to_excel('2010_integrar_2T10_3T10.xlsx', index= False)
# a.to_excel('2010_integrar_3T10_4T10.xlsx', index= False)
# a.to_excel('2010_integrar_4T10_1T11.xlsx', index= False)
# a.to_excel('2011_integrar_1T11_2T11.xlsx', index= False)
# a.to_excel('2011_integrar_2T11_3T11.xlsx', index= False)
# a.to_excel('2011_integrar_3T11_4T11.xlsx', index= False)
# a.to_excel('2011_integrar_4T11_1T12.xlsx', index= False)
# a.to_excel('2012_integrar_1T12_2T12.xlsx', index= False)
# a.to_excel('2012_integrar_2T12_3T12.xlsx', index= False)
# a.to_excel('2012_integrar_3T12_4T12.xlsx', index= False)
# a.to_excel('2012_integrar_4T12_1T13.xlsx', index= False)
# a.to_excel('2013_integrar_1T13_2T13.xlsx', index= False)
# a.to_excel('2013_integrar_2T13_3T13.xlsx', index= False)
# a.to_excel('2013_integrar_3T13_4T13.xlsx', index= False)
# a.to_excel('2013_integrar_4T13_1T14.xlsx', index= False)
# a.to_excel('2014_integrar_1T14_2T14.xlsx', index= False)
# a.to_excel('2014_integrar_2T14_3T14.xlsx', index= False)
# a.to_excel('2014_integrar_3T14_4T14.xlsx', index= False)
# a.to_excel('2014_integrar_4T14_1T15.xlsx', index= False)
# a.to_excel('2015_integrar_1T15_2T15.xlsx', index= False)
# a.to_excel('2015_integrar_2T15_3T15.xlsx', index= False)
# a.to_excel('2015_integrar_3T15_4T15.xlsx', index= False)
# a.to_excel('2015_integrar_4T15_1T16.xlsx', index= False)
# a.to_excel('2016_integrar_1T16_2T16.xlsx', index= False)
# a.to_excel('2016_integrar_2T16_3T16.xlsx', index= False)
# a.to_excel('2016_integrar_3T16_4T16.xlsx', index= False)
# a.to_excel('2016_integrar_4T16_1T17.xlsx', index= False)
# a.to_excel('2017_integrar_1T17_2T17.xlsx', index= False)
# a.to_excel('2017_integrar_2T17_3T17.xlsx', index= False)

# a.to_excel('2017_integrar_3T17_4T17.xlsx', index= False)

# a.to_excel('2017_integrar_4T17_1T18.xlsx', index= False)
# a.to_excel('2018_integrar_1T18_2T18.xlsx', index= False)
# a.to_excel('2018_integrar_2T18_3T18.xlsx', index= False)
# a.to_excel('2018_integrar_3T18_4T18.xlsx', index= False)
# a.to_excel('2018_integrar_4T18_1T19.xlsx', index= False)
# a.to_excel('2019_integrar_1T19_2T19.xlsx', index= False)
# a.to_excel('2019_integrar_2T19_3T19.xlsx', index= False)
# a.to_excel('2019_integrar_3T19_4T19.xlsx', index= False)
# a.to_excel('2019_integrar_4T19_1T20.xlsx', index= False)
# a.to_excel('2020_integrar_1T20_2T20.xlsx', index= False)
# a.to_excel('2020_integrar_2T20_3T20.xlsx', index= False)
# a.to_excel('2020_integrar_3T20_4T20.xlsx', index= False)
# a.to_excel('2020_integrar_4T20_1T21.xlsx', index= False)
# a.to_excel('2021_integrar_1T21_2T21.xlsx', index= False)
# a.to_excel('2021_integrar_2T21_3T21.xlsx', index= False)
# a.to_excel('2021_integrar_3T21_4T21.xlsx', index= False)
# a.to_excel('2021_integrar_4T21_1T22.xlsx', index= False)
# a.to_excel('2022_integrar_1T22_2T22.xlsx', index= False)
# a.to_excel('2022_integrar_2T22_3T22.xlsx', index= False)
# a.to_excel('2022_integrar_3T22_4T22.xlsx', index= False)
# a.to_excel('2022_integrar_4T22_1T23.xlsx', index= False)
# a.to_excel('2023_integrar_1T23_2T23.xlsx', index= False)
# a.to_excel('2023_integrar_2T23_3T23.xlsx', index= False)
# a.to_excel('2023_integrar_3T23_4T23.xlsx', index= False)
# a.to_excel('2023_integrar_4T23_1T24.xlsx', index= False)
# a.to_excel('2024_integrar_1T24_2T24.xlsx', index= False)


# observar
# a.to_excel('2024_integrar_1T24_3T24.xlsx', index= False)
# a.to_excel('2024_integrar_observar_1T20_3T20.xlsx', index= False)
# a.to_excel('2016_integrar_observar_1T16_3T16.xlsx', index= False)
# a.to_excel('2013_integrar_observar_1T13_3T13.xlsx', index= False)

# a.to_excel('2011_integrar_observar_1T11_3T11.xlsx', index= False)
# a.to_excel('2012_integrar_observar_1T12_3T12.xlsx', index= False)
# a.to_excel('2014_integrar_observar_1T14_3T14.xlsx', index= False)
# a.to_excel('2015_integrar_observar_1T15_3T15.xlsx', index= False)
# a.to_excel('2016_integrar_observar_1T16_3T16.xlsx', index= False)
# a.to_excel('2017_integrar_observar_1T17_3T17.xlsx', index= False)
# a.to_excel('2018_integrar_observar_1T18_3T18.xlsx', index= False)
# a.to_excel('2019_integrar_observar_1T19_3T19.xlsx', index= False)
# a.to_excel('2020_integrar_observar_1T20_3T20.xlsx', index= False)

# a.to_excel('2020_integrar_observar_2T20_4T20.xlsx', index= False)
# a.to_excel('2021_integrar_observar_1T21_3T21.xlsx', index= False)

# a.to_excel('2022_integrar_observar_1T22_3T22.xlsx', index= False)
# a.to_excel('2023_integrar_observar_1T23_3T23.xlsx', index= False)
# a.to_excel('2024_integrar_observar_1T24_3T24.xlsx', index= False)


# a.to_excel('2024_integrar_observar_base_2008_1T24_3T24.xlsx', index= False)


# a.to_excel('2024_a_integrar_observar_base_1T24_3T24.xlsx', index= False)

# a.to_excel('2024_b_integrar_observar_base_2T24_3T24.xlsx', index= False)

# a.to_excel('2024_bb_integrar_observar_base_2T24_3T24.xlsx', index= False)




##########################################################
# a.to_excel('integrar_3T22_4T22.xlsx', index= False)
# a.to_excel('integrar_4T22_1T23.xlsx', index= False)
# a.to_excel('integrar_1T23_2T23.xlsx', index= False)
# a.to_excel('integrar_2T23_3T23.xlsx', index= False)
# a.to_excel('integrar_3T23_4T23.xlsx', index= False)
# a.to_excel('integrar_4T23_1T24.xlsx', index= False)
# a.to_excel('integrar_1T24_2T24.xlsx', index= False)
# a.to_excel('integrar_2T24_3T24.xlsx', index= False)