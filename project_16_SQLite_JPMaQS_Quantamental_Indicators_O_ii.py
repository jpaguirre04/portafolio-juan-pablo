# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 10:47:48 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd

# JPMaQS Quantamental Indicators
# https://www.kaggle.com/datasets/macrosynergy/fixed-income-returns-and-macro-trends

con = sqlite3.connect('db_jpm.db')
df1 = pd.read_csv('jpm.csv')

df1.to_sql('jpm', con, if_exists='replace', index=False)

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
from jpm
limit 100;
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
Quieres obtener la suma de los valores (`Value`) para cada categoría (`Xcat`)
en la fecha más reciente (`Real_date`) para cada identificador (`Cid`).
"""

query_1 = """
with reciente as (
        select
        cid,
        max(real_date)
        from jpm
        group by cid        
        )
select
t1.xcat,
sum(value) as total_valores
from jpm t1
inner join reciente t2 on t1.cid = t2.cid
group by t1.xcat
order by total_valores desc
""" 
df_1 = sq(query_1)
# df_1





"""
# 2.-
Quieres obtener la categoría (`Xcat`) con el mayor incremento en el valor 
(`Value`) entre la fecha más reciente y la fecha más antigua para cada 
identificador (`Cid`).
"""

query_2 = """
with minimo as(
        select
        cid,
        min(real_date) fecha_minima,
        value as valor_del_min
        from jpm
        group by cid
        ),
    maxima as(
        select
        cid,
        max(real_date) fecha_maxima,
        value as valor_del_max
        from jpm
        group by cid
        ),
    ambos as(
        select
        t1.cid,
        (t2.valor_del_max - t1.valor_del_min) as incremento
        from minimo t1
        inner join maxima t2 on t1.cid = t2.cid
        )
    
select
j1.xcat,
max(j2.incremento) as mayor_incremento
from jpm as j1
inner join ambos as j2 on j1.cid = j2.cid
""" 
df_2 = sq(query_2)
df_2



"""
# 3.-
Quieres obtener el número de categorías (`Xcat`) únicas para cada 
identificador (`Cid`) que tengan al menos un valor (`Value`) mayor 
que 0 en cualquier fecha (`Real_date`).

*Pista:* Puedes utilizar la función `COUNT(DISTINCT)` para contar 
el número de categorías únicas y la cláusula `WHERE` o `HAVING` 
para filtrar los resultados.
"""


query_3 = """
select
cid,
count(distinct xcat) as distintos_xcat
from jpm
where value > 0
group by cid
having count(distinct xcat) > 0
order by distintos_xcat desc
""" 
df_3 = sq(query_3)
df_3



"""
# 4.-
Quieres obtener el promedio de los valores (`Value`) para cada categoría 
(`Xcat`) y ordenarlos de manera descendente según el promedio. Sin 
embargo, solo quieres incluir las categorías que tengan al menos 5 
registros en la tabla `jpm`.
"""

query_4 = """
select
xcat,
avg(value) as media
from jpm
group by xcat
having count(*) >= 5
order by avg(value) desc
""" 
df_4 = sq(query_4)
df_4



"""
# 5.-
Quieres obtener el `Cid` y el valor máximo (`Value`) para cada `Cid` en 
la tabla `jpm`, pero solo para las fechas (`Real_date`) que sean anteriores 
a una fecha específica (por ejemplo, '2022-01-01').
"""

query_5 = """
select
cid,
max(value) as maximo_valor
from jpm
where real_date < '2022-01-01'
group by cid
""" 
df_5 = sq(query_5)
df_5







