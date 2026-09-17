# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 11:01:14 2025

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
¿Cuál es el porcentaje de clientes que tienen un límite de crédito superior 
a $50,000 y que también tienen un pago mensual promedio superior a $2,000?
"""

query_1_a = """
select
  round(
        count(case
                 when limit_bal < 2000 and promedio_pagos < 1000 then 1
              end) *100 / count(*),
        2) as porcentaje_clientes
from (
      select
      limit_bal,
      avg(Pay_amt1 + Pay_amt2 + Pay_amt3 + Pay_amt4 + Pay_amt5 + Pay_amt6) as promedio_pagos
      from default_of_credit_card_clients
      group by limit_bal) as subconsulta;
""" 
df_1_a = sq(query_1_a)
df_1_a


# Otra forma de hacerlo es utilizando una columna calculada:

query_1_b = """
select
  round(
     count(case
        when limit_bal < 20000 and (Pay_amt1 + Pay_amt2 + Pay_amt3 + Pay_amt4 + Pay_amt5 + Pay_amt6)/6 <1000 then 1
     end) * 100 /count(*), 2) as porcentaje_clientes
from default_of_credit_card_clients 
""" 
df_1_b = sq(query_1_b)
df_1_b




"""
# 2.-
¿Cuál es el número total de clientes que tienen un límite de crédito 
superior a $50,000 y que también tienen al menos un pago mensual 
superior a $5,000?
"""

query_2_a = """
select
count(*)
from default_of_credit_card_clients
where
  limit_bal > 50000 and 
  (Pay_amt1 > 5000 OR
   Pay_amt2 > 5000 OR
   Pay_amt3 > 5000 OR
   Pay_amt4 > 5000 OR
   Pay_amt5 > 5000 OR
   Pay_amt6 > 5000
   );
""" 
df_2_a = sq(query_2_a)
df_2_a

