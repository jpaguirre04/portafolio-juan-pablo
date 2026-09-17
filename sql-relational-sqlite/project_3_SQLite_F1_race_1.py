# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 16:14:00 2025

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
from constructors
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
¿Cuáles son los 5 pilotos con mayor número de victorias en los Grandes Premios 
de F1 en los últimos 10 años, considerando solo aquellos pilotos que han 
participado en al menos 50 carreras durante ese período?
"""

query_1 = """
with 
    -- Filtra los resultados para seleccionar sólo los últimos años
   ultimos_10_anos as(
       select
       r.driverid,
       r.constructorid,
       r.position,
       s.year       
       from results r
       inner join races s on r.raceid = s.raceid
       where s.year >=  2018 - 10
       ),
   -- Cuenta el número de victorias para cada piloto
   victorias_por_piloto as (
       select
       driverid,
       count(*) as num_victorias
       from ultimos_10_anos
       where position = 1
       group by driverid
       ),
   -- Cuenta el número total de carreras disputadas por cada piloto
   carreras_por_piloto as(
       select
       driverid,
       count(*) as num_carreras
       from ultimos_10_anos
       group by driverid
       )
select
d.driverref,
v.num_victorias
from victorias_por_piloto v
inner join carreras_por_piloto c on v.driverid = c.driverid
inner join drivers d on v.driverid = d.driverid
where c.num_carreras >= 50
order by v.num_victorias desc
limit 5;
"""
df_1 = sq(query_1)
df_1




"""
# 2.-
Determinar los 5 pilotos con mayor número de victorias en los Grandes Premios 
de F1, considerando solo aquellos pilotos que han participado en al menos 50 
carreras y han obtenido al menos 10 podios.
"""

query_2 = """
select
d.driverref,
count(r.resultid) as num_victorias
from results r
inner join drivers d on r.driverid = d.driverid
where r.position = 1
and d.driverid in(
                 select
                 driverid
                 from results
                 group by driverid
                 having  count(raceid) >= 50
                 and sum(case when position <= 3 then 1 else 0 end) >= 10
                )
group by d.driverref
order by num_victorias desc
limit 5;
"""
df_2 = sq(query_2)
df_2



"""
# 3.-
Determinar el porcentaje de carreras ganadas por cada constructor (equipo) 
en relación con el número total de carreras en las que han participado, 
considerando solo aquellos constructores que han ganado al menos 20 
carreras y han participado en al menos 150 carreras. Ordenar el resultado 
por porcentaje de carreras ganadas en descendente.
"""

query_3 = """
select
c.constructorref,
count(case when r.position = 1 then r.resultid end) as num_victorias,
count(r.resultid) as num_carreras,
round(count(case when r.position = 1 then r.resultid end) * 100 / count(r.resultid), 2) as porcentaje_victorias
from results r
inner join constructors c on r.constructorid = c.constructorid
group by c.constructorref
having count(r.resultid) >= 150
and count(case when r.position = 1 then r.resultid end) >= 20
order by porcentaje_victorias desc;
"""
df_3 = sq(query_3)
df_3




"""
# 4.-
Determinar los 5 circuitos (tracks) con mayor número de victorias de un mismo 
piloto, considerando solo aquellos pilotos que han ganado al menos 3 carreras 
en el mismo circuito. Además, debes mostrar el nombre del piloto que ha 
obtenido más victorias en cada circuito. Ordenar el resultado por número de 
victorias en descendente.
"""

query_4 = """
select
c.circuitref,
d.driverref,
count(r.resultid) as num_victorias
from results r
inner join drivers d on r.driverid = d.driverid
inner join races ra on r.raceid = ra.raceid
inner join circuits as c on ra.circuitid = c.circuitid
where r.position = 1
group by c.circuitref, d.driverref
having count(r.resultid) >= 3
order by num_victorias desc
limit 5;
"""
df_4 = sq(query_4)
df_4





query_0 = """
select
*
from circuits
"""
df_0 = sq(query_0)
# df_0.columns


