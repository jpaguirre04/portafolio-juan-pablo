# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 09:43:27 2022

@author: s1073533
"""


import pandas as pd
import numpy as npn
import datetime
arica = pd.read_excel('act_tot_18_11_2022.xlsx')
xkl = arica

arica = arica[arica['LOC_NAME'] == 'ARICA']

columnas = ['REGION_CODE_CONTINENT',
            'Maturity', 'DESCRIPTION', 'CPU_ACT',
            'INSTDCT', 'MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
            'PLACD_IND', 'INPLTDT',  'INPOLDT',
            'INPOLCT']

# 'INSTDCT' ,
O = arica[columnas]

O['INPLTDT'] = pd.to_datetime(O['INPLTDT'], format="%d-%m-%Y")
O['INPOLDT'] = pd.to_datetime(O['INPOLDT'] , format="%d-%m-%Y")
O = O.sort_values(by=['INPLTDT'],  ascending=True)
O['DELTA_1'] =  (O['INPOLDT'] - O['INPLTDT'])
O['DELTA_1'] = abs((O['DELTA_1'].apply(lambda x: x.days)))


# obtener semana de floración 
O['semana_siembra'] = O['INPLTDT'].dt.weekofyear
O['semana_poli'] = O['INPOLDT'].dt.weekofyear

O['MAT_GENERATED'] = O['MAT_GENERATED'].astype('object')
O['MATID_Ind'] = O['MATID_Ind'].astype('object')
O['BARCD_IND'] = O['BARCD_IND'].astype('object')


O['breader'] = O['MATID_Ind'].str[0:5].replace('(\d)', '', regex=True)
O['breader'] = O['breader'].astype('object')

O['REGION_CODE_CONTINENT'] = O['REGION_CODE_CONTINENT'].astype("object")
O['DESCRIPTION'] = O['DESCRIPTION'].astype("object")
O['CPU_ACT'] = O['CPU_ACT'].astype("float")
O['Maturity'] = O['Maturity'].astype("float")
O['PLACD_IND'] = O['PLACD_IND'].astype("object")
O['semana_siembra'] = O['semana_siembra'].astype("float")
O['semana_poli'] = O['semana_poli'].astype("float")
O['CPU_ACT'] =  O['CPU_ACT'].astype("float")
O['INPOLCT'] =  O['INPOLCT'].astype("float")
O['INSTDCT'] =  O['INSTDCT'].astype("float")
hoo = O[['BARCD_IND', 'INSTDCT']]
hoo = hoo.dropna()
# INSTDCT
# O.columns

#######################################################################
# matriz T 
from a_MOTOR_G import tablaY
T =  tablaY

# T.columns
T = T.rename(columns = {"codigo" : "breader",
                        "sector" : "PLACD_IND",
                        "SEMANA_SIEMBRA_REAL" : "semana_siembra"})

T['breader'] = T['breader'].astype('object')
T['REGION_CODE_CONTINENT'] = T['REGION_CODE_CONTINENT'].astype('object')
T['DESCRIPTION'] = T['DESCRIPTION'].astype('object')
T['semana_siembra'] = T['semana_siembra'].astype("float64")
T['Maturity'] = T['Maturity'].astype("float64")
T['PLACD_IND'] = T['PLACD_IND'].astype('object')
T =  T.merge(hoo, how='left', on='BARCD_IND')

# print(T.isnull().sum())

# fin de la matrix T
columna_III =['REGION_CODE_CONTINENT', 'DESCRIPTION',
              'PLACD_IND', 'semana_siembra', 
              'breader', 'Maturity', 'INSTDCT', 'INPOLCT']

# 'week_n_INPOLDT'  ,  'week_n_INPLTDT', , 'DELTA_1'
O =  O[O['DELTA_1'].notna()]
O =  O[O['INSTDCT'].notna()]
# print(O.isnull().sum())

X = O[columna_III]
X = X.drop(['INPOLCT'],  axis=1)

# consstruir la vaiable dependiente, explicada
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
Definir la función para medir la calidad de cada enfoque
Definimos una función score_dataset() para comparar los
tres enfoques diferentes para tratar con variables categóricas.
Esta función informa el error absoluto medio (MAE) de un modelo
de bosque aleatorio. En general, queremos que el MAE sea lo
más bajo posible.
"""

# from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Function for comparing different approaches
# Función para comparar diferentes enfoques.
def score_dataset(X_train, X_valid, y_train, y_valid):
    # model =  RandomForestRegressor(n_estimators = 50, random_state=0)
    # model.fit(X_train, y_train)
    model =   XGBRegressor(n_estimators= 66, learning_rate=0.088 , random_state=3)
    model.fit(X_train, y_train, 
                 early_stopping_rounds=5, 
                 eval_set=[(X_valid, y_valid)], 
                 verbose=False)
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



"""
#######################################
### empecemos a predecir con la data T
#######################################
"""
# pero ya tenemos X e Y para predecir

from sklearn.preprocessing import LabelEncoder
import numpy as np

# Obtener la lista de variables categóricas.
# s = (X.dtypes == 'object')
# object_cols = list(s[s].index)

print("Variables Categóricas:")
print(object_cols)

# Make copy to avoid changing original data 
# Haga una copia para evitar cambiar los datos originales
label_X = X.copy()

label_T = T[label_X.columns]

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_X = pd.DataFrame(OH_encoder.fit_transform(X[object_cols]))
OH_label_T = pd.DataFrame(OH_encoder.transform(label_T[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_X.index = X.index
OH_label_T.index = label_T.index

# Remove categorical columns (will replace with one-hot encoding)
num_X = X.drop(object_cols, axis=1)
num_label_T = label_T.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_entren = pd.concat([num_X, OH_cols_X], axis=1)
OH_X_valido = pd.concat([num_label_T, OH_label_T], axis=1)


from sklearn.ensemble import RandomForestRegressor
modelo = RandomForestRegressor(n_estimators= 66, random_state=3)
"""
from xgboost import XGBRegressor
modelo = XGBRegressor(n_estimators=70)
"""
modelo.fit(OH_X_entren, y)
# predecir
T['INPOLCT_est'] =  modelo.predict(OH_X_valido)
T['INPOLCT_est'] = T['INPOLCT_est'].astype('float') 

 
"""
#####################
# INFORMATION CROSS
#####################
"""
xkl = pd.DataFrame(xkl)
xkl = xkl[xkl['LOC_NAME'] == 'ARICA']
marchant = ['BARCD_IND', 'INPOLCT']
xkl = xkl[marchant]

xkl['BARCD_IND'] = xkl['BARCD_IND'].astype('object')
xkl['INPOLCT'] = xkl['INPOLCT'].astype('float')
xkl = xkl.dropna()

T =  T.merge(xkl, how='left', on='BARCD_IND')

T = T.rename(columns={"INPOLCT": "INPOLCT_real"})
T['INPOLCT_real'] = T['INPOLCT_real'].astype("float")
T['error'] = T['INPOLCT_est'] - T['INPOLCT_real']
T['error'] = T['error'].astype('float')
T['MAT_GENERATED'] = T['MAT_GENERATED'].astype('str')
K = T
T = T.rename(columns={"error" : "error_INPOLCT_est"})

# T['error_INPOLCT_est'].hist()
T1 = T[T['INPOLCT_real'].notnull()]
T2 = T[T['INPOLCT_real'].isnull()]

T1['tipo_poli'] = 'realizada'
T2['tipo_poli'] = 'pendiente'


T1['INPOLCT'] = T1['INPOLCT_real']
T2['INPOLCT'] = T2['INPOLCT_est']

del T1['INPOLCT_real']
del T2['INPOLCT_est']

del T2['INPOLCT_real']
del T1['INPOLCT_est']

# T1.columns
# T2.columns

Ty =  pd.concat([T1, T2]).drop_duplicates(subset='BARCD_IND').reset_index(drop=True)
del Ty['error_INPOLCT_est']
# Ty['INPOLCT'] = round(Ty['INPOLCT'], 0)

Ty.columns


Ty['SEMANA_FLORACION_ESTIMADA'] = Ty['SEMANA_FLORACION_ESTIMADA'].astype('object')
Ty['SEMANA_FLORACION_REAL'] = Ty['SEMANA_FLORACION_REAL'].astype('object')
Ty['INPOLCT'] = Ty['INPOLCT'].astype('float64')

Ty = Ty[['fecha_histórica', 'MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
        'REGION_CODE_CONTINENT', 'DESCRIPTION', 'unidades', 'PLACD_IND',
        'Maturity', 'breader', 'FECHA_1', 'periodo_f1', 'mes_año_f1', 'INSTDCT',
        'days_poli_est', 'FECHA_2_est', 'FECHA_2', 'FECHA_POLI', 'tipo_poli',
        'semana_B_est', 'mes_año_f2', 'periodo_f2', 'days_cosecha_est',
        'FECHA_3_est', 'FECHA_3', 'semana_siembra', 'SEMANA_FLORACION_ESTIMADA',
        'INPOLCT', 'SEMANA_FLORACION_REAL', 'SEMANA_COSECHA_ESTIMADA',
        'SEMANA_COSECHA_REAL', 
        ]]


# Ty.to_excel('La_Roca_Polinizadas_Inducción.xlsx', index= False)
  

tabla_A =  Ty.groupby(['SEMANA_FLORACION_ESTIMADA'])['INPOLCT'].sum() 
tabla_A.reindex 


tabla_B =  Ty.groupby(['SEMANA_FLORACION_REAL'])['INPOLCT'].sum()
tabla_B.reset_index


import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')
import numpy as np
import pandas as pd

fig = plt.figure()
ax = plt.axes()
plt.title('Errores de Polinizaciones')

y = K['error'].values
x = K['BARCD_IND'].values
plt.plot(x, y, 'o' , color = 'green')

K = K[K['error']<100]

K['error'].describe()


import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')
import numpy as np
import pandas as pd

fig = plt.figure()
ax = plt.axes()
plt.title('Errores de Polinizaciones')

y = K['error'].values
x = K['BARCD_IND'].values
plt.plot(x, y, 'o' , color = 'green')






