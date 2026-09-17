# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 16:01:48 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit_card_fraud_dataset
# https://www.kaggle.com/datasets/bhadramohit/credit-card-fraud-detection?select=credit_card_fraud_dataset.csv

con = sqlite3.connect('db_ccfd.db')
df1 = pd.read_csv('ccfd.csv')

df1.to_sql('ccfd', con, if_exists='replace', index=False)

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
from ccfd
"""
df_0 = sq(query_0)
# df_0.columns


"""
# 01.-
Encuentra los 5 comerciantes (`Merchantid`) que tienen la mayor cantidad 
de transacciones fraudulentas (`Isfraud = 1`) y calcula el monto total 
de estas transacciones para cada comerciante. Muestra los resultados 
en una tabla con las siguientes columnas:
- `Merchantid`
- `Cantidad_de_transacciones_fraudulentas`
- `Monto_total`

"""

query_01 = """
select
merchantid,
count(*) as  cantidad_transacciones_fraudulentas,
sum(amount) as monto_total
from ccfd
where isfraud = 1  
group by merchantid
order by count(*)
""" 
df_01 = sq(query_01)
df_01



"""
# 02.-
Encuentra los comerciantes (`Merchantid`) que tienen una tasa de 
fraude (`Isfraud = 1`) superior a la media global de fraude en 
todas las transacciones. Muestra los resultados en una tabla con 
las siguientes columnas:

- `Merchantid`
- `Tasa_de_fraude`
- `Media_global_de_fraude`
"""

query_02 = """
with merchant as(
        select
        merchantid,
        sum(case when isfraud = 1 then 1 else 0 end) *1.0 / count(*) as tasa
        from ccfd
        group by merchantid
        )
select
merchantid,
tasa,
(select count(*) from ccfd where isfraud = 1) * 1.0 / (select count(*) from ccfd) as 
media_global_fraude
from merchant 
where tasa > (select count(*) from ccfd where isfraud = 1) * 1.0 / (select count(*) from ccfd)
""" 
df_02 = sq(query_02)
df_02



"""
# 03.-
Encuentra los 3 días del mes con mayor cantidad de transacciones 
fraudulentas (`Isfraud = 1`) y muestra la cantidad de transacciones 
fraudulentas para cada día. Muestra los resultados en una tabla con 
las siguientes columnas:
"""

query_03 = """
select
substr(transactiondate, 9, 2)  as dia_del_mes,
count(*) as cantidad_transacciones_fraudulentas
from ccfd
where isfraud = 1
group by dia_del_mes
order by count(*)  desc
limit 3;
""" 
df_03 = sq(query_03)
df_03



"""
# 04.-
Encuentra los comerciantes (`Merchantid`) que tienen una tasa de fraude 
(`Isfraud = 1`) superior a la media global de fraude en todas las 
transacciones, pero solo para los comerciantes que tienen más de 100 
transacciones en total. Muestra los resultados en una tabla con las
siguientes columnas:
"""

query_04 = """
with merchant as(
        select
        merchantid,
        sum(case when isfraud = 1 then 1 else 0 end) *1.0 / count(*) as tasa,
        count(*) as total_transacciones
        from ccfd
        group by merchantid
        having count(*) > 100
        )
select
merchantid,
tasa,
(select count(*) from ccfd where isfraud = 1) * 1.0 / (select count(*) from ccfd) as 
media_global_fraude,
total_transacciones
from merchant 
where tasa > (select count(*) from ccfd where isfraud = 1) * 1.0 / (select count(*) from ccfd)
""" 
df_04 = sq(query_04)
df_04



"""
# 05.-
Encuentra los 5 pares de comerciantes (`Merchantid`) que tienen la mayor 
cantidad de transacciones en común (es decir, transacciones que se realizaron 
en ambos comercios). Muestra los resultados en una tabla con las siguientes 
columnas:

- `Merchantid1`
- `Merchantid2`
- `Cantidad_de_transacciones_en_común`
"""

query_05 = """
with merchant as(
        select
        merchantid,
        transactionid
        from ccfd
        )
select
m1.merchantid,
m2.merchantid,
count(*) as cantidad_transacciones_en_comun
from merchant as m1
join merchant as m2 on m1.merchantid > m2.merchantid
                      and m1.transactionid = m2.transactionid
group by m1.merchantid, m2.merchantid                       
order by count(*) desc
limit 5;
""" 
df_05 = sq(query_05)
df_05




"""
# 06.-
Encuentra los comerciantes (`Merchantid`) que tienen una tendencia 
creciente en la cantidad de transacciones fraudulentas (`Isfraud = 1`) 
a lo largo del tiempo. Muestra los resultados en una tabla con las 
siguientes columnas:

- `Merchantid`
- `Tendencia` (1 si la tendencia es creciente, 0 si no)
"""

query_06 = """
with tendencia as(
        select
        merchantid,
        substr(transactiondate, 7, 1) as mes,
        count(*) as transacciones_fraudulentas
        from ccfd
        where isfraud = 1
        group by merchantid, mes
        )
select
*,
case 
     when 
     transacciones_fraudulentas > lag(transacciones_fraudulentas) over(partition by merchantid order by mes)
     then 1
     else 0
end as tendencia_creciente
from tendencia
""" 
df_06 = sq(query_06)
df_06



"""
############################################################
############################################################
"""

"""
# 2.-
Encuentra las 5 ubicaciones (Location) con mayor cantidad de transacciones 
fraudulentas (Isfraud = 1) que también tengan un monto promedio de 
transacciones mayor que el monto promedio general de todas las
transacciones en la tabla `credit_card_fraud_dataset`. Ordena los 
resultados por la cantidad de transacciones fraudulentas en orden 
descendente.
"""

query_2 = """
with media as(
        select
        location,
        count(*) as cantidad_transacciones_fraudulentas,
        avg(amount) as media
        from ccfd
        group by location
        )
select
location,
cantidad_transacciones_fraudulentas
from media
where media > (select avg(amount) from ccfd)
group by location
order by cantidad_transacciones_fraudulentas desc
limit 5;
""" 
df_2 = sq(query_2)
df_2




"""
# 4.-
Encuentra las ubicaciones (Location) que tienen más de 10 transacciones 
fraudulentas (Isfraud = 1) y que también tienen un monto total de 
transacciones mayor que el monto total de transacciones de la 
ubicación con menor monto total.
"""

query_4_a = """
with total_por_ubicacion as(
        select
        location,
        sum(amount) as total_amount
        from ccfd
        where isfraud = 1
        group by location
        ),
     ubicacion_por_menor_monto as(
         select
         location,
         min(amount) min_amount
         from ccfd
         ),
     transacciones_fraudulentas_porubicacion as(
         select
         location,
         count(*) as cantidad_transacciones_fraudulentas
         from ccfd
         where isfraud = 1
         group by location
         )
select
t1.location
from transacciones_fraudulentas_porubicacion as t1
join total_por_ubicacion as t2 on t1.location = t2.location
where t1.cantidad_transacciones_fraudulentas > 10 and 
t2.total_amount > (select min_amount from ubicacion_por_menor_monto) 
""" 
df_4_a = sq(query_4_a)
df_4_a





"""
# 5.-
Encuentra las 3 ubicaciones (Location) con mayor cantidad de transacciones 
no fraudulentas (IsFraud = 0) que también tengan un monto promedio de 
transacciones no fraudulentas mayor que el monto promedio general de 
todas las transacciones no fraudulentas.
"""

query_5 = """
with ubicaciones as(
        select
        location,
        count(*) as transacciones_no_fraudulentas,
        avg(amount) as monto_promedio
        from ccfd
        where isfraud = 0
        group by location
        )
select
location
from ubicaciones        
where monto_promedio > (select
                        avg(amount)
                        from ccfd
                        where isfraud = 0
                        )
order by transacciones_no_fraudulentas desc
limit 3;
""" 
df_5 = sq(query_5)
df_5





"""
# 6.-
Encuentra las ubicaciones (Location) que tienen un monto total de 
transacciones fraudulentas (IsFraud = 1) mayor que el monto total 
de transacciones no fraudulentas (IsFraud = 0).
"""

query_6 = """
with locacion as(
        select
        location,
        sum(amount) as monto_fraudulento_por_locacion
        from ccfd
        where isfraud = 1
        group by location
        )
select
location
from locacion
where monto_fraudulento_por_locacion > (select
                                        sum(amount)
                                        from ccfd
                                        where isfraud = 0
                                        )                               
""" 
df_6 = sq(query_6)
df_6



"""
# 7.-
Encuentra las 5 ubicaciones (Location) con mayor cantidad de 
transacciones (independientemente de si son fraudulentas o no) 
que también tengan un monto promedio de transacciones mayor que 
el monto promedio general de todas las transacciones.
"""

query_7 = """
with locacion as(
        select
        location,
        count(*) as transacciones,
        avg(amount) as promedio_montos
        from ccfd
        group by location
        )
select
location
from locacion
where promedio_montos > (select
                         avg(amount)
                         from ccfd)
order by transacciones desc
limit 5;
""" 
df_7 = sq(query_7)
df_7



"""
# 8.-
Encuentra las ubicaciones (Location) que tienen al menos 2 transacciones 
fraudulentas (IsFraud = 1) en un mismo día (Date).
"""

query_8 = """
select
location,
transactiondate
from ccfd
where isfraud = 1
group by location
having count(*) >= 2
""" 
df_8 = sq(query_8)
df_8



"""
# 12.-
Encuentra las transacciones que tienen un monto (Amount) superior al promedio 
de los montos de las transacciones realizadas en la misma ubicación (Location) 
y en el mismo tipo de transacción (TransactionType).
"""

query_12 = """
with transacciones as(
        select
        location,
        transactionid,
        avg(amount) as monto_medio
        from ccfd
        group by location, transactionid
        )
select
c.transactionid
from ccfd as c
join transacciones as t on c.transactionid = t.transactionid 
and c.location = t.location
where c.amount > (select monto_medio from transacciones)
""" 
df_12 = sq(query_12)
df_12


"""
# 13.-
Encuentra las ubicaciones (Location) que tienen un número de transacciones 
(TransactionID) que es mayor que el promedio de transacciones por ubicación.
"""

query_13 = """
with locacion as(
        select
        location,
        count(distinct transactionid) as transacciones
        from ccfd
        group by location
        )
select
c.location
from ccfd c
join locacion l on c.location = l.location
group by c.location
having count(*) > (select avg(transacciones) from locacion)
""" 
df_13 = sq(query_13)
df_13



"""
# 14.-
Encuentra los tipos de transacciones (TransactionType) que tienen un monto 
total (Amount) que es mayor que el 50% del monto total de todas las 
transacciones.
"""

query_14 = """
with tipo_transacciones as(
        select
        transactiontype,
        sum(amount) as suma_transacciones
        from ccfd
        group by transactiontype
        )
select
c.transactiontype
from ccfd as c
join tipo_transacciones as t on c.transactiontype = t.transactiontype
where t.suma_transacciones > 0.5 * (select sum(amount) from ccfd)
group by c.transactiontype
""" 
df_14 = sq(query_14)
df_14


query_14_a = """
select
transactiontype
from ccfd
group by transactiontype
having sum(amount) > 0.5 * (select sum(amount) from ccfd)
""" 
df_14_a = sq(query_14_a)
df_14_a



"""
# 15.-
Encuentra el tipo de transacción (TransactionType) con mayor monto total 
(Amount) en cada ubicación (Location), considerando solo las transacciones 
que tienen un monto mayor que el promedio de transacciones en esa ubicación. 
Además, calcula el porcentaje del monto total de este tipo de transacción 
con respecto al monto total de todas las transacciones en esa ubicación.
"""

query_15 = """
with locacion as(
        select
        location,
        sum(amount) as monto_total,
        avg(amount) as monto_promedio
        from ccfd
        group by location
        )
select
c.transactiontype,
c.location,
(sum(amount) /l.monto_total) as porcentaje
from ccfd  c
join locacion as l on c.location = l.location
where c.amount > (select monto_promedio from locacion)
group by  c.location
""" 
df_15 = sq(query_15)
df_15



"""
# 16.-
Encuentra la ubicación (Location) con el mayor número de transacciones 
(TransactionID) que tienen un monto (Amount) mayor que el promedio de 
transacciones en todas las ubicaciones.
"""

query_16 = """
select
location,
count(distinct transactionid) as numero_transacciones
from ccfd
where amount > (select avg(amount) from ccfd)
group by location
""" 
df_16 = sq(query_16)
df_16









