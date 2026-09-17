# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:11:44 2025

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
from orders
"""
df_0 = sq(query_0)
df_0.columns


"""
# 1.-
¿Cuál es el promedio de tiempo de entrega de los pedidos? 
"""

query_1 = """
with tiempos_entrega as(
        select
        order_id,
        julianday(Order_delivered_customer_date) - julianday(Order_purchase_timestamp) as tiempo_entrega
        from orders
        )
select
avg(tiempo_entrega) as promedio_tiempo_entrega
from tiempos_entrega;
"""
df_1 = sq(query_1)
df_1



"""
# 2.- 
¿Cuáles son los pedidos que tienen un monto total mayor que el promedio de 
monto total de todos los pedidos?
"""

query_2 = """
select
order_id,
Order_purchase_timestamp,
order_status
from orders
where Order_purchase_timestamp > 
      (select avg(julianday(Order_purchase_timestamp)) from orders);
"""
df_2 = sq(query_2)
df_2


"""
# 3.- 
¿Cuáles son los pedidos que tienen un estado de "approved"?
"""

query_3 = """
SELECT 
  Order_id,
  Order_purchase_timestamp,
  Order_status
FROM 
  orders
WHERE 
  Order_status = 'approved';
"""
df_3 = sq(query_3)
df_3


##################################################################################




query_00 = """
select 
*
from customers
"""
df_00 = sq(query_00)
df_00.columns


"""
# 4.- 
¿Cuáles son los 5 estados con mayor cantidad de clientes, ordenados por la 
cantidad de clientes en descenso y con un número de fila?
"""

query_4 = """
with clientes_por_estado as(
        select
        customer_state,
        count(customer_id) as cantidad_clientes
        from customers
        group by customer_state
        )
select
customer_state,
cantidad_clientes,
row_number() over(order by cantidad_clientes desc) as row_num
from clientes_por_estado
limit 5;
"""
df_4 = sq(query_4)
df_4



"""
# 5.- 
¿Cuáles son los clientes que viven en estados con más de 100 clientes, 
ordenados por la cantidad de clientes en su estado y con un ranking de 
cantidad de clientes en su estado?
"""

query_5 = """
with clientes_por_estado as(
        select
        customer_state,
        count(customer_id) as cantidad_clientes
        from customers
        group by customer_state
        ),
     ranking_clientes_por_estado as(
        select
        customer_id,
        customer_state,
        rank() over(order by (select count(*) from customers c2 where c2.customer_state = c1.customer_state) desc) as ranking
        from customers c1
        )
select
*
from ranking_clientes_por_estado
where customer_state in (select customer_state from clientes_por_estado where cantidad_clientes > 100);
"""
df_5 = sq(query_5)
df_5



query_5_b = """
select
c.customer_id,
c.customer_state,
rank() over(order by cnt desc) as ranking
from customers c
join (
      select
      customer_state,
      count(*) as cnt
      from customers
      group by customer_state
      ) as cnt_table on c.customer_state = cnt_table.customer_state;
"""
df_5_b = sq(query_5_b)
df_5_b



"""
# 6.- 
¿Cuáles son los 5 estados con mayor cantidad de clientes en la ciudad de 
São Paulo, ordenados por la cantidad de clientes en descenso?
"""

query_6 = """
select
customer_state,
count(customer_id) as cantidad_clientes
from  customers
where customer_city = 'sao paulo'
group by customer_state
order by cantidad_clientes desc
limit 5;
"""
df_6 = sq(query_6)
df_6
