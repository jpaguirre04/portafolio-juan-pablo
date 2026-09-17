# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 16:07:42 2025

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
y que han solicitado préstamos de más de $10,000. Además, queremos conocer 
el porcentaje de clientes que han incumplido con sus pagos en relación con 
el total de clientes que han solicitado préstamos de más de $10,000.
"""

query_1_a = """
with clientes_incumplimientos as(
        select
        person_age,
        person_income,
        cb_person_default_on_file,
        loan_amnt
        from crd
        where cb_person_default_on_file = 'Y' and loan_amnt > 10000
        ),
    total_clientes as(
        select
        count(*) as total
        from crd
        where loan_amnt > 10000
        ) 
select
c.person_age,
c.person_income,
c.cb_person_default_on_file,
c.loan_amnt,
(select total from total_clientes) as total_clintes,
count(*) * 100 / (select total from total_clientes) as porcentaje_incumplimiento
from clientes_incumplimientos c
group by c.person_age, c.person_income, c.cb_person_default_on_file,
         c.loan_amnt
order by c.person_age
""" 
df_1_a = sq(query_1_a)
df_1_a



"""
# 2.-
Identificar los clientes que tienen un historial de incumplimiento de 
pagos y asignarles una categoría según su ingreso en relación con el 
promedio de ingresos de todos los clientes.
"""

query_2 = """
select
person_age,
person_income,
cb_person_default_on_file,
case 
  when person_income > (select avg(person_income) from crd) then 'ingreso_alto'
  when person_income < (select avg(person_income) from crd) then 'ingreso_bajo'
  else ' ingreso_promedio'
end as categoria_ingreso  
from crd
where cb_person_default_on_file = 'Y';
""" 
df_2 = sq(query_2)
df_2




"""
# 3.-
Identificar los clientes que tienen un historial de incumplimiento de pagos 
y asignarles una categoría según su ingreso en relación con el promedio de 
ingresos de todos los clientes que han solicitado préstamos de más de 
$10,000.
"""

query_3 = """
select
person_age,
person_income,
cb_person_default_on_file,
case
  when person_income > ( select avg(person_income) from crd where loan_amnt > 10000) then 'ingreso_alto'
  when person_income < ( select avg(person_income) from crd where loan_amnt > 10000) then 'ingreso_bajo'
  else 'ingreso promedio'
end as categoria_ingreso
from crd
where cb_person_default_on_file = 'Y' and loan_amnt > 10000;
""" 
df_3 = sq(query_3)
df_3


