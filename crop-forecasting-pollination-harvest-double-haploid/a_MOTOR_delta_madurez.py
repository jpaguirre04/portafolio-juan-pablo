# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 07:20:03 2022

@author: s1073533
"""


import pandas as pd
import numpy as np
import datetime
arica = pd.read_excel('act_tot_23_08_2022.xlsx')

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

T1 =  T[T['semana_siembra'] ==1] 
T1['DELTA_est'] = T1['DELTA_est'].sort_values().values

T2 =  T[T['semana_siembra'] ==2] 
T2['DELTA_est'] = T2['DELTA_est'].sort_values().values

T3 =  T[T['semana_siembra'] ==3] 
T3['DELTA_est'] = T3['DELTA_est'].sort_values().values

T4 =  T[T['semana_siembra'] ==4] 
T4['DELTA_est'] = T4['DELTA_est'].sort_values().values

T5 =  T[T['semana_siembra'] ==5] 
T5['DELTA_est'] = T5['DELTA_est'].sort_values().values

T6 =  T[T['semana_siembra'] ==6] 
T6['DELTA_est'] = T6['DELTA_est'].sort_values().values

T7 =  T[T['semana_siembra'] ==7] 
T7['DELTA_est'] = T7['DELTA_est'].sort_values().values

T8 =  T[T['semana_siembra'] ==8] 
T8['DELTA_est'] = T8['DELTA_est'].sort_values().values

T9 =  T[T['semana_siembra'] ==9] 
T9['DELTA_est'] = T9['DELTA_est'].sort_values().values

T10 =  T[T['semana_siembra'] ==10] 
T10['DELTA_est'] = T10['DELTA_est'].sort_values().values

T11 =  T[T['semana_siembra'] ==11] 
T11['DELTA_est'] = T11['DELTA_est'].sort_values().values

T12 =  T[T['semana_siembra'] ==12] 
T12['DELTA_est'] = T12['DELTA_est'].sort_values().values

T13 =  T[T['semana_siembra'] ==13] 
T13['DELTA_est'] = T13['DELTA_est'].sort_values().values

T14 =  T[T['semana_siembra'] ==14] 
T14['DELTA_est'] = T14['DELTA_est'].sort_values().values

T15 =  T[T['semana_siembra'] ==15] 
T15['DELTA_est'] = T15['DELTA_est'].sort_values().values

T16 =  T[T['semana_siembra'] ==16] 
T16['DELTA_est'] = T16['DELTA_est'].sort_values().values

T17 =  T[T['semana_siembra'] ==17] 
T17['DELTA_est'] = T17['DELTA_est'].sort_values().values

T18 =  T[T['semana_siembra'] ==18] 
T18['DELTA_est'] = T18['DELTA_est'].sort_values().values

T19 =  T[T['semana_siembra'] ==19] 
T19['DELTA_est'] = T19['DELTA_est'].sort_values().values

T20 =  T[T['semana_siembra'] ==20] 
T20['DELTA_est'] = T20['DELTA_est'].sort_values().values

T21 =  T[T['semana_siembra'] ==21] 
T21['DELTA_est'] = T21['DELTA_est'].sort_values().values

T22 =  T[T['semana_siembra'] ==22] 
T22['DELTA_est'] = T22['DELTA_est'].sort_values().values

T23 =  T[T['semana_siembra'] ==23] 
T23['DELTA_est'] = T23['DELTA_est'].sort_values().values

T24 =  T[T['semana_siembra'] ==24] 
T24['DELTA_est'] = T24['DELTA_est'].sort_values().values

T25 =  T[T['semana_siembra'] ==25] 
T25['DELTA_est'] = T25['DELTA_est'].sort_values().values

T26 =  T[T['semana_siembra'] ==26] 
T26['DELTA_est'] = T26['DELTA_est'].sort_values().values

T27 =  T[T['semana_siembra'] ==27] 
T27['DELTA_est'] = T27['DELTA_est'].sort_values().values

T28 =  T[T['semana_siembra'] ==28] 
T28['DELTA_est'] = T28['DELTA_est'].sort_values().values

T29 =  T[T['semana_siembra'] ==29] 
T29['DELTA_est'] = T29['DELTA_est'].sort_values().values

T30 =  T[T['semana_siembra'] ==30] 
T30['DELTA_est'] = T30['DELTA_est'].sort_values().values

T31 =  T[T['semana_siembra'] ==31] 
T31['DELTA_est'] = T31['DELTA_est'].sort_values().values

T32 =  T[T['semana_siembra'] ==32] 
T32['DELTA_est'] = T32['DELTA_est'].sort_values().values

T33 =  T[T['semana_siembra'] ==33] 
T33['DELTA_est'] = T33['DELTA_est'].sort_values().values

T34 =  T[T['semana_siembra'] ==34] 
T34['DELTA_est'] = T34['DELTA_est'].sort_values().values

T35 =  T[T['semana_siembra'] ==35] 
T35['DELTA_est'] = T35['DELTA_est'].sort_values().values

T36 =  T[T['semana_siembra'] ==36] 
T36['DELTA_est'] = T36['DELTA_est'].sort_values().values

T37 =  T[T['semana_siembra'] ==37] 
T37['DELTA_est'] = T37['DELTA_est'].sort_values().values

T38 =  T[T['semana_siembra'] ==38] 
T38['DELTA_est'] = T38['DELTA_est'].sort_values().values

T39 =  T[T['semana_siembra'] ==39] 
T39['DELTA_est'] = T39['DELTA_est'].sort_values().values

T40 =  T[T['semana_siembra'] ==40] 
T40['DELTA_est'] = T40['DELTA_est'].sort_values().values

T41 =  T[T['semana_siembra'] ==41] 
T41['DELTA_est'] = T41['DELTA_est'].sort_values().values

T42 =  T[T['semana_siembra'] ==42] 
T42['DELTA_est'] = T42['DELTA_est'].sort_values().values

T43 =  T[T['semana_siembra'] ==43] 
T43['DELTA_est'] = T43['DELTA_est'].sort_values().values

T44 =  T[T['semana_siembra'] ==44] 
T44['DELTA_est'] = T44['DELTA_est'].sort_values().values

T45 =  T[T['semana_siembra'] == 45] 
T45['DELTA_est'] = T45['DELTA_est'].sort_values().values

T46 =  T[T['semana_siembra'] ==46] 
T46['DELTA_est'] = T46['DELTA_est'].sort_values().values

T47 =  T[T['semana_siembra'] ==47] 
T47['DELTA_est'] = T47['DELTA_est'].sort_values().values

T48 =  T[T['semana_siembra'] ==48] 
T48['DELTA_est'] = T48['DELTA_est'].sort_values().values

T49 =  T[T['semana_siembra'] ==49] 
T49['DELTA_est'] = T49['DELTA_est'].sort_values().values

T50 =  T[T['semana_siembra'] ==50] 
T50['DELTA_est'] = T50['DELTA_est'].sort_values().values

T51 =  T[T['semana_siembra'] ==51] 
T51['DELTA_est'] = T51['DELTA_est'].sort_values().values

T52 =  T[T['semana_siembra'] ==52] 
T52['DELTA_est'] = T52['DELTA_est'].sort_values().values


S = pd.concat([T1, T2, T3, T4, T5, T6, T7, T8, T9, T10,
               T11, T12, T13, T14, T15, T16, T17, T18, T19, T20,
               T21, T22, T23, T24, T25, T26, T27, T28, T29, T30,
               T31, T32, T33, T34, T35, T36, T37, T38, T39, T40,
               T41, T42, T43, T44, T45, T46, T47, T48, T49, T50,
               T51, T52 ])

# S.to_excel('DH_ind_delta_madurez.xlsx', index= False)
