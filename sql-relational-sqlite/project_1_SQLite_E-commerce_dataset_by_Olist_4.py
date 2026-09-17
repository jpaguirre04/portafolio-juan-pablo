# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 11:21:19 2025

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

##########################################################################################


query_0 = """
select
*
from product_category_name_translation
"""
df_0 = sq(query_0)
# df_0.columns


# df_0['Product_category_name_english'].unique()

# df_0['Geolocation_lat'].describe()




"""
# 1.-
¿Cuáles son los 10 estados con mayor concentración de clientes con un alto 
valor promedio de pedidos, considerando solo aquellos clientes que se 
encuentran en una latitud entre -2.360355 and -1.997962?
"""

query_1 = """
with 
   -- calcula el valor total de cada pedido 
       total_pedido as(
       select
       o.order_id,
       sum(oi.price) as total_pedido
       from orders as o
       inner join order_items oi on o.order_id = oi.order_id
       group by o.order_id
       ),
   -- calcula el valor promedio de pedidos para cada cliente    
     avg_pedido_cliente as(
         select
         c.customer_id,
         avg(tp.total_pedido) as avg_pedido
         from customers as c
         inner join orders o  on c.customer_id = o.customer_id
         inner join total_pedido tp on o.order_id = tp.order_id
         group by c.customer_id
         ),
   -- Une la información de clientes con su ubicación geográfica
     clientes_geolocation   as (
        select
        c.customer_id,
        g.geolocation_state,
        agc.avg_pedido
        from customers c
        inner join geolocation g on c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
        inner join avg_pedido_cliente agc on c.customer_id = agc.customer_id
        -- where g.geolocation_lat between -2.360355 and -1.997962
        )
select 
cg.geolocation_state,
avg(cg.avg_pedido) as avg_pedido_estado,
sum(cg.avg_pedido) as suma_pedido_estado,
rank() over (order by avg(cg.avg_pedido) desc) as ranking
from clientes_geolocation cg
group by cg.geolocation_state
having   avg(cg.avg_pedido) > (select avg(avg_pedido) from avg_pedido_cliente)
order by ranking 
limit 10;
"""
df_1 = sq(query_1)
df_1


#######################################################################################


"""
# 2.-
¿Cuáles son las categorías de productos con mayor variedad de precios, 
considerando sólo aquellos productos que tienen un precio promedio mayor 
que el promedio general de todos los productos, y que además tienen una 
descripción en inglés?
"""
#  `products` y `products_category_name_translations`

query_2 = """
with 
   -- calcula el precio promedio de cada producto
   avg_precio_producto as(
       select
       p.product_id,
       avg(oi.price) as avg_precio
       from products as p
       inner join order_items as oi on p.product_id = oi.product_id
       group by p.product_id
       ),
  -- Une la información de productos con su categoría y descripción en inglés
  productos_categoria_descripcion as(
      select
      p.product_id,
      pcnt.product_category_name,
      p.product_name_lenght,
      app.avg_precio
      from products p
      inner join product_category_name_translation as pcnt
      on p.product_category_name = pcnt.product_category_name
      inner join avg_precio_producto app on p.product_id = app.product_id
      where pcnt.Product_category_name_english 
              in ('auto', 'bed_bath_table',
             'furniture_decor', 'sports_leisure', 'perfumery', 'housewares',
             'telephony', 'watches_gifts', 'food_drink', 'baby', 'stationery',
             'tablets_printing_image', 'toys', 'fixed_telephony',
             'garden_tools', 'fashion_bags_accessories', 'small_appliances',
             'consoles_games', 'audio')
      )
select
pcd.product_category_name,
min(pcd.avg_precio) as precio_minimo,
max(pcd.avg_precio) as precio_maximo,
avg(pcd.avg_precio) as precio_promedio,
count(distinct pcd.product_id) as cantidad_productos
from productos_categoria_descripcion pcd
where pcd.avg_precio > (select avg(avg_precio) from avg_precio_producto)
group by pcd.product_category_name
order by precio_maximo - precio_minimo desc
limit 10;
"""
df_2 = sq(query_2)
df_2

