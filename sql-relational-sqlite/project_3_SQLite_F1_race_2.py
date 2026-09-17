# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 16:58:34 2025

@author: Juan Pablo Aguirre
"""


import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# https://www.kaggle.com/datasets/davidcochran/formula-1-race-data-sqlite

conn = sqlite3.connect('Formula1.sqlite')
c = conn.cursor()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(table)


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

query_0 = """
select
*
from races
"""
df_0 = sq(query_0)
# df_0.columns
# df_0['Fastestlap'].min()


query_1 = """
select
*
from drivers
"""
df_1 = sq(query_1)
# df_1.columns


"""
# 1.-
Determinar el piloto que ha tenido la mayor cantidad de "vueltas rápidas" 
(fastest laps) en cada temporada, considerando solo aquellos pilotos que 
han participado en al menos el 75% de las carreras de la temporada. Además, 
debes mostrar el porcentaje de vueltas rápidas que cada piloto ha logrado 
en relación con el número total de carreras en las que ha participado.
"""

query_1 = """
with  vueltas_rapidas as(
        select
        r.driverid,
        r.raceid,
        r.fastestlap,
        r.raceid,
        count(r.resultid) over(partition by r.driverid, r.raceid) as num_vueltas
        from results r
        where r.fastestlap = 17
        ),
      participaciones as(
          select
          r.driverid,
          r.raceid,
          count(r.resultid) over (partition by r.driverid) as num_carreras
          from results r
          ),
      temporadas as(
          select
          r.raceid,
          rs.year,
          count(r.resultid) over (partition by rs.year) as num_carreras_temporada
          from results r
          inner join races rs on r.raceid = rs.raceid
          )
select    
vr.driverid,
d.driverref,
t.year,
count(vr.raceid) as num_vueltas_rapidas,
round(count(vr.raceid)* 100/ p.num_carreras, 2) as porcentaje_vueltas_rapidas
from vueltas_rapidas vr
inner join drivers d on vr.driverid = d.driverid
inner join participaciones p on vr.driverid = p.driverid
inner join temporadas t on vr.raceid = t.raceid
where p.num_carreras >= 0.75 * t.num_carreras_temporada
group by vr.driverid, d.driverref, t.year
order by t.year, num_vueltas_rapidas desc
"""
df_1 = sq(query_1)
df_1

# df_1.to_csv('F1_race_scrip_2_exercise_1')


#################################################################################


"""
# 2.-
Determinar los pilotos que han logrado la mayor cantidad de podios 
(1er, 2do o 3er lugar) en diferentes circuitos durante su carrera. Además, 
debes mostrar el porcentaje de podios que cada piloto ha logrado en relación 
con el número total de carreras que ha disputado en cada circuito.
"""

query_2 = """
select
d.driverref,
rc.circuitid,
count(case when r.position in(1,2,3)  then 1 else null end) as num_podios,
round(count(case when r.position in(1,2,3) then 1 else null end) * 100/ count(*), 2) as porcentaje_podios
from results r
inner join  drivers d on r.driverid = d.driverid
inner join races rc on r.raceid = rc.raceid
group by d.driverref, rc.circuitid 
order by num_podios desc,  porcentaje_podios desc
"""
df_2 = sq(query_2)
df_2

# df_2.to_csv('F1_race_scrip_2_exercise_2')

