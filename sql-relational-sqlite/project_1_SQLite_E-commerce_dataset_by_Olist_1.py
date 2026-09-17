# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:31:40 2025

@author: Juan Pablo Aguirre
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database?select=olist.sqlite

conn = sqlite3.connect('olist.sqlite')
c = conn.cursor()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(table)


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())


"""
# 0.- 
toda la tabla
"""

query_0 = """
select 
*
from sellers
"""
df_0 = sq(query_0)
df_0.columns

"""
# 1.- 
¿ cuántos vendedores hay en la tabla sellers ?
"""

query_1 = """
select 
count(*) as total_vendedores
from sellers
"""
df_1 = sq(query_1)
df_1


"""
# 2.- 
¿ cuatons son los 5 vendedores con mayor cantidad de productos ofrecidos,
y cuantos productosa ofrecen cada uno ?
"""

query_2 = """
with productos_por_vendedor as(
        select
        Seller_id,
        count(*) as cantidad_productos
        from sellers
        group by Seller_id
        )
select
seller_id,
cantidad_productos
from productos_por_vendedor
order by cantidad_productos desc
limit 5;
"""
df_2 = sq(query_2)
df_2


"""
# 3.- 
¿Cuál es el ranking de los vendedores según su ID de vendedor?
"""

query_3 = """
select
seller_id,
rank() over(order by seller_id asc) as ranking
from sellers
order by seller_id asc
limit 10;
"""
df_3 = sq(query_3)
df_3



"""
# 4.- 
¿Cuál es el ranking de los vendedores según su código postal 
(Seller_zip_code_prefix)?
"""

query_4 = """
select
seller_id,
seller_zip_code_prefix,
rank() over(order by seller_zip_code_prefix asc) as ranking
from sellers
order by Seller_zip_code_prefix asc
"""
df_4 = sq(query_4)
df_4



"""
# 5.- 
¿Cuáles son los 3 estados con mayor cantidad de vendedores y cuántos 
vendedores hay en cada uno, considerando solo los vendedores que están 
en ciudades que comienzan con la letra "S"?
"""

query_5 = """
select
seller_state,
count(*) as cantidad_vendedores
from sellers
where seller_city like '%S%'
group by seller_state
order by cantidad_vendedores desc
limit 3
"""
df_5 = sq(query_5)
df_5



"""
# 6.- 
¿Cuáles son los vendedores que tienen un código postal mayor que el promedio 
de códigos postales de todos los vendedores?
"""

query_6 = """
select
*
from sellers
where  seller_zip_code_prefix > (select 
                                 avg(seller_zip_code_prefix) 
                                 from sellers)
"""
df_6 = sq(query_6)
df_6



"""
# 7.- 
¿Cuáles son los vendedores que tienen un código postal mayor que el promedio 
de códigos postales de todos los vendedores, considerando solo los vendedores 
que están en ciudades que comienzan con la letra "S" y ordenando los 
resultados por código postal en orden descendente?
"""

query_7 = """
select
*
from sellers
where seller_zip_code_prefix > (select 
                                 avg(seller_zip_code_prefix) 
                                 from sellers)
      and seller_city like 'S%'
order by seller_zip_code_prefix  desc    
"""
df_7 = sq(query_7)
df_7



##############################################################################


"""
# 8.- 
¿ cuales son los vendedores que se encuentran en las ciudades con latitud menor
a -20 y cual es su respectiva localización?
"""


queri_0 = """
select
*
from geolocation
limit 100;
"""
df_00 = sq(queri_0)
df_00.columns


query_8 = """
select
s.seller_id,
s.seller_city, 
g.geolocation_lat,
g.geolocation_lng
from sellers s
join geolocation g 
on s.seller_city = g.geolocation_city
where g.geolocation_lat < -20
"""
df_8 = sq(query_8)
df_8



"""
# 9.- 
¿Cuáles son las 10 ciudades con mayor latitud promedio, considerando sólo las
ciudades que tienen más de 1000 registros y ordenando los resultados por 
latitud promedio en orden descendente, y además, muestra el ranking de cada 
ciudad según su latitud promedio?
"""

query_9 = """
with ciudad_latitud_promedio as(
                select
                geolocation_city,
                avg(geolocation_lat) as latitud_promedio
                from geolocation
                group by geolocation_city
                having count(*) > 1000
                )
select
geolocation_city,
latitud_promedio,
rank() over(order by latitud_promedio desc) as ranking
from ciudad_latitud_promedio
order by latitud_promedio
limit 10
"""
df_9 = sq(query_9)
df_9



"""
# 10.- 
¿Cuáles son las 10 ciudades con mayor latitud promedio, considerando solo las 
ciudades que tienen más de 1000 registros y que se encuentran en el mismo 
estado, y muestra el ranking de cada ciudad según su latitud promedio, 
uniendo la información de la tabla geolocation consigo misma para relacionar 
las ciudades por estado?
"""

query_10 = """
with ciudad_latitud_promedio as(
        select
        g1.geolocation_city,
        avg(g1.geolocation_lat) as latitud_promedio
        from geolocation g1
        inner join geolocation g2 
        on g1.geolocation_state = g2.geolocation_state
        group by g1.geolocation_city
        having count(distinct g1.geolocation_city)> 1 and count(*) > 1000
        )
select
geolocation_city,
latitud_promedio,
rank() over(order by latitud_promedio desc) as ranking
from ciudad_latitud_promedio
order by latitud_promedio desc
limit 10
"""
# df_10 = sq(query_10)
# df_10








"""
# 11.- 
¿Cuáles son los vendedores que se encuentran en la misma ciudad que otros 
vendedores, y muestra la jerarquía de ciudades donde se encuentran estos 
vendedores?
"""

query_11 = """
with recursive sellers_ciudades as(
        select
        seller_id,
        seller_city,
        0 as nivel
        from sellers
        union all
        select 
        s.seller_id,
        s.seller_city,
        nivel + 1
        from sellers s 
        join sellers_ciudades sc on s.seller_city = sc.seller_city
        where s.seller_id != sc.seller_id
        )
select distinct
seller_id,
seller_city
from sellers_ciudades
where nivel > 0
"""
# df_11 = sq(query_11)
# df_11


















