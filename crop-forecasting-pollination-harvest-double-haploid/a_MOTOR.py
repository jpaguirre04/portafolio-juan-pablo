# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 08:03:56 2021
V
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
# arica = pd.read_excel('act_tot_17_03_2023.xlsx')
# arica = pd.read_excel('act_tot_14_03_2023.xlsx')
# arica = pd.read_excel('act_tot_10_03_2023.xlsx')
# arica = pd.read_excel('act_tot_07_03_2023.xlsx')
# arica = pd.read_excel('act_tot_03_03_2023.xlsx')
# arica = pd.read_excel('act_tot_28_02_2023.xlsx')
# arica = pd.read_excel('act_tot_24_02_2023.xlsx')
# arica = pd.read_excel('act_tot_21_02_2023.xlsx')
# arica = pd.read_excel('act_tot_17_02_2023.xlsx')
arica = pd.read_excel('act_tot_14_02_2023.xlsx')
# arica = pd.read_excel('act_tot_10_02_2023.xlsx')
# arica = pd.read_excel('act_tot_07_02_2023.xlsx')
# arica = pd.read_excel('act_tot_03_02_2023.xlsx')
# arica = pd.read_excel('act_tot_31_01_2023.xlsx')
# arica = pd.read_excel('act_tot_27_01_2023.xlsx')
# arica = pd.read_excel('act_tot_24_01_2023.xlsx')
# arica = pd.read_excel('act_tot_20_01_2023.xlsx')
# arica = pd.read_excel('act_tot_17_01_2023.xlsx')
# arica = pd.read_excel('act_tot_13_01_2023.xlsx')
# arica = pd.read_excel('act_tot_10_01_2023.xlsx')
# arica = pd.read_excel('act_tot_06_01_2023.xlsx')
# arica = pd.read_excel('act_tot_03_01_2023.xlsx')
# arica = pd.read_excel('act_tot_30_12_2022.xlsx')
# arica = pd.read_excel('act_tot_27_12_2022.xlsx')
# arica = pd.read_excel('act_tot_23_12_2022.xlsx')
# arica = pd.read_excel('act_tot_20_12_2022.xlsx')
# arica = pd.read_excel('act_tot_16_12_2022.xlsx')
# arica = pd.read_excel('act_tot_13_12_2022.xlsx')
# arica = pd.read_excel('act_tot_09_12_2022.xlsx')
# arica = pd.read_excel('act_tot_18_11_2022.xlsx')
# arica = pd.read_excel('act_tot_15_11_2022.xlsx')
# arica = pd.read_excel('act_tot_11_11_2022.xlsx')
# arica = pd.read_excel('act_tot_08_11_2022.xlsx')
# arica = pd.read_excel('act_tot_04_11_2022.xlsx')
# arica = pd.read_excel('act_tot_02_11_2022.xlsx')
# arica = pd.read_excel('act_tot_28_10_2022.xlsx')
# arica = pd.read_excel('act_tot_25_10_2022.xlsx')
# arica = pd.read_excel('act_tot_21_10_2022.xlsx')
# arica = pd.read_excel('act_tot_18_10_2022.xlsx')
# arica = pd.read_excel('act_tot_14_10_2022.xlsx')
# arica = pd.read_excel('act_tot_11_10_2022.xlsx')
# arica = pd.read_excel('act_tot_07_10_2022.xlsx')
# arica = pd.read_excel('act_tot_04_10_2022.xlsx')
# arica = pd.read_excel('act_tot_30_09_2022.xlsx')
# arica = pd.read_excel('act_tot_27_09_2022.xlsx')
# arica = pd.read_excel('act_tot_20_09_2022.xlsx')
# arica = pd.read_excel('act_tot_13_09_2022.xlsx')
# arica = pd.read_excel('act_tot_09_09_2022.xlsx')
# arica = pd.read_excel('act_tot_06_09_2022.xlsx')
# arica = pd.read_excel('act_tot_02_09_2022.xlsx')
# arica = pd.read_excel('act_tot_30_08_2022.xlsx')
# arica = pd.read_excel('act_tot_26_08_2022.xlsx')
# arica = pd.read_excel('act_tot_23_08_2022.xlsx')
# arica = pd.read_excel('act_tot_19_08_2022.xlsx')



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
O['codigo'] = O['MATID_Ind'].str[0:5].replace('(\d)', '', regex=True)
O['codigo'] = O['codigo'].astype('object')
O['REGION_CODE_CONTINENT'] = O['REGION_CODE_CONTINENT'].astype("object")
O['DESCRIPTION'] = O['DESCRIPTION'].astype("object")
O['Maturity'] = O['Maturity'].astype("float")
O['CPU_ACT'] = O['CPU_ACT'].astype("float")
O = O[O['Maturity'].notna()]
O['PLACD_IND'] = O['PLACD_IND'].astype("object")

O['PLACD_IND'].unique()

# sectores = O[(O['PLACD_IND'] == 64.0) | (O['PLACD_IND'] == 28.0)]

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
             'codigo', 'FECHA_1', 'FECHA_2', 'FECHA_3']
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
         'codigo', 'FECHA_1', 'FECHA_2', 'FECHA_3']]
# print(t_1.isnull().sum())
t_1 = t_1[t_1['sector'].notnull()]
# t_1 = t_1[t_1['FECHA_2'].notnull()]
# print(t_1.isnull().sum())
t_1['Maturity'] = t_1['Maturity'].astype("int32")
t_1['semana_A'] = t_1['FECHA_1'].dt.weekofyear
t_1['semana_A'] = t_1['semana_A'].astype("float")

t_1['semana_B'] = t_1['FECHA_2'].dt.weekofyear
t_1['semana_B'] = t_1['semana_B'].astype("float")

t_1['DELTA_1'] =  (t_1['FECHA_2'] - t_1['FECHA_1'])
t_1['DELTA_1'] = abs((t_1['DELTA_1'].apply(lambda x: x.days)))
t_1['DELTA_1'] = t_1['DELTA_1'].astype('float64')
# t_1 = t_1.dropna()

t_1['semana_C'] = t_1['FECHA_3'].dt.weekofyear
t_1['semana_C'] = t_1['semana_C'].astype("float")

# acá cambie la fecha de inicio
t_1['DELTA_2'] =  (t_1['FECHA_3'] - t_1['FECHA_2'])
t_1['DELTA_2'] = abs((t_1['DELTA_2'].apply(lambda x: x.days)))
t_1['DELTA_2'] = t_1['DELTA_2'].astype('float64')

# t_1['DELTA_2'].describe()
# t_1['DELTA_2'].hist()


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

e = pd.concat([t1, t2, t3, t4]).drop_duplicates(subset='BARCD_IND').reset_index(drop=True)

e['mes_año_f1'] = e['mes_año_f1'].astype('float') 


# trasladar a la cosecha
t_2 = e[e['FECHA_3'].notnull()] # "t_2" para la cosecha !!! hacer el mismo
# analisis de la cosecha dispaarada!!!

#### construir data a predecir, o proyecttar en los periodos
program_H = e[['MATID_Ind', 'MAT_GENERATED', 'BARCD_IND',
               'REGION_CODE_CONTINENT',  'DESCRIPTION',
               'unidades', 'sector', 'Maturity',
               'codigo', 'FECHA_1', 'periodo_f1',  
               'mes_año_f1', 'FECHA_2', ]]
program_H = program_H[program_H['FECHA_1'].notnull()]
program_H['semana_A'] = program_H['FECHA_1'].dt.weekofyear
program_H = program_H[program_H['FECHA_2'].isnull()]
# program_H = program_H.drop(columns = ['FECHA_2'])
del program_H['FECHA_2']


program_H['Maturity'] = program_H['Maturity'].astype("float")

start_date = '2022-01-01'
between = (program_H['FECHA_1'] >= start_date)
program_H = program_H[between]
# inducción y luego baby nursery

# p = p.dropna()

# print(p.isnull().sum())

e = e[e['FECHA_2'].notnull()]

# e = e.dropna()
# print(e.isnull().sum())

column_V = ['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'Maturity', 'codigo', 'semana_A',
            'periodo_f1', 'mes_año_f1', 'periodo_f1']

"""
column_V = ['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'Maturity', 'codigo', 'semana_A',
            'periodo_f1', 'mes_año_f1', 'periodo_f1']
"""


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
    model =  RandomForestRegressor(n_estimators = 68, random_state=4)
    model.fit(X_train.values, y_train.values)
    """model =   XGBRegressor(n_estimators=66, learning_rate=0.115)
    model.fit(X_train, y_train, 
                 early_stopping_rounds=25, 
                 eval_set=[(X_valid, y_valid)], 
                 verbose=False)"""
    preds = model.predict(X_valid.values)
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
compare = pd.read_excel('act_tot_17_03_2023.xlsx')

compare = pd.DataFrame(compare)
compare = compare[compare['LOC_NAME'] == 'ARICA']
xy = compare
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
marchant_A = ['BARCD_IND',  'FECHA_2']
compareA = compare[marchant_A]
compareA['BARCD_IND'] = compareA['BARCD_IND'].astype('object')
compareA = compareA[compareA['BARCD_IND'].notna()]
start_date = '2022-01-01'
between = (compareA['FECHA_2'] >= start_date)
compareA = compareA[between]


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


print("MAE from Approach 1, validación de fecha de polinizaciones:")  
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

modelo = RandomForestRegressor(n_estimators= 68 , random_state=4)
"""
from xgboost import XGBRegressor
modelo = XGBRegressor(n_estimators=66, learning_rate=0.115)
"""
modelo.fit(OH_X_entren.values, y.values)
# predecir
program_H['days_poli_est'] =  modelo.predict(OH_X_valido.values)
program_H['days_poli_est'] = round(program_H['days_poli_est'] , 0)
program_H['FECHA_2_est'] = pd.to_datetime(program_H['FECHA_1']) + pd.to_timedelta(program_H['days_poli_est'].astype(np.int),'D')
# program_H.columns

"""
# CRUZAR CON LA INFORMACIÓN DE POLI
"""
program_H['BARCD_IND'] = program_H['BARCD_IND'].astype('object')
program_H =  program_H.merge(compareA, how='left', on='BARCD_IND')
program_H.sort_values(by=['FECHA_1'], inplace=True, ascending=True)


"""
# conisderar la POLI real y después la estimada !!!
# construir la poli que se usará para la cosecha !!!
"""


O_real = program_H[program_H['FECHA_2'].notnull()]
O_real['FECHA_POLI'] = O_real['FECHA_2'] 
# O_real = O_real.rename(columns= {'PSS_GPOLDT_REAL': 'FECHA_POLI'})
O_real['tipo_poli'] = 'poli_real'
# del O_real['GPOLDT_est']


O_est = program_H[program_H['FECHA_2'].isnull()]
O_est['FECHA_POLI'] = O_est['FECHA_2_est'] 
# O_est = O_est.rename(columns= {'GPOLDT_est': 'FECHA_POLI'})
O_est['tipo_poli'] = 'poli_estimada'
# del O_est['PSS_GPOLDT_REAL']

"""
O_total = pd.concat([O_est, 
               O_real]).drop_duplicates(subset='registro_unico').reset_index(drop=False)
"""
program_H_total = pd.concat([O_est, O_real])
# O_total = pd.concat([O_real, O_est])
# O_total.columns

program_H_total['semana_B_est'] = program_H_total['FECHA_2_est'].dt.weekofyear
program_H_total['semana_B_real'] = program_H_total['FECHA_2'].dt.weekofyear
program_H_total['semana_B'] = program_H_total['FECHA_POLI'].dt.weekofyear
program_H_total.sort_values(by=['FECHA_POLI'], inplace=True, ascending=True)

# ahora definir el periodo de temnpodara en la data
# a proyectar

t_o = program_H_total[program_H_total['FECHA_POLI'].notnull()]
t_o['mes_año_f2'] = pd.to_datetime(t_o['FECHA_POLI']).dt.month
t_o['mes_año_f2'] = t_o['mes_año_f2'].astype('float') 
 
# t_o['periodo'] = t_o[t_o['mes_año'] == [12, 1, 2, 3, 4, 5]]
ti = t_o[(t_o['mes_año_f2'] == 12) | (t_o['mes_año_f2'] <= 2)]
tii = t_o[(t_o['mes_año_f2'] <= 5) & ((t_o['mes_año_f2']  > 2))]
tiii = t_o[(t_o['mes_año_f2'] <= 8) & ((t_o['mes_año_f2']  > 5))]
tiv = t_o[(t_o['mes_año_f2'] <= 11) & ((t_o['mes_año_f2']  > 8))]

ti['periodo_f2'] = 'verano'
tii['periodo_f2'] = 'otoño'
tiii['periodo_f2'] = 'invierno'
tiv['periodo_f2'] = 'primavera'

program_K_total = pd.concat([ti, tii, tiii, tiv]).drop_duplicates(subset='BARCD_IND').reset_index(drop=True)


"""
#######################################
###--- COSECHA EN INDUCCIÓN---####
#######################################
"""
# la fecha de inicio es la poli

# t_2.columns
# t_2['DELTA_2'].describe()
# t_2['DELTA_2'].hist()


#### acá tambien cambié la fecha de inicio #####
t_2 = t_2[(t_2['FECHA_3'].notnull())]
t_2['mes_año_f2'] = pd.to_datetime(t_2['FECHA_2']).dt.month
t_2['mes_año_f2'] = t_2['mes_año_f2'].astype('float') 
 
# t_2['periodo'] = t_2[t_2['mes_año'] == [12, 1, 2, 3, 4, 5]]
t1 = t_2[(t_2['mes_año_f2'] == 12) | (t_2['mes_año_f2'] <=2)]
t2 = t_2[(t_2['mes_año_f2'] <= 5) & ((t_2['mes_año_f2']  > 2))]
t3 = t_2[(t_2['mes_año_f2'] <= 8) & ((t_2['mes_año_f2']  > 5))]
t4 = t_2[(t_2['mes_año_f2'] <= 11) & ((t_2['mes_año_f2']  > 8))]

t1['periodo_f2'] = 'verano'
t2['periodo_f2'] = 'otoño'
t3['periodo_f2'] = 'invierno'
t4['periodo_f2'] = 'primavera'

p = pd.concat([t1, t2, t3, t4]).drop_duplicates(subset='BARCD_IND').reset_index(drop=True)

column_VI = ['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'Maturity', 'codigo',  
            'semana_A',  'semana_B']

"""
column_VI = ['REGION_CODE_CONTINENT', 'DESCRIPTION',
            'sector', 'Maturity', 'codigo',  
            'semana_A',  'semana_B', 
            'periodo_f1', 'mes_año_f1']

"""

X1 = p[column_VI]
# consstruir la vaiable dependiente, explicada
y1 = p.DELTA_2
y1 = y1.astype('int32')

# y1.hist()
# y1.describe()


"""
#####--- VALIDACION II---#####
# hasta acá, pero lo de abajo es para validar un modelo
# de predicción
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
s = (X1_train.dtypes == 'object')
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

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH1_cols_train = pd.DataFrame(OH_encoder.fit_transform(X1_train[object_cols]))
OH1_cols_valid = pd.DataFrame(OH_encoder.transform(X1_valid[object_cols]))

# One-hot encoding removed index; put it back
OH1_cols_train.index = X1_train.index
OH1_cols_valid.index = X1_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X1_train = X1_train.drop(object_cols, axis=1)
num_X1_valid = X1_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X1_train = pd.concat([num_X1_train, OH1_cols_train], axis=1)
OH_X1_valid = pd.concat([num_X1_valid, OH1_cols_valid], axis=1)

print("MAE from Approach 1, validación de fecha de polinizaciones:")  
print(round(score_dataset(OH_X1_train, OH_X1_valid, y1_train, y1_valid),4))

"""
####----PREDECIR LAS COSECHAS-----######
"""

from sklearn.preprocessing import LabelEncoder
import numpy as np

# Obtener la lista de variables categóricas.
t = (X1.dtypes == 'object')
objecto_columna = list(t[t].index)

print("Variables Categóricas:")
print(objecto_columna)

# Make copy to avoid changing original data 
# Haga una copia para evitar cambiar los datos originales
label_X1 = X1.copy()

label_T1 = program_K_total[label_X1.columns]

# Apply one-hot encoder to each column with categorical data
OHot_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_X1 = pd.DataFrame(OHot_encoder.fit_transform(X1[objecto_columna]))
OH_label_T1 = pd.DataFrame(OHot_encoder.transform(label_T1[objecto_columna]))

# One-hot encoding removed index; put it back
OH_cols_X1.index = X1.index
OH_label_T1.index = label_T1.index


# Remove categorical columns (will replace with one-hot encoding)
num_X1 = X1.drop(objecto_columna, axis=1)
num_label_T1 = label_T1.drop(objecto_columna, axis=1)


# Add one-hot encoded columns to numerical features
OHot_X1_entren = pd.concat([num_X1, OH_cols_X1], axis=1)
OHot_X1_valido = pd.concat([num_label_T1, OH_label_T1], axis=1)

from sklearn.ensemble import RandomForestRegressor

modelo = RandomForestRegressor(n_estimators= 68, random_state=4)
modelo.fit(OHot_X1_entren.values, y1.values)
# predecir
program_K_total['days_cosecha_est'] =  modelo.predict(OHot_X1_valido.values)
program_K_total['days_cosecha_est'] = round(program_K_total['days_cosecha_est'] , 0)
program_K_total['FECHA_3_est'] = pd.to_datetime(program_K_total['FECHA_POLI']) + pd.to_timedelta(program_K_total['days_cosecha_est'].astype(np.int),'D')
program_K_total['semana_C_est'] = program_K_total['FECHA_3_est'].dt.weekofyear
# program_K_total.columns


"""
###---INFORTMATION CROSS----###
"""

marchant_B = ['BARCD_IND',  'FECHA_3']
compareB = compare[marchant_B]
compareB['BARCD_IND'] = compareB['BARCD_IND'].astype('object')
# compareB = compareB[compareB['BARCD_IND'].notna()]
start_date = '2022-01-01'
entre = (compareB['FECHA_3'] >= start_date)
compareB = compareB[entre]



"""
# CRUZAR CON LA INFORMACIÓN DE COSECHA
"""
program_K_total['BARCD_IND'] = program_K_total['BARCD_IND'].astype('object')
program_K_total =  program_K_total.merge(compareB, how='left', on='BARCD_IND')
program_K_total.sort_values(by=['FECHA_1'], inplace=True, ascending=True)

# program_K_total.columns
program_K_total = program_K_total[['MATID_Ind', 'MAT_GENERATED', 
                                   'BARCD_IND', 'REGION_CODE_CONTINENT',
       'DESCRIPTION', 'unidades', 'sector', 'Maturity', 'codigo', 'FECHA_1',
       'periodo_f1', 'mes_año_f1',  'days_poli_est', 'FECHA_2_est',
       'FECHA_2', 'FECHA_POLI', 'tipo_poli', 'semana_B',  'periodo_f2', 'semana_B_est',
       'mes_año_f2', 'days_cosecha_est', 'FECHA_3_est', 'FECHA_3']]

program_K_total['SEMANA_SIEMBRA_REAL'] = program_K_total['FECHA_1'].dt.weekofyear
program_K_total['SEMANA_FLORACION_ESTIMADA'] = program_K_total['FECHA_2_est'].dt.weekofyear
program_K_total['SEMANA_FLORACION_REAL'] = program_K_total['FECHA_2'].dt.weekofyear
program_K_total['SEMANA_COSECHA_ESTIMADA'] = program_K_total['FECHA_3_est'].dt.weekofyear
program_K_total['SEMANA_COSECHA_REAL'] = program_K_total['FECHA_3'].dt.weekofyear

# program_K_total.columns

program_K_total['error_poli'] =  program_K_total['FECHA_2'] - program_K_total['FECHA_2_est']
program_K_total['error_poli'] = (program_K_total['error_poli'].apply(lambda x: x.days))

program_K_total['error_cosecha'] =  program_K_total['FECHA_3'] - program_K_total['FECHA_3_est']
program_K_total['error_cosecha'] = (program_K_total['error_cosecha'].apply(lambda x: x.days))


k5 = program_K_total[program_K_total['BARCD_IND']== 'UR293039219']
# program_K_total.columns
# program_K_total.to_excel('Silicon_Valley_17_03_2023.xlsx', index= False)
# program_K_total = program_K_total.dropna()
import matplotlib.pyplot as plt
# multiple line plots
plt.plot('BARCD_IND' , 'SEMANA_SIEMBRA_REAL', data = program_K_total, marker='o', markerfacecolor='brown', markersize=5, color='lightgreen', linewidth=4, label= "siembra")
plt.plot('BARCD_IND' , 'SEMANA_FLORACION_ESTIMADA', data = program_K_total, marker='o', markerfacecolor='blue', markersize=5, color='orange', linewidth=4, label= "floración_estimada")
plt.plot('BARCD_IND' , 'SEMANA_FLORACION_REAL', data = program_K_total, marker='o', markerfacecolor='blue', markersize=5, color='yellow', linewidth=4, label= "floración_real")
plt.plot('BARCD_IND' , 'SEMANA_COSECHA_ESTIMADA', data = program_K_total, marker='o', markerfacecolor='yellow', markersize=5, color='blue', linewidth=4, label= "cosecha_estimada")
plt.plot('BARCD_IND' , 'SEMANA_COSECHA_REAL', data = program_K_total, marker='o', markerfacecolor='lightgreen', markersize=5, color='tomato', linewidth=4, label= "cosecha_real")
plt.title('La_Roca_Inducción: FLORACIÓN y COSECHA')
# show legend
plt.legend()
# show graph 
plt.show()


# program_K_total.columns
