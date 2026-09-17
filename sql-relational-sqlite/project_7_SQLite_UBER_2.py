# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 17:08:56 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# Uber ride price
# https://www.kaggle.com/datasets/kushsheth/uber-ride-price-prediction

con = sqlite3.connect('db_uber.db')

dfiv = pd.read_csv('uber_ride_price.csv')

dfiv.to_sql('uber_ride_price', con, if_exists='replace', index=False)

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
from uber_ride_price
"""
df_0 = sq(query_0)
# df_0.columns

df_0.dtypes


"""
# 1.-
Calcula el top 10 de los conductores que han realizado más viajes 
en Nueva York durante el año 2019, considerando solo los viajes 
que se realizaron con un número de pasajeros mayor a 1 y un 
precio mayor a $10. Además, sólo considera los conductores que 
han realizado viajes con un promedio de tarifa (Fare_amount) 
mayor al promedio general de tarifa de todos los conductores. 
Finalmente, ordena los resultados por el número de viajes en 
orden descendente y muestra el promedio de tarifa para cada 
conductor.
"""

query_1 = """
with promedio_tarifa_general as(
        select
        avg(fare_amount) as promedio_tarifa
        from uber_ride_price
        where strftime('%Y', substr(pickup_datetime, 1, 19)) = '2010'
        and passenger_count > 1
        and fare_amount > 10        
        ),
     promedio_tarifa_conductores as(
         select
         key,
         avg(fare_amount) as promedio_tarifa_conductor
         from uber_ride_price
         where passenger_count> 1
               and fare_amount > 10
         group by key      
         )
select
t1.key,
count(*) as num_viajes,
t2.promedio_tarifa_conductor
from uber_ride_price t1
inner join promedio_tarifa_conductores t2 on t1.key = t2.key
inner join promedio_tarifa_general t3 
        on t2.promedio_tarifa_conductor > t3.promedio_tarifa
where t1.passenger_count > 1
      and t1.fare_amount > 10        
group by t1.key, t2.promedio_tarifa_conductor
order by num_viajes desc        
""" 
df_1 = sq(query_1)
df_1


###############################################################

