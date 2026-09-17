# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 14:41:58 2025

@author: Juan Pablo Aguirre
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# https://www.kaggle.com/datasets/davidcochran/formula-1-race-data-sqlite

conn = sqlite3.connect('Formula1.sqlite')
c = conn.cursor()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(table)


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

query_0 = """
select
*
from results
"""
df_0 = sq(query_0)
# df_0.columns



"""
# 1.-
Desarrolla un modelo de clasificación que prediga si un piloto de F1 ganará 
una carrera en función de sus características y las condiciones de la carrera.
"""

query_1 = """
select
r.driverId,
r.constructorId,
rc.circuitId,
r.position,
r.points,
r.laps,
r.time,
case
   when r.position = 1 then  1
   else 0
end as winner   
from results r
inner join races rc on r.raceId = rc.raceId
where
r.position is not null
and r.position is not null
and r.laps is not null
and r.time is not null;
"""
df_1 = sq(query_1)
df_1.columns

df_1.dtypes

df_1['Winner'] = df_1['Winner'].astype('float64')



df_1 = df_1[['Driverid', 'Constructorid', 'Circuitid',  'Points', 'Laps',
             'Winner']]

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Cargar datos preprocesados
df = df_1

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(df.drop('Winner', axis=1), df['Winner'], test_size=0.2, random_state=42)

# Entrenar modelo de clasificación
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar modelo de clasificación
y_pred = modelo.predict(X_test)
print('Precisión:', accuracy_score(y_test, y_pred))
print('Informe de clasificación:')
print(classification_report(y_test, y_pred))
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred))
