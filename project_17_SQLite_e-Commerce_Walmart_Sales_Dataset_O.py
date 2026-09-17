# -*- coding: utf-8 -*-
"""
Created on Mon May 26 10:29:13 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd

# walmart-sales-dataset 
# https://www.kaggle.com/datasets/devarajv88/walmart-sales-dataset

con = sqlite3.connect('db_walmart.db')
df1 = pd.read_csv('w.csv')

df1.to_sql('w', con, if_exists='replace', index=False)

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
from w
limit 100;
"""
df_0 = sq(query_0)
# df_0.columns

"""
# 1.-
¿Cuál es el total de compras (`Purchase`) realizadas por cada categoría de 
producto (`Product_category`)?
"""

query_1 = """
select
product_category,
sum(purchase) as total_compras
from w
group by product_category
order by total_compras desc
""" 
df_1 = sq(query_1)
# df_1




"""
# 3.-
¿Cuál es la categoría de producto (`Product_category`) que tiene el mayor 
número de clientes (`User_id`) que han realizado compras (`Purchase`) 
en más de una categoría de producto (`Product_category`)?
"""

query_3 = """
select
product_category,
count(distinct user_id) as numero_clientes
from w
where user_id in(select
                 user_id
                 from (select
                       user_id,
                       count(distinct product_category) as num_categorias
                       from w
                       group by user_id
                     ) as subquery
                 where num_categorias > 1
                )
group by product_category
order by numero_clientes desc;
""" 
df_3 = sq(query_3)
df_3




"""
# 4.-
¿Cuáles son los 5 productos (`Product_id`) más vendidos en la categoría de 
producto (`Product_category`) que tiene el mayor total de compras 
(`Purchase`)?
"""

query_4 = """
select
product_id,
sum(purchase) as total_compras
from w
where product_category in   (select
                            product_category
                            from w
                            group by product_category
                            order by sum(purchase) desc
                            limit 1
                            )
group by product_id
order by total_compras desc
limit 5;
""" 
df_4 = sq(query_4)
df_4




"""
# 5.-
¿Cuáles son las 3 ocupaciones (`Occupation`) que tienen el mayor promedio 
de compras (`Purchase`) en la categoría de productos (`Product_category`) 
más comprada por mujeres (`Gender` = 'F')?
"""

query_5 = """
select
occupation,
avg(purchase) as compras_medias
from w
where gender = 'F' and 
      product_category in (select
                           product_category
                           from w
                           where gender = 'F' 
                           group by product_category
                           order by sum(purchase) desc
                           limit 1
                           )
group by occupation
order by compras_medias desc
limit 3;
""" 
df_5 = sq(query_5)
df_5



"""
# 6.-
¿Cuál es la categoría de producto (`Product_category`) que tiene la mayor 
diferencia en el promedio de compras (`Purchase`) entre hombres 
(`Gender` = 'M') y mujeres (`Gender` = 'F')?
"""

query_6 = """
with hombres as(
               select
               product_category,
               avg(purchase) as media_compras_h
               from w
               where gender = 'M'
               group by product_category
               ),
     mujeres as(
               select
               product_category,
               avg(purchase) as media_compras_m
               from w
               where gender = 'F'
               group by product_category
              )
select
h.product_category,
abs(h.media_compras_h - m.media_compras_m) as diferencias
from hombres as h
join mujeres as m on h.product_category = m.product_category
order by diferencias desc
limit 1;
""" 
df_6 = sq(query_6)
df_6




"""
# 7.-
¿Cuál es la ocupación (`Occupation`) que tiene el mayor número de clientes 
(`User_id`) que compran productos en más de una categoría (`Product_category`)?
"""

query_7 = """
with clientes as(
        select
        user_id
        from w
        group by user_id
        having count(distinct product_category) > 1        
        )
select
occupation
from w
where user_id in (select
                  user_id
                  from clientes)
group by occupation
order by count(distinct user_id) desc
limit 1
""" 
df_7 = sq(query_7)
df_7




"""
# 8.-
¿Cuál es la ciudad (`City_category`) que tiene el mayor promedio de compras 
(`Purchase`) para clientes que llevan más de 2 años viviendo en la misma 
ciudad (`Stay_in_current_city_years` > 2)?
"""

query_8 = """
select
city_category,
avg(purchase) as compras_medias
from w
where Stay_in_current_city_years > 2
group by city_category
order by compras_medias desc
limit 1;
""" 
df_8 = sq(query_8)
df_8




"""
# 9.-
¿Cuál es la ocupación (`Occupation`) que tiene el mayor número de clientes 
que compran productos en la categoría de mayor venta (`Product_category` 
con el mayor total de compras)?
"""

query_9 = """
with compras as(
        select
        product_category
        from w
        group by product_category
        order by sum(purchase) desc
        limit 1
        )
select
occupation
from w
where product_category in (select
                           product_category
                           from compras)
group by occupation
order by count(user_id) desc
limit 1;
""" 
df_9 = sq(query_9)
df_9



"""
# 10.-
¿Cuál es el producto (`Product_ID`) que tiene la mayor cantidad de compras 
(`Purchase`) en la categoría de productos más comprada por mujeres 
(`Gender` = 'F')?
"""

query_10 = """
with compras as(
        select
        product_category
        from w
        where gender = 'F'
        group by product_category
        order by sum(purchase) desc
        limit 1
        )
select
product_id
from w
where product_category  in (select
                            product_category
                            from compras)
group by product_id
order by sum(purchase) desc
limit 1
""" 
df_10 = sq(query_10)
df_10



"""
# 11.-
¿Cuál es la ocupación (`Occupation`) que tiene la mayor proporción de 
clientes que compran productos en más de una categoría (`Product_category`) 
en comparación con el total de clientes de esa ocupación?
"""

# hacer de nuevo
query_11 = """
with clientes_mas_producto as(
        select
        occupation,
        user_id
        from w
        group by occupation, user_id
        having count(distinct user_id) > 1
        ),
     total_clientes as(
         select
         occupation,
         count(distinct user_id) as total_clientes_ocupacion
         from w
         group by occupation
         ),
     clientes_mas_producto_ocupation as(
         select
         occupation,
         count(distinct user_id) as clientes_mas_producto_ocupacion
         from w
         group by occupation
         )
select
cmp.occupation,
1.0 * cmp.clientes_mas_producto_ocupacion /
tc.total_clientes_ocupacion as proporcion
from clientes_mas_producto_ocupation cmp
join total_clientes tc on cmp.occupation = tc.occupation
order by proporcion desc
limit 1;
""" 
df_11 = sq(query_11)
df_11



"""
# 12.-
¿Cuál es el rango de edad (`Age`) que tiene el mayor número de clientes 
que compran productos en la categoría de electrónica 
(`Product_category` = 1)?
"""

query_12 = """
select
case 
    when age >= 18 and age <= 24 then 'niño'
    when age >= 25 and age <= 34 then 'joven'
    when age >= 35 and age <= 44 then 'adulto_joven'
    else 'adulto'
end rangos,
count(distinct user_id) as clientes
from w
where product_category = 1
group by rangos
order by clientes desc
limit 1;
""" 
df_12 = sq(query_12)
df_12




"""
# 13.-
¿Cuál es la ocupación (`Occupation`) que tiene el mayor número de 
clientes que compran en solo una categoría de productos 
(`Product_category`)?
"""

query_13 = """
with clientes as(
        select
        user_id,
        count(distinct product_category) as categorias
        from w
        group by user_id
        having count(distinct product_category) = 1
        )
select
w.occupation,
count(distinct w.user_id) as usuarios
from w
join clientes as c on w.user_id = c.user_id
group by w.occupation
order by count(distinct w.user_id) desc
limit 1
""" 
df_13 = sq(query_13)
df_13



"""
# 14.-
¿Cuál es la categoría de producto (`Product_category`) que tiene el 
mayor número de productos comprados por usuarios que tienen una 
ocupación (`Occupation`) que comienza con la letra 4?
"""

query_14 = """
select
product_category,
sum(purchase) as productos_comprados
from w
where occupation = 4
group by product_category
order by sum(purchase) desc
limit 1;
""" 
df_14 = sq(query_14)
df_14



"""
# 15.-
¿Cuál es el producto (`Product_ID`) que tiene el mayor número de compras 
(`Purchase`) en la categoría de productos (`Product_category`) 
igual a 3?
"""

query_15 = """
select
product_id,
sum(purchase) as suma
from w
where product_category = 3
group by product_id
order by sum(purchase) desc
limit 1
""" 
df_15 = sq(query_15)
df_15



