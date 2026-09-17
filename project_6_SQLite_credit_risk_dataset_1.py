# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 17:41:48 2025

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
¿Cuál es el impacto de la edad, el ingreso y el historial de crédito en el 
riesgo de crédito para diferentes categorías de préstamos? ¿Cómo cambia este 
impacto según la propiedad de vivienda y el estado de empleo?
"""

query_1 = """
with datos_preparados as(
        select
        person_age,
        person_income,
        cb_person_cred_hist_length,
        person_home_ownership,
        loan_grade,
        loan_status
        from risk
        ),
    analisis_risk as(
        select
        loan_grade,
        person_home_ownership,
        avg(person_age) as promedio_edad,
        avg(person_income) as promedio_ingreso,
        avg(cb_person_cred_hist_length) as promedio_cred_hist,
        sum(case when loan_status = 1 then 1 else 0 end) as num_default
        from datos_preparados
        group by loan_grade, person_home_ownership
        )
select
loan_grade,
person_home_ownership,
promedio_edad,
promedio_ingreso,
promedio_cred_hist,
num_default,
round(num_default * 100 / count(*), 2) as porcentaje_default
from analisis_risk
group by loan_grade, person_home_ownership
order by loan_grade, person_home_ownership;
"""
df_1 = sq(query_1)
df_1






"""
# 2.-
¿Cuál es el impacto de la propiedad de vivienda en el riesgo de crédito 
para las personas que tienen un historial de crédito prolongado y un 
ingreso superior al promedio? ¿Cómo cambia este impacto según la edad 
y la categoría de préstamo?
"""

query_2 = """
with datos_preparados as (
        select
        person_age,
        person_income,
        person_home_ownership,
        loan_grade,
        loan_status,
        cb_person_cred_hist_length
        from risk
        ),
filtro_subquery as(
       select
       person_age,
       person_income
       from risk
       where cb_person_cred_hist_length > (select avg(cb_person_cred_hist_length) from risk)
       and person_income > (select avg(person_income) from risk)
      )
select
dp.person_home_ownership,
dp.loan_grade,
dp.person_age,
dp.person_income,
sum(case when dp.loan_status = 1 then 1 else 0 end) as num_default
from datos_preparados as dp
join filtro_subquery as fs on dp.loan_status = fs.person_age 
                          and dp.person_income = fs.person_income
group by dp.person_home_ownership, dp.loan_grade,  dp.person_age, dp.person_income                        
order by dp.person_home_ownership, dp.loan_grade,  dp.person_age, dp.person_income
"""
df_2 = sq(query_2)
df_2



