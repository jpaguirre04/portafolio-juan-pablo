# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 10:25:47 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit-card-approval-prediction
# https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction?select=credit_record.csv

con = sqlite3.connect('db_cca.db')

dfi = pd.read_csv('application_record.csv')
dfii = pd.read_csv('credit_record.csv')


dfi.to_sql('application_record', con, if_exists='replace', index=False)
dfii.to_sql('credit_record', con, if_exists='replace', index=False)

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
from application_record
"""
df_0 = sq(query_0)
# df_0.columns

df_0['Name_income_type'].unique()



query_00 = """
select
*
from credit_record
"""
df_00 = sq(query_00)
# df_00.columns

df_00['Status'].unique()





"""
# 1.-
Identificar a los solicitantes de crédito que tienen un historial 
crediticio positivo y un ingreso total anual superior a $50,000.
"""

query_1 = """
      select
      ar.id,
      ar.name_income_type,
      ar.amt_income_total,
      cr.status
      from application_record ar
      inner join credit_record cr 
      on ar.id = cr.id
      where ar.amt_income_total > 50000
            and cr.status = '0'
      group by ar.id, ar.name_income_type,
               ar.amt_income_total, cr.status
""" 
df_1 = sq(query_1)
df_1




"""
# 2.-
Identificar a los solicitantes de crédito que:

- Tienen un historial crediticio positivo (es decir, han realizado pagos a 
  tiempo) durante al menos 6 meses.

- Tienen un ingreso total anual superior a $50,000.
- Tienen un tipo de ingreso que sea "Trabajador por cuenta ajena" o 
  "Emprendedor".
- No tienen ningún registro de crédito con un estado de "Mora" o 
  "Incumplimiento".
"""

query_2 = """
with positivos as(
        select
        id,
        months_balance
        from credit_record
        -- Suponiendo que '0' --indica un historial crediticio positivo
        where status = '0' 
        ),
     cumplidores as(
         select
         id,
         sum(months_balance) as suma
         from positivos
         group by id
         having sum(months_balance) < -10
         )
select
ar.id,
ar.name_income_type,
ar.amt_income_total,
cr.status,
p.months_balance
from application_record ar
inner join cumplidores c on ar.id = c.id
inner join positivos p on ar.id = p.id
left join credit_record cr on  ar.id = cr.id
where ar.amt_income_total > 50000
      and name_income_type in ('Commercial associate',  'State servant')
      and cr.status in ('X', 'C')
group by ar.id, ar.name_income_type, ar.amt_income_total,
         cr.status, p.months_balance
""" 
df_2 = sq(query_2)
df_2



"""
# 3.-
Identificar a los solicitantes de crédito que:

- Tienen un ingreso total anual superior a $70,000.
- Tienen un tipo de ingreso que sea "Emprendedor" o "Trabajador por cuenta propia".
- Han tenido al menos 2 créditos aprobados en los últimos 12 meses.
- No han tenido ningún crédito rechazado en los últimos 6 meses.
"""

query_3 = """
with creditos_aprobados as(
        select
        ar.id,
        count(cr.id) as cantidad_creditos_aprobados,
        max(cr.months_balance) as meses_con_credito_aprobado
        from application_record as ar
        inner join credit_record cr on ar.id = cr.id
        where cr.status in ('0')  -- Suponiendo que '0' indica un crédito aprobado
        group by ar.id
        )
select
ar.id,
ar.name_income_type,
ar.amt_income_total
from application_record ar
inner join creditos_aprobados ca on ar.id = ca.id
where ar.amt_income_total > 70000
and ar.name_income_type in ('Working', 'Commercial associate')
and ca.cantidad_creditos_aprobados >= 2
""" 
df_3 = sq(query_3)
df_3








