# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:45:28 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit_risk_dataset
# https://www.kaggle.com/datasets/laotse/credit-risk-dataset?select=credit_risk_dataset.csv

con = sqlite3.connect('bd_cr.db')
df1 = pd.read_csv('crd.csv')

df1.to_sql('crd', con, if_exists='replace', index=False)

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
from crd
"""
df_0 = sq(query_0)
# df_0.columns

df_0['Cb_person_default_on_file'].unique()


# df_0.info()



"""
# 1.-
Identificar los clientes que tienen un historial de incumplimiento de pagos 
y cuyo ingreso promedio es mayor que el ingreso promedio de todos los 
clientes.
"""

query_1_a = """
with clientes_incumplimientos as(
        select
        person_age,
        person_income,
        Cb_person_default_on_file
        from crd
        where Cb_person_default_on_file = 'Y'
        ),
     ingreso_promedio as(
         select
         avg(person_income) as promedio
         from crd
         )
select
c.person_age,
c.person_income,
c.Cb_person_default_on_file
from clientes_incumplimientos c     
where c.Cb_person_default_on_file > (select promedio from ingreso_promedio)
""" 
df_1_a = sq(query_1_a)
df_1_a



"""
# 2.-
Identificar los clientes que tienen un historial de incumplimiento de 
pagos, cuyo ingreso es mayor que el promedio de todos los clientes, y 
asignarles un número de fila según su edad.
"""

query_2 = """
with clientes_incumplimiento as(
        select
        person_age,
        person_income,
        cb_person_default_on_file,
        row_number() over(order by person_age) as fila
        from crd
        where cb_person_default_on_file = 'Y'
        ),
     ingreso_promedio as(
         select
         avg(person_income) as promedio
         from crd
         )
select
c.person_age,
c.person_income,
c.cb_person_default_on_file,
c. fila,
case
   when c.person_income > (select 
                           promedio 
                           from ingreso_promedio) 
                           then 'mayor que el promedio'
   else 'menor o igual al promedio'
end as  ingreso_comparado
from clientes_incumplimiento c
where c.person_income > (select promedio from ingreso_promedio)
order by c.fila;
""" 
df_2 = sq(query_2)
df_2

