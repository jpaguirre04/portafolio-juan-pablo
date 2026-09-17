# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 11:26:01 2025

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
Analizar la relación entre el tipo de empleo y el riesgo crediticio, 
considerando la edad y el ingreso de los clientes.
"""

query_1 = """
with clientes_con_incumplimiento as(
        select
        c.loan_intent,
        c.person_age,
        c.person_income,
        case
           when cb_person_default_on_file = 'Y' then 1
           else 0
        end as incumplimiento
        from crd c
        inner join ( 
                     select
                     loan_intent,
                     avg(person_income) as ingreso_promedio
                     from crd
                     group by loan_intent
                  ) i on c.loan_intent = i.loan_intent
        )
select
loan_intent,
count(*) as cantidad_clientes,
sum(incumplimiento) as cantidad_clientes_con_incumplimiento, 
avg(person_income) as ingreso_promedio,
avg(person_age) as edad_promedio
from clientes_con_incumplimiento
group by loan_intent
order by cantidad_clientes_con_incumplimiento desc;
""" 
df_1 = sq(query_1)
df_1



