# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 16:52:48 2025

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
from order_items
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
¿Cuáles son los 10 vendedores con mayor valor promedio de ventas por pedido, 
considerando solo aquellos pedidos que tienen un estado de "entregado" y que 
además tienen un valor total mayor que el promedio general de todos los pedidos?
"""

query_1 = """
with
  -- Calcula el valor total de cada pedido
  total_pedido as(
      select
      oi.order_id,
      sum(oi.price) as total_pedido
      from order_items oi
      group by oi.order_id
      ),
  --calcula el valor promedio de ventas por pedido para cada vendedor
  avg_ventas_vendedor as(
      select
      s.seller_id,
      avg(total_pedido) as avg_ventas
      from sellers s
      inner join order_items oi on s.seller_id = oi.seller_id
      inner join total_pedido tp on oi.order_id = tp.order_id
      inner join orders o on tp.order_id = o.order_id
      where o.order_status = 'delivered'
      group by s.seller_id
      )
select
avv.seller_id,
avv.avg_ventas,
row_number() over(order by avv.avg_ventas desc) as row_num,
rank() over(order by avv.avg_ventas desc) as ranking
from avg_ventas_vendedor avv
where avv.avg_ventas > (select avg(total_pedido) from total_pedido)
order by avv.avg_ventas desc
limit 10;
"""
df_1 = sq(query_1)
df_1


#######################################################################################













