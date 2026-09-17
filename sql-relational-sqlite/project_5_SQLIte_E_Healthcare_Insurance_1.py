# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 16:36:11 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# https://www.kaggle.com/datasets/willianoliveiragibin/healthcare-insurance

con = sqlite3.connect('db_insurance.db')

df = pd.read_csv('insurance.csv')

df.to_sql('insurance', con, if_exists='replace', index=False)

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
from insurance
"""
df_0 = sq(query_0)
# df_0.columns




"""
# 1.-
calcula el promedio de gastos en seguros de salud para personas que tienen una 
edad entre 30 y 50 años y que fuman, y que muestra los 5 regiones con mayor 
promedio de gastos:
"""

query_1 = """
with
    -- Subquery para calcular el promedio de gastos por región
    promedio_gastos as(
        select
        region,
        avg(charges) as promedio_gastos
        from insurance
        where age between 30 and 50 
              and smoker = 'yes'
        group by region        
        ),
    -- Subquery para calcular el ranking de las regiones por promedio de gastos
    ranking_regiones as(
        select
        region,
        promedio_gastos,
        row_number() over(order by promedio_gastos desc) as ranking
        from promedio_gastos 
        )
-- Consulta principal para obtener las 5 regiones con mayor promedio de gastos    
select
region,
promedio_gastos
from ranking_regiones    
where ranking <= 5
"""
df_1 = sq(query_1)
df_1



"""
# 2.-
¿Cuál es el promedio de gastos en seguros de salud para personas que tienen 
un índice de masa corporal (BMI) mayor a 30 y que no fuman, y cómo se 
compara con el promedio de gastos para personas que fuman y tienen un BMI 
mayor a 30?
"""

query_2 = """
select
smoker,
avg(charges) as promedio_gastos
from insurance
where bmi > 30
group by smoker;
"""
df_2 = sq(query_2)
df_2



"""
# 3.-
¿Cuál es el promedio de gastos en salud (Charges) para fumadores y no 
fumadores en cada región, y qué región tiene el mayor promedio de gastos 
en salud para fumadores y no fumadores?
"""

query_3 = """
select
region,
smoker,
avg(charges) as promedio_gastos
from insurance
group by region, smoker
order by promedio_gastos desc
"""
df_3 = sq(query_3)
df_3



"""
# 4.-
¿Cuál es la relación entre el índice de masa corporal (Bmi) y los gastos en 
salud (Charges) para diferentes rangos de edad? ¿Cómo cambia esta relación 
según el sexo y el estado de fumador?
"""

query_4 = """
with rangos_edad as(
        select
        case
        when age between 18 and 24 then '18-24'
        when age between 25 and 34 then '25-34'
        when age between 35 and 44 then '35-44'
        when age between 45 and 54 then '45-54'
        when age between 55 and 64 then '5-64'
        else '65+'
        end as rango_edad,
        *
        from insurance
        
        )
select
rango_edad,
sex,
smoker,
avg(charges) as promedio_gastos
from rangos_edad
group by rango_edad, sex, smoker
order by rango_edad, sex, smoker
"""
df_4 = sq(query_4)
df_4



"""
# 5.-
¿Cuál es el impacto de la edad y el índice de masa corporal (Bmi) en los 
gastos en salud (Charges) para fumadores y no fumadores? ¿Cómo cambia este 
impacto según el sexo?
"""

query_5 = """
with datos_preparados as(
        select
        age,
        bmi,
        charges,
        smoker,
        sex,
        case
           when age < 40 then 'joven'
           when age >= 40 and age < 60 then 'adulto'
           else 'mayor'
        end as rango_edad
       from insurance  
       )
select
rango_edad,
sex,
smoker,
avg(charges) as promedio_gastos,
avg(bmi) as promedio_bmi
from datos_preparados
group by rango_edad, sex, smoker
order by rango_edad, sex, smoker
"""
df_5 = sq(query_5)
df_5



"""
# 6.-
¿Cuáles son los 10% de los pacientes con los gastos en salud (Charges) más 
altos, y cómo se distribuyen según la región, el sexo y el estado de fumador? 
¿Cuál es el promedio de gastos en salud para cada grupo de pacientes?
"""

query_6 = """
with pacientes_10porciento as(
        select
        charges,
        region,
        sex,
        smoker
        from insurance
        where charges > (select avg(charges)* 1.5 from insurance)
        ),
     pacientes_rangos as(
        select 
        region,
        sex,
        smoker,
        rank() over(partition by region, sex, smoker order by charges desc) as rango
        from pacientes_10porciento 
        )
select
region,
sex,
smoker,
count(*) as num_pacientes
from pacientes_rangos
where rango >= 10
group by region, sex, smoker
order by region, sex, smoker
"""
df_6 = sq(query_6)
df_6

















