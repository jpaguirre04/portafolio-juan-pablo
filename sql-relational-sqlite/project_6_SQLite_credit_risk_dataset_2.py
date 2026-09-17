# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 11:05:28 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# https://www.kaggle.com/datasets/laotse/credit-risk-dataset?select=credit_risk_dataset.csv

con = sqlite3.connect('db_risk.db')

df = pd.read_csv('risk.csv')

df.to_sql('risk', con, if_exists='replace', index=False)

con.commit()
# con.close()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", con)
# print(table)


def sq(q):
    return pd.read_sql_query(q, con).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

query_0 = """
select
*
from risk
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
¿Cuál es el impacto del historial de crédito en el riesgo de crédito para 
diferentes categorías de préstamos y niveles de ingreso? ¿Cómo cambia este 
impacto según la edad y la propiedad de vivienda?
"""

query_1 = """
with datos_preparados as(
        select
        person_age,
        person_income,
        person_home_ownership,
        loan_grade,
        loan_status,
        cb_person_cred_hist_length,
        cb_person_default_on_file
        from risk
        ),
    historial_credito as(
        select
        cb_person_cred_hist_length,
        count(*) as num_personas,
        sum(case when loan_status = 1 then 1 else 0 end) as num_default
        from datos_preparados
        group by cb_person_cred_hist_length
        )
select
hc.cb_person_cred_hist_length,
hc.num_personas,
hc.num_default,
round(hc.num_default * 100 / hc.num_personas, 2) as porcentaje_default,
dp.person_age,
dp.person_income,
dp.person_home_ownership,
dp.person_home_ownership,
dp.loan_grade
from historial_credito hc 
join datos_preparados dp on hc.cb_person_cred_hist_length = dp.cb_person_cred_hist_length
order by hc.cb_person_cred_hist_length, dp.person_age, 
         dp.person_income, dp.person_home_ownership, dp.loan_grade
"""
df_1 = sq(query_1)
df_1



"""
######--- SQLITE and PYTHON ---######
"""


"""
# 2.-
¿Cuál es el impacto de la edad, el ingreso y el historial de crédito 
en el riesgo de crédito para diferentes categorías de préstamos? 
¿Podemos predecir el riesgo de crédito de una persona en función 
de sus características utilizando un modelo de regresión logística?
"""

query_2 = """
with datos_preparados as (
        select
        person_age,
        person_income,
        cb_person_cred_hist_length,
        loan_grade,
        loan_status
        from risk
        )
select
person_age,
person_income,
cb_person_cred_hist_length,
loan_grade,
case when loan_status = 1 then 1 else 0 end as riesgo
from datos_preparados
"""
df_2 = sq(query_2)
df_2

df_2['Loan_grade'].unique()


import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Cargar los datos
df = df_2
df.columns

# Preparar los datos para la predicción
X = df[['Person_age', 'Person_income', 'Cb_person_cred_hist_length', 'Loan_grade']]
y = df['Riesgo']


# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo de regresión logística
modelo = LogisticRegression()
modelo.fit(X_train, y_train)

# Predecir el riesgo de crédito para los datos de prueba
y_pred = modelo.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo:", accuracy)
print("Informe de clasificación:")
print(classification_report(y_test, y_pred))



