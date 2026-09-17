# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 19:25:16 2025

@author: Juan Pablo Aguirre
"""


import sqlite3
import pandas as pd


# https://www.kaggle.com/datasets/raniajaberi/car-insurance


con = sqlite3.connect('db_insurance_car.db')
df1 = pd.read_csv('ci.csv')

df1.to_sql('ci', con, if_exists='replace', index=False)

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
from ci
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
¿Cuál es el promedio de millas anuales recorridas por los conductores que 
tienen más de 2 infracciones de velocidad?
"""

query_1 = """
select
avg(annual_mileage) as media_millas_anuales
from ci
where speeding_violations > 2
""" 
df_1 = sq(query_1)
df_1


"""
# 2.-
¿Cuál es el número total de conductores que tienen un crédito score 
superior a 700 y han tenido al menos un accidente en el pasado?
"""

query_2 = """
select
count(*) as total_conductores
from ci
where credit_score > 700 and past_accidents >= 1
""" 
df_2 = sq(query_2)
df_2


"""
# 3.-
Cuál es el promedio de edad de los conductores que tienen un vehículo 
de tipo "Sedan" y han tenido más de 1 DUI (conducción bajo la influencia 
de sustancias)?
"""

query_3 = """
select
avg(age) as edad_media
from ci
where vehicle_type = 'Sedan' and duis > 1
""" 
df_3 = sq(query_3)
df_3


"""
# 4.-
¿Cuál es el número total de conductores casados que tienen hijos y 
han tenido al menos 1 infracción de velocidad?
"""

query_4 = """
select
count(*) as numero_total_conductores
from ci
where married = 1 and children = 1 and speeding_violations >= 1
""" 
df_4 = sq(query_4)
df_4


"""
# 5.-
¿Cuáles son los 5 niveles de educación más comunes entre los conductores 
que han tenido al menos 2 accidentes en el pasado y tienen un crédito 
score inferior a 600? ¿Puedes mostrar el nivel de educación y el 
número de conductores que cumplen con estas condiciones?
"""

query_5 = """
select
education,
count(*) as total_conductores_por_education
from ci
where past_accidents >= 2 and   credit_score < 600
group by education
order by count(*) desc
limit 5;
""" 
df_5 = sq(query_5)
df_5



"""
# 6.-
¿Cuáles son los tipos de vehículos más comunes entre los conductores 
que tienen un crédito score superior a 700 y han tenido menos de 2 
infracciones de velocidad en el último año? ¿Puedes mostrar el tipo 
de vehículo y el número de conductores que cumplen con estas 
condiciones?
"""

query_6 = """
select
vehicle_type,
count(*) as numero_conductores
from ci
where credit_score > 700 and speeding_violations < 2
group by vehicle_type
order by count(*) desc
limit 5;
""" 
df_6 = sq(query_6)
df_6



"""
# 7.-
¿Cuáles son los conductores que tienen un crédito score superior a 700 
y han tenido más de 1 accidente en el pasado, pero no han tenido ninguna 
infracción de velocidad? ¿Puedes mostrar el ID del conductor, el crédito 
score y el número de accidentes?
"""

query_7 = """
select
id,
credit_score,
past_accidents
from ci
where credit_score > 700 and past_accidents > 1 and
      speeding_violations = 0
""" 
df_7 = sq(query_7)
df_7



"""
# 8.-
¿Cuáles son los conductores que tienen un nivel de educación universitario 
y han tenido al menos 2 DUI, pero tienen un crédito score superior a 600? 
¿Puedes mostrar el ID del conductor, el nivel de educación, el crédito 
score y el número de DUI?
"""

query_8 = """
select
id,
education,
credit_score,
duis
from ci
where education = 1 and duis >= 2 and credit_score > 600 
""" 
df_8 = sq(query_8)
df_8



"""
# 9.-
¿Cuáles son los 3 niveles de educación que tienen el mayor número de 
conductores con un crédito score inferior a 500 y que han tenido al 
menos 1 accidente en el pasado? ¿Puedes mostrar el nivel de educación, 
el número de conductores y el promedio de crédito score para cada nivel 
de educación?
"""

query_9 = """
select
education,
count(*) total_conductores,
avg(credit_score) as media_credit_score
from ci
where credit_score < 500 and past_accidents >= 1
group by education
order by count(*) desc
limit 3;
""" 
df_9 = sq(query_9)
df_9




"""
# 10.-
¿Cuáles son los 5 tipos de vehículos que tienen el mayor número de 
conductores con más de 2 infracciones de velocidad y un crédito 
score inferior a 700? ¿Puedes mostrar el tipo de vehículo, el 
número de conductores y el promedio de infracciones de velocidad 
para cada tipo de vehículo? Además, ordena los resultados por 
el promedio de infracciones de velocidad en orden descendente.
"""

query_10 = """
select
vehicule_type,
count(*) as numero_conductores,
avg(speeding_violations) as media_infracciones_felocidad
from ci
where speeding_violations > 2 and and credit_score < 700
group by vehicle_type 
order by media_infracciones_velocidad desc
limit 5;
""" 
df_10 = sq(query_10)
df_10

