# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 09:20:09 2025

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
¿Cuál es el límite de crédito promedio de los clientes que pagan 
puntualmente, agrupado por rango de edad y nivel de educación?
"""

query_1 = """
select
case 
   when age <= 30 then 'menor o igual a 30'
   when age between 31 and 50 then '31-50'
   else 'mayor a 50'
end as rango_edad,
education,
avg(limit_bal) as promedio_limite_credito
from default_of_credit_card_clients
where dpnm = 0
group by 
      case 
         when age <= 30 then 'menor o igual a 30'
         when age between 31 and 50 then '31-50'
         else 'mayor a 50'
      end,
education
order by rango_edad, education;      
""" 
df_1 = sq(query_1)
df_1




"""
# 2.-
¿Cuáles son los clientes que tienen un límite de crédito superior al 
promedio de los clientes de su mismo nivel de educación?
"""

query_2_a = """
select
id,
education,
limit_bal
from default_of_credit_card_clients 
where limit_bal > (select
                       avg(limit_bal)
                       from default_of_credit_card_clients
                       where education = default_of_credit_card_clients.education
                   );
""" 
df_2_a = sq(query_2_a)
df_2_a



"""
Sin embargo, esta consulta no funcionará correctamente porque la subconsulta 
está intentando acceder a la tabla externa (`tu_tabla`) utilizando el alias 
`tu_tabla.Education`, lo cual no es permitido.

Para solucionar este problema, podemos utilizar una subconsulta con una 
tabla derivada:
"""


query_2_b = """
select
id,
education,
limit_bal
from default_of_credit_card_clients 
where limit_bal > (select
                   avg(limit_bal)
                   from (select 
                         education,
                         limit_bal
                         from default_of_credit_card_clients
                         ) as subtabla
                   where subtabla.education = default_of_credit_card_clients.education
                   );
""" 
df_2_b = sq(query_2_b)
df_2_b



"""
Sin embargo, esta consulta todavía no funcionará correctamente porque 
la subconsulta está intentando acceder a la tabla externa (`tu_tabla`) 
utilizando el alias `tu_tabla.Education`, lo cual no es permitido.

Para solucionar este problema, podemos utilizar una subconsulta con una 
tabla derivada y un JOIN:
"""    




query_2_c = """
select
t1.id,
t1.education,
t1.limit_bal
from default_of_credit_card_clients as t1
join (select
      education,
      avg(limit_bal) as promedio_limite
      from default_of_credit_card_clients
      group by education
      ) as t2
on t1.education = t2.education
where t1.limit_bal > t2.promedio_limite
""" 
df_2_c = sq(query_2_c)
df_2_c














