# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 10:25:47 2025

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
¿Cuál es el porcentaje de clientes que incumplieron con el pago en el 
próximo mes, agrupado por rango de edad y sexo?
"""

query_1 = """
select
sex,
case
   when age between 20 and 30 then '20-30'
   when age between 31 and 40 then '31-40'
   when age between 41 and 50 then '41-50'
   else 'mayor a 50'
end as rango_edad,
count(case when dpnm = 1 then 1 end)  as cantidad_incumplidores,
count(*) as cantidad_total,
round(count(case when dpnm = 1 then 1 end) * 100 / count(*), 2) as porcentaje_incumplidores
from default_of_credit_card_clients
group by sex,
         case
            when age between 20 and 30 then '20-30'
            when age between 31 and 40 then '31-40'
            when age between 41 and 50 then '41-50'
            else 'mayor a 50'
         end 
order by sex, rango_edad;         
""" 
df_1 = sq(query_1)
df_1



"""
# 2.-
¿Cuál es el límite de crédito promedio para los clientes que pagan 
puntualmente?
"""

query_2 = """
select
avg(limit_bal) as promedio_limite_credito
from default_of_credit_card_clients
where dpnm = 0
""" 
df_2 = sq(query_2)
df_2




"""
# 3.-
Vamos a explorar la relación entre el límite de crédito y el 
incumplimiento de pagos.

Para analizar esta relación, podemos utilizar una consulta SQL que 
nos permita visualizar cómo se distribuye el incumplimiento de pagos 
según el límite de crédito.
"""

query_3 = """
select
case 
   when limit_bal <= 20000 then '0-20000'
   when limit_bal <= 50000 then '20001-50000'
   when limit_bal <= 10000 then '50001-100000'
   else 'más de 100000'
end as rango_limite_credito,
count(case when dpnm = 1 then 1 end) as cantidad_incumplidores,
count(*) as cantidad_total,
round(count(case when dpnm = 1 then 1 end) *100/count(*), 2) as porcentaje_incumplidores
from default_of_credit_card_clients   
group by 
     case 
        when limit_bal <= 20000 then '0-20000'
        when limit_bal <= 50000 then '20001-50000'
        when limit_bal <= 10000 then '50001-100000'
        else 'más de 100000'
     end
order by  rango_limite_credito
""" 
df_3 = sq(query_3)
df_3




"""
 # 4.-
Vamos a explorar el porcentaje de clientes que pagan puntualmente 
según su nivel de educación.

Para analizar esta relación, podemos utilizar una consulta SQL que nos 
permita visualizar cómo se distribuye el pago puntual según el nivel 
de educación.
"""


"""
Esta consulta nos permitirá ver cómo se distribuye el pago puntual según 
el nivel de educación, y así podemos analizar si hay una relación entre 
estos dos factores.
"""


query_4 = """
select
education,
count(case when dpnm = 0 then 1 end) as cantidad_puntual,
count(*) as cantidad_total,
round(count(case when dpnm = 0 then 1 end) * 100/ count(*),2) as porcentaje_puntual
from default_of_credit_card_clients   
group by education
order by education;
""" 
df_4 = sq(query_4)
df_4


"""
 # 5.-
¿Cuál es el porcentaje de clientes que pagan puntualmente según su 
estado civil?
"""

"""
Esta consulta nos permitirá ver cómo se distribuye el pago puntual según 
el estado civil, y así podemos analizar si hay una relación entre estos 
dos factores.
"""

query_5 = """
select
marriage,
count(case when dpnm = 0 then 1 end) as cantidad_puntual,
count(*) as cantidad_total,
round(count(case when dpnm = 0 then 1 end)* 100 / count(*), 2) as procentaje_puntual
from default_of_credit_card_clients
group by marriage
order by marriage
""" 
df_5 = sq(query_5)
df_5



"""
 # 6.-
¿Cuál es el porcentaje de clientes que pagan puntualmente, agrupado por 
rango de edad y nivel de educación, y que además tienen un límite de 
crédito superior a $50,000?
"""

query_6 = """
select
age,
case 
   when age <= 30 then 'menor o igual a 30'
   when age <= 50 then '31-50'
   else 'mayor a 50'
end as rango_edad,
education,
count(case when dpnm = 0 then 1 end) as cantidad_puntual,
count(*) as cantidad_total,
round(count(case when dpnm = 0 then 1 end) * 100/count(*), 2) as porcentaje_puntual
from default_of_credit_card_clients
where limit_bal > 50000
group by
   case 
      when age <= 30 then 'menor o igual a 30'
      when age <= 50 then '31-50'
      else 'mayor a 50'
   end,
education
order by rango_edad, education
""" 
df_6 = sq(query_6)
df_6



