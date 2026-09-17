# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 19:26:36 2025

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
Identificar los clientes que tienen un historial de incumplimiento de 
pagos y que han solicitado préstamos de más de $10,000. Asignarles una 
categoría según su ingreso en relación con el promedio de ingresos de 
todos los clientes que han solicitado préstamos de más de $10,000. 
Además, asignar un ranking a cada cliente según su ingreso en 
orden descendente.
"""

query_1 = """
with clientes_incumplimientos as(
        select
        person_age,
        person_income,
        cb_person_default_on_file,
        loan_amnt
        from crd
        where cb_person_default_on_file = 'Y' and loan_amnt > 10000
        ) 
select
c.person_age,
c.person_income,
c.cb_person_default_on_file,
c.loan_amnt,
case 
  when person_income > (select avg(person_income) from crd) then 'ingreso_alto'
  when person_income > (select avg(person_income) from crd) then 'ingreso_bajo'
  else ' ingreso_promedio'
end as categoria_ingreso,  
rank() over(order by c.person_income desc) as ranking_ingreso
from clientes_incumplimientos c
order by c.person_age
""" 
df_1 = sq(query_1)
df_1




"""
# 2.-
Ahora que hemos analizado la distribución de los clientes y hemos 
identificado los clientes con un historial de incumplimiento de pagos, 
vamos a segmentar a los clientes según sus características demográficas 
y de comportamiento.

*Pregunta:* ¿Cuáles son los segmentos de clientes que tienen un mayor
 riesgo crediticio y qué características los definen?

Para responder a esta pregunta, podemos utilizar técnicas de segmentación, 
como clustering o regresión logística, para identificar grupos de 
clientes con características similares.

"""

query_2 = """
with clientes_segmentados as(
        select
        person_age,
        person_income,
        cb_person_default_on_file,
        loan_amnt,
        case
        when person_age < 30 and person_income < 50000 then 'jovenes con ingresos bajos'
        when person_age >= 30 and person_age < 50 and person_income >= 50000  and person_income < 100000 then  'jovenes con ingresos bajos'
        when person_age >= 50 and person_income >= 100000 then 'jovenes con ingresos bajos'
        else 'otros'
        end  as segmento
        from crd
        )
select
segmento,
count(*) as cantidad_clientes,
sum(case when cb_person_default_on_file = 'Y' then 1 else 0 end) as cantidad_clientes_con_incumplimiento
from clientes_segmentados
group by segmento
order by cantidad_clientes desc
""" 
df_2 = sq(query_2)
df_2

