# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 10:33:01 2025

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

df1['grading'].unique()


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
Usando la tabla que contiene las columnas mencionadas, 
escribe una consulta que retorne la fecha (Real_date), 
el país/moneda (Cid) y el valor (Value) del indicador más
alto (máximo), para cada categoría de indicador (Xcat) distinta.

Tu resultado debe mostrar una sola fila por cada Xcat que 
exista en la base de datos, con el registro que tenga el 
Value más alto asociado.

hay dos formas
"""

# este
query_1 = """
select
t1.real_date,
t1.cid,
t1.xcat,
t1.value
from jpm t1
inner join (
           select
           xcat,
           max(value) as maxvalue
           from jpm
           group by xcat
           ) t2
on t1.xcat = t2.xcat and t1.value = t2.maxvalue;
""" 
df_1 = sq(query_1)
df_1


# una solucion más avanzada, con funciones ventana

query_1_i = """
select
real_date,
cid,
xcat,
value
from (
      select
      *,
      -- asigna un numero de fila (rn) a cada fila dentro de su xcat.
      -- orderna de mayor a menor valor (desc).
      row_number() over(partition by xcat order by value desc) as rn
      from jpm
      )
where rn = 1
""" 
df_1_i = sq(query_1_i)
df_1_i



"""
# 2.-
Usando la tabla jpm y asumiendo que el campo Real_date está 
almacenado como texto en formato YYYY-MM-DD, escribe una 
consulta que calcule el promedio (AVG(Value)) para cada 
indicador (Xcat) y para cada país (Cid), pero solo para 
los datos registrados en el segundo trimestre 
(meses de abril, mayo y junio) de todos los años.

El resultado debe mostrar: Xcat, Cid y Average_Q2_Value.
"""

# este
query_2 = """
select
xcat,
cid,
avg(value) Average_Q2_Value
from jpm
where strftime('%m', real_date) in ('04', '05', '06')
group by xcat, cid
""" 
df_2 = sq(query_2)
df_2



"""
# 3.-
Asumiendo que existe un indicador en la columna Xcat 
llamado 'T-BOND', escribe una consulta SQLite que:
Aísle solo los registros donde Xcat es 'T-BOND'.
Calcule el valor del mes anterior del año anterior 
(Value_Lag) utilizando la función de ventana LAG 
(desplazamiento de 12 periodos).
Calcule el Crecimiento Interanual (YOY) para cada fila donde sea posible:

Crecimiento YOY=( 
Valor del A 
n
˜
 o Anterior
Valor Actual)−1
Calcule el promedio de esos crecimientos interanuales para cada 
país/moneda (Cid).

Finalmente, devuelva el país (Cid) que tuvo el mayor crecimiento 
interanual (YOY Growth) promedio.

El resultado final debe ser solo el Cid (y su crecimiento promedio) 
con la mayor tasa de crecimiento.
"""

# este
query_3 = """
select
cid, 
xcat,
value / lag(value, 12, null) over(partition by cid, xcat order by real_date) - 1
as tasa
from jpm 
where xcat is 'T-BOND'
group by cid, xcat
order by real_date 
""" 
df_3 = sq(query_3)
df_3


query_3 = """
select
cid,
avg(tasa_YOY) as promedio_crecimiento_YOY
from (
      -- paso 1: calcular la tasa YOY para cada mes
      select
      cid,
      (value / lag(value, 12 , null) over(
       partition by cid, xcat
       order by real_date) -1) as tasa_YOY
      from jpm
      where xcat = 'T-BOND'
      )
-- Pso 2 : Filtrar y agregar el crecimiento YOY promedio por pais
where  tasa_YOY is not null -- eliminar el primer año de datos (donde LAG es NULL)
group by cid
order by promedio_crecimiento_YOY desc
limit 1;
""" 
df_3 = sq(query_3)
df_3



"""
# 4.-
Objetivo: Queremos ver el valor promedio (Value) y el número total de 
registros para cada categoría de indicador macroeconómico (Xcat) y 
para cada identificador de país o región (Cid) que tenga una calidad 
de datos (Grading) que no sea 'B'.
"""

# este
query_4 = """
select
cid,
xcat,
count(*) as registros,
sum(value) as sumas
from jpm
where grading <> 'B'
group by cid, xcat
""" 
df_4 = sq(query_4)
df_4



"""
# 5.-
Objetivo: Queremos encontrar las tres combinaciones de país/región (Cid) 
y categoría macro (Xcat) con el mayor número de registros (COUNT(*)) y 
cuyo valor promedio (Value) sea negativo (menor que 0).
"""


query_5 = """
select
cid,
xcat,
count(*) as cuantos
from jpm
group by cid, xcat
having avg(value) < 0
order by count(*) desc
limit 3;
""" 
df_5 = sq(query_5)
df_5








