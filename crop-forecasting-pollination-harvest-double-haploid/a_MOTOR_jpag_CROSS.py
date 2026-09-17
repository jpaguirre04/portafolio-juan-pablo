# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 15:18:23 2022

@author: s1073533
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:02:05 2022

@author: s1073533
"""
# SIEMBRA A FLORACIONES 
# with RANDOM FOREST REGRESSION
"""
#######---- MOTOR ----#######
"""
import pandas as pd
import numpy as np
import datetime
# DATA
arica = pd.read_excel('act_tot_09_12_2022.xlsx')
chavi = arica
arica = arica[arica['LOC_NAME'] == 'ARICA']

"""
###----PREPARAR LA DATA  INDUCCIÓN----###
"""
O = arica[['REGION_CODE_CONTINENT', 'MATID_Ind',
           'CPU_ACT', 'MAT_GENERATED', 'BARCD_IND',
           'DESCRIPTION',  'PLACD_IND', 'Maturity', 
           'INPLTDT', 'INPOLDT', 'INHVDT']]

O['INPLTDT'] = pd.to_datetime(O['INPLTDT'], format="%d-%m-%Y")
O['INPOLDT'] = pd.to_datetime(O['INPOLDT'] , format="%d-%m-%Y")
O['INHVDT'] = pd.to_datetime(O['INHVDT'], format="%d-%m-%Y")
O['MAT_GENERATED'] = O['MAT_GENERATED'].astype('object')
O['MATID_Ind'] = O['MATID_Ind'].astype('object')
O['BARCD_IND'] = O['BARCD_IND'].astype('object')
O['breader'] = O['MATID_Ind'].str[0:5].replace('(\d)', '', regex=True)
O['breader'] = O['breader'].astype('object')
O['REGION_CODE_CONTINENT'] = O['REGION_CODE_CONTINENT'].astype("object")
O['DESCRIPTION'] = O['DESCRIPTION'].astype("object")
O['Maturity'] = O['Maturity'].astype("float")
O['CPU_ACT'] = O['CPU_ACT'].astype("float")
O = O[O['Maturity'].notna()]
O['PLACD_IND'] = O['PLACD_IND'].astype("object")
# O = O[O['INHVDT'].notnull()]
# cambiar el mat_generatedpara inducción
# print(O.isnull().sum())

# cambio de nombres para concatenar
O = O.rename(columns={"CPU_ACT" : "unidades",
                      "PLACD_IND" : "sector",
                      "INPLTDT" : "FECHA_1", 
                      "INPOLDT" : "FECHA_2", 
                      "INHVDT" : "FECHA_3"})

columna_W = ['MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
             'REGION_CODE_CONTINENT', 'DESCRIPTION',
             'unidades', 'sector', 'Maturity',
             'breader', 'FECHA_1', 'FECHA_2', 'FECHA_3']
O = O[columna_W]
W = O
W = W.sort_values(by="FECHA_1")
W['FECHA_1'] = pd.to_datetime(W['FECHA_1'], format="%d-%m-%Y")
W['FECHA_2'] = pd.to_datetime(W['FECHA_2'] , format="%d-%m-%Y")
W['FECHA_3'] = pd.to_datetime(W['FECHA_3'], format="%d-%m-%Y")
W['Maturity'] = W['Maturity'].astype("int32")
# matriz auxiliar
R = W
# print(W.isnull().sum())

"""
###----JUNTAR LA DATA TOTAL----###
"""

t_1 = R[['MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
         'REGION_CODE_CONTINENT', 'DESCRIPTION',
         'sector', 'Maturity', 'unidades',
         'breader', 'FECHA_1', 'FECHA_2', 'FECHA_3']]
# print(t_1.isnull().sum())
t_1 = t_1[t_1['sector'].notnull()]
# t_1 = t_1[t_1['FECHA_2'].notnull()]
# print(t_1.isnull().sum())
t_1['Maturity'] = t_1['Maturity'].astype("int32")
t_1['semana_A'] = t_1['FECHA_1'].dt.weekofyear
t_1['semana_A'] = t_1['semana_A'].astype("float")

t_1['semana_B'] = t_1['FECHA_2'].dt.weekofyear
t_1['semana_B'] = t_1['semana_B'].astype("float")

t_1['DELTA_1'] =  (t_1['FECHA_3'] - t_1['FECHA_1'])
t_1['DELTA_1'] = abs((t_1['DELTA_1'].apply(lambda x: x.days)))
# t_1 = t_1.dropna()

t_1['semana_C'] = t_1['FECHA_3'].dt.weekofyear
t_1['semana_C'] = t_1['semana_C'].astype("float64")


#### acá tambien cambié la fecha de inicio #####
t_1['mes_año_f1'] = pd.to_datetime(t_1['FECHA_1']).dt.month
t_1['mes_año_f1'] = t_1['mes_año_f1'].astype('float') 
 
# t_1['periodo'] = t_1[t_1['mes_año'] == [12, 1, 2, 3, 4, 5]]
t1 = t_1[(t_1['mes_año_f1'] == 12) | (t_1['mes_año_f1'] <=2)]
t2 = t_1[(t_1['mes_año_f1'] <= 5) & ((t_1['mes_año_f1']  > 2))]
t3 = t_1[(t_1['mes_año_f1'] <= 8) & ((t_1['mes_año_f1']  > 5))]
t4 = t_1[(t_1['mes_año_f1'] <= 11) & ((t_1['mes_año_f1']  > 8))]

t1['periodo_f1'] = 'verano'
t2['periodo_f1'] = 'otoño'
t3['periodo_f1'] = 'invierno'
t4['periodo_f1'] = 'primavera'

e = pd.concat([t1, t2, t3, t4]).drop_duplicates(subset='MAT_GENERATED').reset_index(drop=True)

e['mes_año_f1'] = e['mes_año_f1'].astype('float') 

# trasladar a la cosecha
t_2 = e[e['FECHA_3'].notnull()] # "t_2" para la cosecha !!!

# print(t_2.isnull().sum())

"""
#### construir data a predecir, o proyecttar en los periodos
"""
program_H = e[e['FECHA_3'].isnull()]
program_H = e[['BARCD_IND', 'REGION_CODE_CONTINENT', 'DESCRIPTION',
               'sector', 'Maturity', 'breader', 'FECHA_1',
               'periodo_f1', 'semana_A']]

# print(program_H.isnull().sum())
# program_H = program_H.dropna()

e = e[e['FECHA_3'].notnull()]
# e = e.dropna()
# print(e.isnull().sum())


column_V = ['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'Maturity', 'breader', 
             'periodo_f1', 'semana_A']

X = e[column_V]

# consstruir la vaiable dependiente, explicada
y = e.DELTA_1
y = y.astype('int32')

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


from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Function for comparing different approaches
# Función para comparar diferentes enfoques.
def score_dataset(X_train, X_valid, y_train, y_valid):
    model =  RandomForestRegressor(n_estimators= 71, random_state= 5)
    model.fit(X_train, y_train)
    """ model =   XGBRegressor(n_estimators=66, learning_rate=0.115)
    model.fit(X_train, y_train, 
                 early_stopping_rounds=25, 
                 eval_set=[(X_valid, y_valid)], 
                 verbose=False)"""
    preds = model.predict(X_valid)
    #print(preds)
    return mean_absolute_error(y_valid, preds)


"""
#####################
# INFORMATION CROSS
#####################
"""
import pandas as pd
import numpy as np
import datetime
compare = pd.read_excel('act_tot_23_12_2022.xlsx')

compare = pd.DataFrame(compare)
compare = compare[compare['LOC_NAME'] == 'ARICA']
marchant = ['MAT_GENERATED', 'BARCD_IND', 
            'INPLTDT', 'INPOLDT', 'INHVDT']
compare = compare[marchant]

compare['INPLTDT'] = pd.to_datetime(compare['INPLTDT'], format="%d-%m-%Y")
compare['INPOLDT'] = pd.to_datetime(compare['INPOLDT'], format="%d-%m-%Y")
compare['INHVDT'] = pd.to_datetime(compare['INHVDT'], format="%d-%m-%Y")

compare = compare.rename(columns={"INPLTDT" : "FECHA_1", 
                                  "INPOLDT" : "FECHA_2", 
                                  "INHVDT" : "FECHA_3"})
compare['MAT_GENERATED'] = compare['MAT_GENERATED'].astype('object')
compare['BARCD_IND'] = compare['BARCD_IND'].astype('object')
compare['ETAPA'] = 'bn'
compare['registro_unico'] = compare.BARCD_IND.str.cat(compare.ETAPA, sep='_')
marchant_A = ['BARCD_IND',  'FECHA_3']
compareA = compare[marchant_A]
compareA['BARCD_IND'] = compareA['BARCD_IND'].astype('object')
compareA = compareA[compareA['BARCD_IND'].notna()]



"""
##########################
#  END---INFORMATION CROSS
##########################
"""


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


print("MAE from Approach 1, validación de fecha de cosechas:")  
print(round(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid),4))


"""
##########################################
### empecemos a predecir con la data T,
###--- predecir las polinizaciones ----###
##########################################
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

label_T = program_H[label_X.columns]

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
modelo = RandomForestRegressor(n_estimators= 71, random_state=5)
"""
from xgboost import XGBRegressor
modelo = XGBRegressor(n_estimators=66, learning_rate=0.115)
"""
modelo.fit(OH_X_entren, y)
# predecir
program_H['DELTA_1_est'] =  modelo.predict(OH_X_valido)
program_H['DELTA_1_est'] = round(program_H['DELTA_1_est'] , 0)
program_H['FECHA_3_est'] = pd.to_datetime(program_H['FECHA_1']) + pd.to_timedelta(program_H['DELTA_1_est'].astype(np.int),'D')
# program_H.columns


"""
# CRUZAR CON LA INFORMACIÓN DE COSECHA
"""
program_H['BARCD_IND'] = program_H['BARCD_IND'].astype('object')
program_H =  program_H.merge(compareA, how='left', on='BARCD_IND')
program_H.sort_values(by=['FECHA_1'], inplace=True, ascending=True)


# y.describe()
# y.hist()

# program_H['DELTA_1_est'].hist()



program_H['DELTA_1_est'].describe()

program_H['DELTA_1_est'].hist()


import pandas as pd
import matplotlib.pyplot as plt

boxplot = program_H.boxplot(column=[ 'DELTA_1_est'])
boxplot.plot()
plt.show()

program_H['error_cosecha'] =  program_H['FECHA_3'] - program_H['FECHA_3_est']
program_H['error_cosecha'] = (program_H['error_cosecha'].apply(lambda x: x.days))

import pandas as pd
import matplotlib.pyplot as plt
boxplot = program_H.boxplot(column=['error_cosecha'])
boxplot.plot()
plt.show()

# program_H.columns
# program_H.to_excel('resumen_siembra_cosecha.xlsx', index= False)

program_H['error_cosecha'].describe()
# program_H['error_cosecha'].describe()
program_H['error_cosecha'].hist()



start_date = '2022-11-01'
between = (program_H['FECHA_3'] >= start_date)
program_H = program_H[between]



program_Hight = program_H[(program_H['error_cosecha']>= -3) & (program_H['error_cosecha']<= 3) ]
# program_Hight['error_cosecha'].describe()

# ATÍPICOS
program_Low = program_H[(program_H['error_cosecha']<- 3) | (program_H['error_cosecha']> 3) ]
# program_Low['error_cosecha'].describe()

# 368/381

# 342/4877

# program_H.to_excel('resumen_siembra_cosecha.xlsx', index= False)

# program_Hight.to_excel('resumen_siembra_cosecha_no_atipico.xlsx', index= False)

# program_Low.to_excel('resumen_siembra_cosecha_atipico.xlsx', index= False)
