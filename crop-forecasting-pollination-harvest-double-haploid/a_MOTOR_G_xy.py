# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 07:24:37 2023

@author: s1073533
"""



"""
#######--- ES PARA ROBUSTECER LA DATA CON LAS CANTIDADES ---####
"""

import pandas as pd
from a_MOTOR_G import tablaY
from a_MOTOR import xy
# tablaY.columns


columnas = ['REGION_CODE_CONTINENT', 'Maturity', 'DESCRIPTION', 
            'CPU_ACT', 'INSTDCT',  'MATID_Ind', 'MAT_GENERATED',
            'BARCD_IND', 'PLACD_IND', 'INPLTDT', 'Heterotic Group',
            'INPOLDT', 'INHVDT', 'INPOLCT', 'INHVECT']

# 'INSTDCT' ,  '# ProcessEARS (Lab)'
O = xy[columnas]

O['MAT_GENERATED'] = O['MAT_GENERATED'].astype('object')
O['MATID_Ind'] = O['MATID_Ind'].astype('object')
O['BARCD_IND'] = O['BARCD_IND'].astype('object')
O['breeding'] = O['MATID_Ind'].str[0:5].replace('(\d)', '', regex=True)
O['breeding'] = O['breeding'].astype('object')
O =  O.rename(columns = {'Heterotic Group' : 'Heterotic_Group'})
O['Heterotic_Group'] = O['Heterotic_Group'].fillna('faltante')
O['REGION_CODE_CONTINENT'] = O['REGION_CODE_CONTINENT'].astype("object")
O['DESCRIPTION'] = O['DESCRIPTION'].astype("object")
O['Maturity'] = O['Maturity'].astype("float")
O['PLACD_IND'] = O['PLACD_IND'].astype("object")
O['INPLTDT'] = pd.to_datetime(O['INPLTDT'], format="%d-%m-%Y")
O['INPOLDT'] = pd.to_datetime(O['INPOLDT'] , format="%d-%m-%Y")
O['INHVDT'] = pd.to_datetime(O['INHVDT'] , format="%d-%m-%Y")
O = O.sort_values(by=['INPLTDT'],  ascending=True)
O['DELTA_1'] =  (O['INPOLDT'] - O['INPLTDT'])
O['DELTA_1'] = abs((O['DELTA_1'].apply(lambda x: x.days)))
O['DELTA_2'] =  (O['INHVDT'] - O['INPOLDT'])
O['DELTA_2'] = abs((O['DELTA_2'].apply(lambda x: x.days)))
O['semana_siembra'] = O['INPLTDT'].dt.weekofyear
O['semana_poli'] = O['INPOLDT'].dt.weekofyear
O['semana_siembra'] = O['semana_siembra'].astype("float")
O['semana_poli'] = O['semana_poli'].astype("float")
O['CPU_ACT'] =  O['CPU_ACT'].astype("float")
O['INSTDCT'] =  O['INSTDCT'].astype("float")
O['INPOLCT'] =  O['INPOLCT'].astype("float")
O['INHVECT'] =  O['INHVECT'].astype("float")

base_fill = O
base_fill['tipo_INSTDCT'] = base_fill['INSTDCT'].notnull()
base_fill['tipo_INPOLCT'] = base_fill['INPOLCT'].notnull()
base_fill['tipo_INHVECT'] = base_fill['INHVECT'].notnull()

K = base_fill[['CPU_ACT', 'INSTDCT', 'INPOLCT', 'INHVECT']]
# print(K.isnull().sum())
K.corr()

A = O
B = O
C = O
# print(A.isnull().sum())
# S1 = A[A['Maturity'].isnull()] # ES PARA COMPROBAR SI LA MADUREZ ESTÁ VACÍA

"""
#######--- recuperar INSTDCT ---####
"""
S1 = A[['MATID_Ind', 'BARCD_IND', 'REGION_CODE_CONTINENT',
        'DESCRIPTION', 'Heterotic_Group', 'breeding',
        'Maturity', 'CPU_ACT', 'INSTDCT']]
S1 = S1[S1['INSTDCT'].isnull()]
del S1['INSTDCT']
# pronosticar el statcount
columna_I =['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'Heterotic_Group', 'breeding', 'Maturity', 
            'CPU_ACT', 'INSTDCT']
A = A[columna_I]

# print(A.isnull().sum())
A = A[A['INSTDCT'].notnull()]

X = A[columna_I]
X = X.drop(['INSTDCT'],  axis=1)
# construir la vaiable dependiente, explicada
y = A.INSTDCT
y = y.astype('float')


"""
Definir la función para medir la calidad de cada enfoque
Definimos una función score_dataset() para comparar los
tres enfoques diferentes para tratar con variables categóricas.
Esta función informa el error absoluto medio (MAE) de un modelo
de bosque aleatorio. En general, queremos que el MAE sea lo
más bajo posible.
"""
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Function for comparing different approaches
# Función para comparar diferentes enfoques.
def score_dataset(X_train, X_valid, y_train, y_valid):
    model =  RandomForestRegressor(n_estimators = 68, random_state=4)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    #print(preds)
    return mean_absolute_error(y_valid, preds)

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

label_T = S1[label_X.columns]

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

modelo = RandomForestRegressor(n_estimators= 68, random_state=4)
modelo.fit(OH_X_entren, y)

# predecir
S1['INSTDCT'] =  modelo.predict(OH_X_valido)
S1['INSTDCT'] = S1['INSTDCT'].astype('int32') 
COL =  ['BARCD_IND',  'INSTDCT']

S = S1[COL]

# madurez.to_excel('madurez_mat_generated.xlsx', index= False)

# madurez['Maturity'].hist()
# madurez['Maturity'].describe()

"""
###--- INFORMATION CROSS ---####
"""
base_fill = base_fill.set_index('BARCD_IND')
base_fill['INSTDCT'] = base_fill['INSTDCT'].combine_first(S.set_index('BARCD_IND')['INSTDCT'])
base_fill.reset_index(level=0, inplace=True)

"""
#######--- recuperar INPOLCT ---####
"""
S2 = base_fill[['MATID_Ind', 'BARCD_IND', 'REGION_CODE_CONTINENT',
                'DESCRIPTION', 'Heterotic_Group', 'breeding',
                'Maturity', 'INSTDCT', 'INPOLCT']]
S2 = S2[(S2['INPOLCT'].isnull()) & (S2['INSTDCT'].notnull())]
del S2['INPOLCT']

# print(S2.isnull().sum())
# pronosticar el statcount
columna_II =['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'Heterotic_Group', 'breeding', 'Maturity', 
            'INSTDCT', 'INPOLCT']
base_fill_i = base_fill[columna_II]
# print(A.isnull().sum())
base_fill_i = base_fill_i[base_fill_i['INPOLCT'].notnull()]
X1 = base_fill_i[columna_II]
X1 = X1.drop(['INPOLCT'],  axis=1)
# construir la vaiable dependiente, explicada
y1 = base_fill_i.INPOLCT
y1 = y1.astype('float')

"""
#####--- VALIDACION II---#####
##################
"""
import pandas as pd
from sklearn.model_selection import train_test_split
# Divide data into training and validation subsets
X1_train, X1_valid, y1_train, y1_valid = train_test_split(X1, y1, train_size=0.8, test_size=0.2,
                                                                   random_state=0)
# Echamos un vistazo a los datos de entrenamiento con el método head()
#a continuación.
X1_train.head()
# Obtener la lista de variables categóricas.
l = (X1_train.dtypes == 'object')
objecto_columna = list(l[l].index)

print("Variables Categóricas:")
print(objecto_columna)

"""
####
Puntuación del Método OneHotEncoder (codificación de etiquetas)
####
"""
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
import numpy as np

# Apply one-hot encoder to each column with categorical data
OH1_codificador = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH1_colu_train = pd.DataFrame(OH1_codificador.fit_transform(X1_train[objecto_columna]))
OH1_colu_valid = pd.DataFrame(OH1_codificador.transform(X1_valid[objecto_columna]))

# One-hot encoding removed index; put it back
OH1_colu_train.index = X1_train.index
OH1_colu_valid.index = X1_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X1_train = X1_train.drop(objecto_columna, axis=1)
num_X1_valid = X1_valid.drop(objecto_columna, axis=1)

# Add one-hot encoded columns to numerical features
OH_X1_train = pd.concat([num_X1_train, OH1_colu_train], axis=1)
OH_X1_valid = pd.concat([num_X1_valid, OH1_colu_valid], axis=1)

print("MAE from Approach 2, en INDUCCIÓN desde poli a stdcount")  
print(round(score_dataset(OH_X1_train, OH_X1_valid, y1_train, y1_valid),4))



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
label_X1 = X1.copy()
label_T1 = S2[label_X1.columns]

# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder , OneHotEncoder

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_X1 = pd.DataFrame(OH_encoder.fit_transform(X1[object_cols]))
OH_label_T1 = pd.DataFrame(OH_encoder.transform(label_T1[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_X1.index = X1.index
OH_label_T1.index = label_T1.index

# Remove categorical columns (will replace with one-hot encoding)
num_X1 = X1.drop(object_cols, axis=1)
num_label_T1 = label_T1.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X1_entren = pd.concat([num_X1, OH_cols_X1], axis=1)

# OH_X_entren.columns
OH_X1_valido = pd.concat([num_label_T1, OH_label_T1], axis=1)

from sklearn.ensemble import RandomForestRegressor
modelo = RandomForestRegressor(n_estimators= 70, random_state=5)
modelo.fit(OH_X1_entren, y1)

# predecir
S2['INPOLCT'] =  modelo.predict(OH_X1_valido)
S2['INPOLCT'] = S2['INPOLCT'].astype('int32') 
COL =  ['BARCD_IND',  'INPOLCT']

S2 = S2[COL]
# madurez.to_excel('madurez_mat_generated.xlsx', index= False)
# madurez['Maturity'].hist()
# madurez['Maturity'].describe()

"""
###--- INFORMATION CROSS ---####
"""
base_fill = base_fill.set_index('BARCD_IND')
base_fill['INPOLCT'] = base_fill['INPOLCT'].combine_first(S2.set_index('BARCD_IND')['INPOLCT'])
base_fill.reset_index(level=0, inplace=True)


"""
#######--- recuperar INHVECT ---####
"""
S3 = base_fill[['MATID_Ind', 'BARCD_IND', 'REGION_CODE_CONTINENT',
        'DESCRIPTION', 'Heterotic_Group', 'breeding',
        'Maturity', 'INPOLCT', 'INHVECT']]
S3 = S3[(S3['INHVECT'].isnull()) & (S3['INPOLCT'].notnull())]
del S3['INHVECT']

# print(S3.isnull().sum())

# pronosticar el statcount
columna_III =['REGION_CODE_CONTINENT', 'DESCRIPTION',
              'Heterotic_Group', 'breeding', 'Maturity', 
              'INPOLCT', 'INHVECT']
base_fill_ii = base_fill[columna_III]
# print(C.isnull().sum())
base_fill_ii = base_fill_ii[base_fill_ii['INHVECT'].notnull()]
X2 = base_fill_ii[columna_III]
X2 = X2.drop(['INHVECT'],  axis=1)
# construir la vaiable dependiente, explicada
y2 = base_fill_ii.INHVECT
y2 = y2.astype('float')

"""
#####--- VALIDACION II---#####
##################
"""
import pandas as pd
from sklearn.model_selection import train_test_split
# Divide data into training and validation subsets
X2_train, X2_valid, y2_train, y2_valid = train_test_split(X2, y2, train_size=0.8, test_size=0.2,
                                                                   random_state=0)
# Echamos un vistazo a los datos de entrenamiento con el método head()
#a continuación.
X2_train.head()
# Obtener la lista de variables categóricas.
l = (X2_train.dtypes == 'object')
objecto_columna = list(l[l].index)

print("Variables Categóricas:")
print(objecto_columna)

"""
####
Puntuación del Método OneHotEncoder (codificación de etiquetas)
####
"""
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
import numpy as np

# Apply one-hot encoder to each column with categorical data
OH2_codificador = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH2_colu_train = pd.DataFrame(OH2_codificador.fit_transform(X2_train[objecto_columna]))
OH2_colu_valid = pd.DataFrame(OH2_codificador.transform(X2_valid[objecto_columna]))

# One-hot encoding removed index; put it back
OH2_colu_train.index = X2_train.index
OH2_colu_valid.index = X2_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X2_train = X2_train.drop(objecto_columna, axis=1)
num_X2_valid = X2_valid.drop(objecto_columna, axis=1)

# Add one-hot encoded columns to numerical features
OH_X2_train = pd.concat([num_X2_train, OH2_colu_train], axis=1)
OH_X2_valid = pd.concat([num_X2_valid, OH2_colu_valid], axis=1)

print("MAE from Approach 2, en INDUCCIÓN desde poli a stdcount")  
print(round(score_dataset(OH_X2_train, OH_X2_valid, y2_train, y2_valid),4))



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
label_X2 = X2.copy()
label_T2 = S3[label_X2.columns]

# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder , OneHotEncoder

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_X2 = pd.DataFrame(OH_encoder.fit_transform(X2[object_cols]))
OH_label_T2 = pd.DataFrame(OH_encoder.transform(label_T2[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_X2.index = X2.index
OH_label_T2.index = label_T2.index

# Remove categorical columns (will replace with one-hot encoding)
num_X2 = X2.drop(object_cols, axis=1)
num_label_T2 = label_T2.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X2_entren = pd.concat([num_X2, OH_cols_X2], axis=1)

# OH_X_entren.columns
OH_X2_valido = pd.concat([num_label_T2, OH_label_T2], axis=1)

from sklearn.ensemble import RandomForestRegressor
modelo = RandomForestRegressor(n_estimators= 68, random_state=4)
modelo.fit(OH_X2_entren, y2)

# predecir
S3['INHVECT'] =  modelo.predict(OH_X2_valido)
S3['INHVECT'] = S3['INHVECT'].astype('int32') 
COL =  ['BARCD_IND',  'INHVECT']

S3 = S3[COL]
# madurez.to_excel('madurez_mat_generated.xlsx', index= False)
# madurez['Maturity'].hist()
# madurez['Maturity'].describe()

"""
###--- INFORMATION CROSS ---####
"""
base_fill = base_fill.set_index('BARCD_IND')
base_fill['INHVECT'] = base_fill['INHVECT'].combine_first(S3.set_index('BARCD_IND')['INHVECT'])
base_fill.reset_index(level=0, inplace=True)

# print(base_fill.isnull().sum())

base_fill = base_fill[['BARCD_IND', 'REGION_CODE_CONTINENT', 'Maturity', 'DESCRIPTION',
                        'MATID_Ind', 'MAT_GENERATED', 'PLACD_IND', 'INPLTDT', 
                        'Heterotic_Group', 'INPOLDT', 'INHVDT', 'CPU_ACT', 'INSTDCT',
                        'tipo_INSTDCT', 'INPOLCT', 'tipo_INPOLCT', 'INHVECT',
                        'tipo_INHVECT', 'breeding', 'DELTA_1', 'DELTA_2', 
                        'semana_siembra', 'semana_poli',]]

"""
base_fill = base_fill[(base_fill['CPU_ACT'] > base_fill['INSTDCT']) & 
                      (base_fill['INSTDCT'] > base_fill['INPOLCT']) & 
                      (base_fill['INPOLCT'] > base_fill['INHVECT'])]
"""