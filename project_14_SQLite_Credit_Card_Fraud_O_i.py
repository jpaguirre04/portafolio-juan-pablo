# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 09:40:45 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit_card_fraud_dataset
# https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud


con = sqlite3.connect('db_cc.db')
df1 = pd.read_csv('ct.csv')

df1.to_sql('ct', con, if_exists='replace', index=False)

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
from ct
limit 100;
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 1.-
¿Cuál es la relación entre la distancia desde la ubicación del titular de 
la tarjeta (_Distance_from_home_) y la probabilidad de fraude (_Fraud_)?
"""

query_1 = """
select
sum(case when fraud = 1 then distance_from_last_transaction end) distancia_promedio_fraude,
sum(case when fraud = 0 then distance_from_last_transaction end) distancia_promedio_sin_fraude
from ct
""" 
df_1 = sq(query_1)
df_1




"""
# 2.-
¿Cuál es el porcentaje de transacciones fraudulentas que se realizaron en 
línea (_Online_order = 1_) en comparación con las transacciones no 
fraudulentas?
"""

query_2 = """
select
1.0 * sum(case when online_order = 1 and fraud = 1 then 1 end) / 
(select count(*) from ct where fraud = 1) as porcentaje_fraudulenta,
1.0 * sum(case when online_order = 1 and fraud = 0 then 1 end) / 
(select count(*) from ct where fraud = 0) as porcentaje_no_fraudulenta
from ct
""" 
df_2 = sq(query_2)
df_2


"""
# 3.-
¿Cuál es el porcentaje de transacciones fraudulentas que se realizaron con la 
tecnología de chip (_Used_chip = 1_) en comparación con las transacciones no 
fraudulentas?
"""


query_3 = """
select
1.0 * sum(case when used_chip = 1 and fraud = 1 then 1 end) /
(select count(*) from ct where fraud = 0) as porcentaje_transaccion
from ct
""" 
df_3 = sq(query_3)
df_3



"""
# 4.-
¿Cuál es el porcentaje de transacciones fraudulentas que se realizaron con 
un pedido en línea (_Online_order = 1_) y que también utilizaron un chip 
(_Used_chip = 1_)?
"""

query_4 = """
select
1.0 * sum(case when fraud = 1 and online_order = 1 and used_chip = 1 then 1 end) /
(select count(*) from ct) as porcentaje
from ct
""" 
df_4 = sq(query_4)
df_4


"""
# 5.-
¿Cuál es el porcentaje de transacciones fraudulentas que se realizaron con 
un pedido en línea (_Online_order = 1_) y que también utilizaron un chip 
(_Used_chip = 1_), pero solo para los retailers que tienen un promedio 
de distancia desde la última transacción mayor a 1000?
"""

query_5 = """
select
1.0 * sum(case when online_order = 1 and used_chip = 1 and fraud = 1 then 1 else 0 end) /
(select count(*) from ct) porcentaje_transacciones_fraudulentas
from ct
where distance_from_last_transaction > 1000
""" 
df_5 = sq(query_5)
df_5



"""
# 6.-
Encuentra el porcentaje de transacciones fraudulentas que se realizaron 
con un pedido en línea (_Online_order = 1_) y que también utilizaron un 
chip (_Used_chip = 1_), pero solo para las transacciones que tienen una 
distancia desde la última transacción mayor al promedio de distancia 
desde la última transacción de todas las transacciones no 
fraudulentas
"""


query_6 = """
select
1.0 * sum(case when online_order = 1 and used_chip = 1 and fraud = 1 then 1 end) /
(select count(*) from ct where fraud = 1) as porcentaje_transacciones
from ct
where 
       distance_from_last_transaction > (select 
                                         avg(distance_from_last_transaction)
                                         from ct) 
""" 
df_6 = sq(query_6)
df_6




"""
# 7.-
Encuentra el promedio de la distancia desde la última transacción para las 
transacciones fraudulentas que se realizaron con un pedido en línea 
(_Online_order = 1_) y que también utilizaron un chip (_Used_chip = 1_), 
pero solo para los casos en que la distancia desde la última transacción 
sea mayor que la mediana de la distancia desde la última transacción para 
todas las transacciones no fraudulentas.
"""

query_7 = """
with rank_transaction as(
        select
        distance_from_last_transaction,
        row_number() over(order by distance_from_last_transaction) as row_number,
        count(*) over() as total_rows
        from ct
        where fraud = 0
        ),
     medianaa as(
         select
         avg(distance_from_last_transaction) as mediana
         from rank_transaction
         where row_number in ((total_rows + 1)/2 + (total_rows +2)/2)
         )
select
avg(distance_from_last_transaction)
from ct
where  online_order = 1 and
      used_chip = 1 and 
      fraud = 1 and
      distance_from_last_transaction > (select mediana from medianaa)
""" 
df_7 = sq(query_7)
df_7



"""
# 8.-
Encuentra el número de transacciones fraudulentas que se realizaron con 
un pedido en línea (`Online_order = 1`) y que tuvieron un ratio de precio 
de compra mayor que 1,5 veces el ratio de precio de compra promedio de 
todas las transacciones no fraudulentas.
"""


query_8 = """
select
count(*) as transacciones_fraudulentas
from ct
where fraud = 1 and online_order = 1 and 
         ratio_to_median_purchase_price > 
         1.5 * (select
                avg(ratio_to_median_purchase_price)
                from ct
                where fraud = 0)
""" 
df_8 = sq(query_8)
df_8



"""
# 9.-
Encuentra el valor de la columna `Repeat_retailer` que tiene el mayor 
porcentaje de transacciones fraudulentas en relación con el total de 
transacciones para cada valor de la columna `Repeat_retailer`, 
considerando solo las transacciones que se realizaron con un pedido 
en línea (`Online_order = 1`) y que utilizaron un chip (`Used_chip = 1`). 
Además, muestra el porcentaje de transacciones fraudulentas para ese valor 
de `Repeat_retailer` y el total de transacciones para ese valor.
"""

query_9 = """
with retailer as(
        select
        repeat_retailer,
        count(*) as transacciones_repeat_retailer
        from ct
        where fraud = 1
        group by repeat_retailer
        ) 
select
t.repeat_retailer,
transacciones_repeat_retailer,
1.0 * sum(case when t.fraud = 1 and t.online_order = 1 and used_chip = 1 then 1 end) /
r.transacciones_repeat_retailer as porcentaje
from ct  t
join retailer r on t.repeat_retailer = r.repeat_retailer
group by t.repeat_retailer
""" 
df_9 = sq(query_9)
df_9


"""
# 11.-
Encuentra el valor de la columna `Repeat_retailer` que tiene el mayor 
número de transacciones con fraude (`Fraud = 1`) en relación con el 
total de transacciones para ese valor de `Repeat_retailer`, considerando 
solo las transacciones que se realizaron con un pedido en línea 
(`Online_order = 1`) y que utilizaron un chip (`Used_chip = 1`).
"""

query_11 = """
select
repeat_retailer,
1.0 * sum(case when fraud = 1 then 1 end) / count(*) as relacion
from ct
where online_order = 1 and used_chip = 1
group by repeat_retailer
""" 
df_11 = sq(query_11)
df_11



"""
# 13.-
Encuentra los 5 retailers más comunes en las transacciones fraudulentas 
que involucran compras en línea y utilizan la autenticación por PIN. 
Para cada retailer, calcula el número total de transacciones, el 
número de transacciones fraudulentas y el porcentaje de transacciones 
fraudulentas. Ordena los resultados por el porcentaje de transacciones 
fraudulentas en orden descendente.
"""

query_13 = """
select
repeat_retailer,
sum(case when fraud = 1 then 1 end) as transacciones_fraudulentas,
1.0 * sum(case when fraud = 1 then 1 end) /  count(*) as porcentaje
from ct
where online_order = 1 and used_pin_number = 1
group by repeat_retailer
order by  transacciones_fraudulentas
limit 5;
""" 
df_13 = sq(query_13)
df_13



"""
##############################################################################

##############################################################################
"""



"""
# 2.-
Crea un ranking de los 5 retailers más frecuentes en casos de fraude 
(`Fraud = 1`) y no fraude (`Fraud = 0`) por separado, considerando 
solo las transacciones que involucran compras en línea 
(`Online_order = 1`). Utiliza la columna `Repeat_retailer` 
para identificar a los retailers.

Requisitos adicionales
- Utiliza una ventana para calcular el ranking.
- Muestra los resultados en dos tablas separadas: una para casos de fraude y otra para casos de no fraude.
- Incluye las siguientes columnas en cada tabla:
- `Repeat_retailer`
- `Frecuencia` (número de transacciones)
- `Ranking`
"""

query_2 = """
with fraude_no as(
        select
        repeat_retailer,
        count(*) as frecuencia_no,
        rank() over(order by count(*) desc) as rank_transa_no_fraud
        from ct
        where fraud = 0
        group by repeat_retailer
        ),
     fraude_si as(
       select
       repeat_retailer,
       count(*) as frecuencia_si,
       rank() over(order by count(*) desc) as rank_transa_si_fraud
       from ct
       where fraud = 1
       group by repeat_retailer
       )
select
s.repeat_retailer,
n.frecuencia_no,
s.frecuencia_si,
n.rank_transa_no_fraud,
s.rank_transa_si_fraud
from fraude_no as n
join fraude_si as s on n.repeat_retailer = s.repeat_retailer
""" 
df_2 = sq(query_2)
df_2




"""
# 4.-
Encuentra los minoristas (`Repeat_retailer`) que tienen una tasa de fraude
(`Fraud = 1`) mayor que la tasa de fraude promedio de todos los minoristas. 
Considera solo las transacciones que involucran compras en línea 
(`Online_order = 1`).

Requisitos adicionales
- Utiliza una subconsulta para calcular la tasa de fraude promedio de 
todos los minoristas.

- Muestra los resultados en una tabla con las siguientes columnas:
- `Repeat_retailer`
- `Tasa_de_fraude`
- `Tasa_de_fraude_promedio`
"""

query_4 = """
with minorista as(
        select
        repeat_retailer,
        1.0 * sum(case when fraud = 1 and online_order =1  then 1 end) /
        (select count(*) from ct where fraud = 1) as tasa_fraude
        from ct
        group by repeat_retailer
        )
select
c.repeat_retailer,
m.tasa_fraude,
(select avg(tasa_fraude) from minorista) as tasa_fraude_promedio
from ct  c
join minorista m on c.repeat_retailer = m.repeat_retailer
where m.tasa_fraude > (select avg(tasa_fraude) from minorista)
group by c.repeat_retailer
""" 
df_4 = sq(query_4)
df_4




















