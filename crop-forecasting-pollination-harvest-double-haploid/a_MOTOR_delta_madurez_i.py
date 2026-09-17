# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:05:57 2022

@author: s1073533
"""


import pandas as pd
import numpy as np
import datetime
arica = pd.read_excel('act_tot_20_09_2022.xlsx')

arica = arica[arica['LOC_NAME'] == 'ARICA']

columnas = ['Maturity', 'INPLTDT',  'INHVDT' ]

arica = arica[columnas]
M = arica
M = M[M['Maturity'].notna()]

"""
######
#------ SIEMBRA Y COSECHA
######
"""
M['INPLTDT'] = pd.to_datetime(M['INPLTDT'], format="%d-%m-%Y")
M['INHVDT'] = pd.to_datetime( M['INHVDT'] , format="%d-%m-%Y")
M['Maturity'] = M['Maturity'].astype("float")
M['DELTA_1'] =  (M['INHVDT'] - M['INPLTDT'])
M['DELTA_1'] = abs((M['DELTA_1'].apply(lambda x: x.days)))
# M['mes_siembra'] = pd.DatetimeIndex(M['INPLTDT']).month
M['semana_siembra'] =  M['INPLTDT'].dt.weekofyear
M = M[M['DELTA_1'].notna()]


"""
####--construir la tabla a proyectar ---#####
"""
# generar secuencia de madurez, por semana del año
myList1 = list(range(0, 17))
print("The given list is:", myList1)
tempList = list(myList1)
count =  17 * 5
# print("Number of Times to repeat the elements:",count)
for i in range(count):
    for element in tempList:
        myList1.append(element)
# print("The output list is:", myList1)

# generar secuencia de numero de semana del año
import numpy as np
x = np.array(list(range(1,53)))
K = np.repeat(x, 17)
# M = np.repeat(K, 5)
T = pd.DataFrame(K)
T = T.rename(columns = {0:'semana_siembra'}, inplace = False)
T['Maturity'] = pd.DataFrame(myList1)


X = M[['semana_siembra', 'Maturity']]
y = M.DELTA_1

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
    model =   XGBRegressor(n_estimators=65, learning_rate=0.09)
    model.fit(X_train, y_train, 
                 early_stopping_rounds=25, 
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

print("MAE from Approach, validación de lapsos:")  
print(round(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid),6))



"""
#######################################
### empecemos a predecir con la data T
#######################################
"""
# pero ya tenemos X e Y para predecir

from sklearn.preprocessing import LabelEncoder
import numpy as np

# Obtener la lista de variables categóricas.
s = (X.dtypes == 'object')
object_cols = list(s[s].index)

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
modelo = RandomForestRegressor(n_estimators= 65, random_state=3)
"""
from xgboost import XGBRegressor
modelo = XGBRegressor(n_estimators=70)
"""
modelo.fit(OH_X_entren, y)
# predecir
T['DELTA_est'] =  modelo.predict(OH_X_valido)
T['DELTA_est'] = round(T['DELTA_est'].astype('float'), 0)

r = T['Maturity']
# r.reset_index(drop=True)

S = T.sort_values(["semana_siembra",  "DELTA_est", "Maturity"], ascending=[True, True,  False])
S = S.reset_index()

del S['Maturity']
del S['index']

S['Maturity'] = r
# S.columns

S = S[['semana_siembra', 'Maturity', 'DELTA_est']]


# S.to_excel('DH_ind_delta_madurez.xlsx', index= False)


