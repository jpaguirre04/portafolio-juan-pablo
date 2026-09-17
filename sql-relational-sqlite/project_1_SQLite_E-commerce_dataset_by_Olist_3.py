# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 10:09:06 2025

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
max(Order_purchase_timestamp) 
from orders
"""
df_0 = sq(query_0)
df_0.columns
# df_0['Order_purchase_timestamp'].min()

"""
# 1.-
¿Cuáles son los 10 clientes con mayor valor promedio de pedido en los últimos 
6 meses, considerando solo aquellos que han realizado al menos 3 pedidos en 
ese período y que tienen un valor total de pedidos superior al promedio 
general de la plataforma?
"""

query_1 = """
with 
   -- Calcula el valor promedio de pedido para cada cliente en los últimos 6 meses
   promedio_pedido_cliente as (
   select
   c.customer_id,
   avg(oi.price) as promedio_pedido
   from customers as c
   inner join orders as o on c.customer_id = o.customer_id
   inner join order_items as oi on o.order_id = oi.order_id
   where  o.order_purchase_timestamp <=  date('2018-10-17', '-6 month')  
   group by c.customer_id
   ),
   -- Calcula el valor total de pedidos para cada cliente en los últimos 6 meses
   total_pedido_cliente as(
   select
   c.customer_id,
   sum(oi.price) as total_pedido
   from customers as c
   inner join orders as o on c.customer_id = o.customer_id
   inner join order_items as oi on o.order_id = oi.order_id
   where  o.order_purchase_timestamp <=  date('2018-10-17', '-6 month')  
   group by c.customer_id
   ),
   -- Calcula el promedio general de la plataforma
   promedio_general as(
       select
       avg(oi.price) as promedio_general
       from order_items as oi
       )
select
ppc.customer_id,
ppc.promedio_pedido,
tpc.total_pedido,
rank() over(order by ppc.promedio_pedido desc) as ranking
from promedio_pedido_cliente as ppc
inner join total_pedido_cliente as tpc
on ppc.customer_id = tpc.customer_id
where tpc.total_pedido > (select promedio_general from promedio_general)
and  tpc.customer_id in (
                         select
                         c.customer_id
                         from customers c
                         inner join orders o on c.customer_id = o.customer_id
                         where
                         o.order_purchase_timestamp >= date('2018-10-17', '-6 month')
                         group by c.customer_id
                         having count(o.order_id) >= 3
                        )
order by ranking
"""
df_1 = sq(query_1)
df_1
# --timestamp_sub(timestamp, interval 30 day)


###############################################################################



query_00 = """
select 
*
from order_payments 
"""
df_00 = sq(query_00)
df_00.columns


"""
# 2.-
¿Cuáles son los 10 días del año con mayor valor total de pagos en la 
plataforma Olist, y qué porcentaje del total de pagos realizados en el 
año corresponden?
"""

query_2 = """
select
o.order_purchase_timestamp as fecha_pago,
sum(op.payment_value) as valor_total_pago
from orders as o
inner join order_payments as op 
on o.order_id = op.order_id
group by fecha_pago
order by valor_total_pago desc
limit 10;
"""
df_2 = sq(query_2)
df_2


# --timestamp_sub(timestamp, interval 30 day)

