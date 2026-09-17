# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:45:28 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# Default of credit card clients
# https://www.kaggle.com/datasets/mariosfish/default-of-credit-card-clients?select=default+of+credit+card+clients.csv

con = sqlite3.connect('db_ccc.db')
df1 = pd.read_csv('default_of_credit_card_clients.csv')

df1.to_sql('default_of_credit_card_clients', con, if_exists='replace', index=False)

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
from default_of_credit_card_clients
"""
df_0 = sq(query_0)
# df_0.columns

# df_0.info()



"""
# 1.-
A continuación, te muestro cómo se puede aplicar el modelo logístico a 
la tabla que hemos estado trabajando.

Supongamos que queremos predecir la probabilidad de que un cliente incumpla 
con sus pagos en función del límite de crédito y los pagos mensuales.

Podemos utilizar la siguiente consulta SQL para estimar los coeficientes 
del modelo logístico:
"""

query_1_a = """
select
sum(limit_bal * incumplimiento) / sum(limit_bal * limit_bal) as beta1,
sum(pay_amt1 * incumplimiento) / sum(pay_amt1 * pay_amt1) as beta2,
sum(incumplimiento) / count(*) as beta0
from (select
      limit_bal,
      pay_amt1,
      case
       when pay_amt1 < 1000 then 1
       else 0
      end as incumplimiento
      from default_of_credit_card_clients
      ) as subconsulta;
""" 
df_1_a = sq(query_1_a)
df_1_a


"""
Esta consulta estima los coeficientes del modelo logístico utilizando 
método de los mínimos cuadrados.

Una vez que tenemos los coeficientes estimados, podemos utilizar la 
siguiente consulta SQL para predecir la probabilidad de incumplimiento 
para cada cliente:
"""    


query_1_b = """
with  subconsulta as (
        select
        limit_bal,
        pay_amt1,
        sum(limit_bal * incumplimiento) / sum(limit_bal * limit_bal) as beta1,
        sum(pay_amt1 * incumplimiento) / sum(pay_amt1 * pay_amt1) as beta2,
        sum(incumplimiento) / count(*) as beta0
        from (select
              limit_bal,
              pay_amt1,
              case
               when pay_amt1 < 1000 then 1
               else 0
              end as incumplimiento
              from default_of_credit_card_clients
              ) 
        
      )  
select
limit_bal,
pay_amt1,
1/ (1 + (beta0 + beta1 + beta2)) as pausa
from subconsulta
""" 
df_1_b = sq(query_1_b)
df_1_b




import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Carga los datos
datos = df1

# Define la variable dependiente (Dpnm)
y = datos['dpnm']

# Define las variables independientes (resto de columnas)
X = datos.drop(['ID', 'dpnm'], axis=1)

# Codifica las variables categóricas (Sex, Education, Marriage)
# X['SEX'] = X['SEX'].map({1: 0, 2: 1})
# X['EDUCATION'] = X['EDUCATION'].map({1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5})
# X['MARRIAGE'] = X['MARRIAGE'].map({1: 0, 2: 1, 3: 2})


# Divide los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea un modelo de regresión logística
modelo = LogisticRegression()

# Entrena el modelo con los datos de entrenamiento
modelo.fit(X_train, y_train)

# Predice los resultados para los datos de prueba
y_pred = modelo.predict(X_test)


