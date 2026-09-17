# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 08:57:39 2023

@author: s1073533
"""
import pandas as pd
import numpy as np
import datetime
from a_MOTOR_G import tablaY
arica = pd.read_excel('act_tot_10_01_2023.xlsx')
columnas = ['REGION_CODE_CONTINENT',
            'Maturity', 'DESCRIPTION', 'CPU_ACT', 'INSTDCT', 
            'MATID_Ind', 'MAT_GENERATED' , 'BARCD_IND', 'PLACD_IND',
            'INPLTDT',  'INPOLDT', 'INPOLCT', 'INHVECT']

O = arica[columnas]
O['INPLTDT'] = pd.to_datetime(O['INPLTDT'], format="%d-%m-%Y")
O['INPOLDT'] = pd.to_datetime(O['INPOLDT'] , format="%d-%m-%Y")
O = O.sort_values(by=['INPLTDT'],  ascending=True)
O['DELTA_1'] =  (O['INPOLDT'] - O['INPLTDT'])
O['DELTA_1'] = abs((O['DELTA_1'].apply(lambda x: x.days)))

# obtener semana de floración
O['semana_siembra'] = O['INPLTDT'].dt.weekofyear
O['semana_poli'] = O['INPOLDT'].dt.weekofyear
O['semana_siembra'] = O['semana_siembra'].astype("float")
O['semana_poli'] = O['semana_poli'].astype("float")



O['MAT_GENERATED'] = O['MAT_GENERATED'].astype('object')
O['MATID_Ind'] = O['MATID_Ind'].astype('object')
O['BARCD_IND'] = O['BARCD_IND'].astype('object')

O['breeding'] = O['MATID_Ind'].str[0:5].replace('(\d)', '', regex=True)
O['breeding'] = O['breeding'].astype('object')

O['REGION_CODE_CONTINENT'] = O['REGION_CODE_CONTINENT'].astype("object")
O['DESCRIPTION'] = O['DESCRIPTION'].astype("object")
O['CPU_ACT'] = O['CPU_ACT'].astype("float")
O['Maturity'] = O['Maturity'].astype("float")
O['sector'] = O['PLACD_IND'].astype("object")
O['CPU_ACT'] =  O['CPU_ACT'].astype("float")
O['INSTDCT'] =  O['INSTDCT'].astype("float")
O['INPOLCT'] =  O['INPOLCT'].astype("float")
O['INHVECT'] =  O['INHVECT'].astype("float")

O = O[O['CPU_ACT']> 0]
O['cpu_vs_stdcount'] = round(O['INSTDCT'] / O['CPU_ACT'], 4)
O = O[O['INSTDCT']> 0]
O['stdcount_vs_polct'] = round(O['INPOLCT'] / O['INSTDCT'], 4)
O = O[O['INPOLCT']> 0]
O['polct_vs_hrvst'] = round(O['INHVECT'] / O['INPOLCT'], 4)

R = O


"""##### DATA A PROYECTAR---#####"""
from a_MOTOR_G import tablaY
# tablaY.columns
program_H = tablaY[['fecha_histórica', 'MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
                    'REGION_CODE_CONTINENT', 'DESCRIPTION',  'sector',
                    'Maturity', 'codigo', 'FECHA_1', 'FECHA_2_est',
                    'FECHA_2', 'FECHA_POLI', 'tipo_poli',
                    'FECHA_3_est', 'FECHA_3', 'SEMANA_SIEMBRA_REAL',
                    'SEMANA_FLORACION_ESTIMADA', 'SEMANA_FLORACION_REAL',
                    'SEMANA_COSECHA_ESTIMADA', 'SEMANA_COSECHA_REAL']]

marchant_i = ['BARCD_IND', 'CPU_ACT', 'INSTDCT', 'INPOLCT', 'INHVECT']
O1 = O[marchant_i]
program_H = program_H.merge(O1, how='left', on='BARCD_IND')


"""####--- FIN ---####"""


columna_I =['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'breeding', 'Maturity', 
            'CPU_ACT', 'INSTDCT',  
            'semana_siembra', 'semana_poli', 'INPOLCT']
O = O.dropna()

X = O[columna_I]
X = X.drop(['INPOLCT'],  axis=1)
# construir la vaiable dependiente, explicada
y = O.INPOLCT
y = y.astype('float')


"""
#####--- VALIDACION I---#####
# hasta acá, pero lo de abajo es para validar un modelo
# de predicción
##################
"""
import pandas as pd
from sklearn.model_selection import train_test_split


# Divide data into training and validation subsets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                                random_state=0)

# Echamos un vistazo a los datos de entrenamiento con el método head()
#a continuación.
X_train.head()

# Obtener la lista de variables categóricas.
s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)

print("Categorical variables:")
print(object_cols)

"""
función de validación 
"""

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Function for comparing different approaches
# Función para comparar diferentes enfoques.
def score_dataset(X_train, X_valid, y_train, y_valid):
    model =  RandomForestRegressor(n_estimators = 68, random_state=4)
    model.fit(X_train, y_train)
    """model =   XGBRegressor(n_estimators= 66, learning_rate=0.088 , random_state=3)
    model.fit(X_train, y_train, 
                 early_stopping_rounds=5, 
                 eval_set=[(X_valid, y_valid)], 
                 verbose=False)"""
    preds = model.predict(X_valid)
    #print(preds)
    return mean_absolute_error(y_valid, preds)


"""
####
Puntuación del Método ONeHotEncder (codificación de etiquetas)
####
"""
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
import numpy as np

# Make copy to avoid changing original data 
# Haga una copia para evitar cambiar los datos originales
# Use as many lines of code as you need!

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

print("MAE from Approach 1, considerando las madureces:")  
print(round(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid),2))

