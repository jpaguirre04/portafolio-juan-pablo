# -*- coding: utf-8 -*-
"""
Created on Sat May 31 20:41:16 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# https://www.kaggle.com/datasets/harishkumardatalab/medical-insurance-price-prediction

con = sqlite3.connect('db_insurance_medical.db')
df1 = pd.read_csv('mi.csv')

df1.to_sql('mi', con, if_exists='replace', index=False)

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
from mi
limit 100;
"""
df_0 = sq(query_0)
# df_0.columns

"""
# 1.-
Calcular el promedio de los cargos de seguro médico para fumadores y 
no fumadores, y mostrar los resultados en una tabla con dos columnas: 
Smoker y Average_Charges.
"""

query_1 = """
select
smoker,
avg(charges) as average_charges
from mi
group by smoker
""" 
df_1 = sq(query_1)
df_1


"""
# 2.-
Calcular el promedio de los cargos de seguro médico para cada región, 
pero solo para los asegurados que tienen un índice de masa corporal 
(BMI) mayor a 30.
"""

query_2 = """
select
region,
avg(charges) as cargos_por_region
from mi
where bmi > 30
group by region
""" 
df_2 = sq(query_2)
df_2



"""
# 3.-
Encontrar la región con el mayor promedio de cargos de seguro médico 
para fumadores que tienen más de 2 hijos y un BMI mayor a 25.
"""

query_3 = """
select
region,
avg(charges) as cargo_por_region
from mi
where smoker = 'yes' and children > 2 and bmi > 25
group by region
order by avg(charges) desc
limit 1;
""" 
df_3 = sq(query_3)
df_3




"""
# 4.-
¿Cuál es la región con el mayor promedio de cargos de seguro médico para 
fumadores que tienen más de 2 hijos y un BMI mayor a 25, y que también 
tienen un promedio de edad mayor al promedio de edad general de todos 
los asegurados?
"""

query_4 = """
with promedio_edad_general as(
        select
        avg(age) as edad_promedio
        from mi
        ),
     fumadores as (
         select
         region,
         avg(charges) as cargo_medio_por_region,
         avg(age) as edad_media_por_region
         from mi
         where smoker = 'yes' and children > 2 and bmi > 25
         group by region
         ) 
select
region,
cargo_medio_por_region,
edad_media_por_region
from fumadores 
where  edad_media_por_region = (select
                                max(cargo_medio_por_region)
                                from fumadores
                                where edad_media_por_region > (select
                                                               edad_promedio
                                                               from promedio_edad_general
                                                               )
                                )
""" 
df_4 = sq(query_4)
df_4



query_4_a = """
with fumadores as (
         select
         region,
         avg(charges) as cargo_medio_por_region,
         avg(age) as edad_media_por_region
         from mi
         where smoker = 'yes' and children > 2 and bmi > 25
         group by region
         ) 
select
region,
cargo_medio_por_region,
edad_media_por_region
from fumadores 
where  edad_media_por_region = (select
                                max(edad_media_por_region)
                                from fumadores
                                where edad_media_por_region >(select
                                                              avg(age)
                                                              from mi)
                                )
""" 
df_4_a = sq(query_4_a)
df_4_a



"""
# 5.-
Encuentra las 3 regiones con el mayor promedio de cargos de seguro médico 
para fumadores que tienen más de 2 hijos y un BMI mayor a 25. Luego, para 
cada una de estas regiones, calcula el porcentaje de asegurados que tienen 
un cargo de seguro médico mayor al promedio de cargos de seguro médico 
de la región.
"""

query_5 = """
with fumadores as(
        select
        region,
        avg(charges) as cargo_medio_por_region
        from mi
        where smoker = 'yes' and children > 2  and bmi > 25 
        group by region
        ),
     top_3_regiones as(
         select
         region
         from fumadores
         order by cargo_medio_por_region
         limit 3
         )
select
f.region,
f.cargo_medio_por_region,
sum(case when m.charges > f.cargo_medio_por_region then 1 end) * 1.0
/ count(*)  as porcentaje
from mi m
join fumadores as f on m.region = f.region
join top_3_regiones as t on f.region = t.region
where m.smoker = 'yes' and m.children > 2 and m.bmi > 25
group by t.region
""" 
df_5 = sq(query_5)
df_5



"""
# 6.-
¿Cuál es el promedio de cargos de seguro médico para cada región, 
clasificado por la cantidad de hijos que tienen los asegurados? 
Es decir, quieres saber el promedio de cargos de seguro médico 
para asegurados con 0 hijos, 1 hijo, 2 hijos, 3 hijos, etc.
"""


query_6 = """
with hijos as(
        select
        region,
        case
           when children < 3 then 'poco'
           when children >= 3 and children <= 4 then 'medio'
           else 'alto'
        end as ninos,
        avg(charges) as carga_media
        from mi
        group by region, ninos
        )
select
*
from hijos
""" 
df_6 = sq(query_6)
df_6




"""
# 7.-
¿Cuál es la región con el mayor promedio de cargos de seguro médico para 
fumadores que tienen más de 2 hijos y un BMI mayor a 25, y que también 
tiene el mayor porcentaje de asegurados que son fumadores?
"""

query_7 = """
with fum as(
        select
        region,
        avg(charges) as  promedio
        from mi
        where smoker = 'yes' and children > 2 and bmi > 25 
        group by region
        )
select
f.region,
f.promedio,
1.0*sum(case when mi.smoker = 'yes' then 1 end) / count(*)
as porcentaje
from mi
inner join fum as f on mi.region = f.region 
group by f.region, f.promedio
order by porcentaje desc
limit 1;
""" 
df_7 = sq(query_7)
df_7














