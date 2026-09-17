# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 08:22:23 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# https://www.kaggle.com/datasets/kanchana1990/uber-customer-reviews-dataset-2024

# UBER EATS
# https://www.kaggle.com/datasets/thedevastator/the-ubereats-restaurant-dataset-over-100000-us-r


# Uber Fares Dataset
# https://www.kaggle.com/datasets/yasserh/uber-fares-dataset

# Uber ride price
# https://www.kaggle.com/datasets/kushsheth/uber-ride-price-prediction

# Uber and Lyft Dataset Boston, MA
# https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma

con = sqlite3.connect('db_uber.db')

# df = pd.read_csv('uber.csv')
# dff = pd.read_csv('ubereat.csv')
# dfff = pd.read_csv('uberfares.csv')
dfiv = pd.read_csv('uber_ride_price.csv')
# dfv = pd.read_csv('rideshare.csv')


"""
df.to_sql('uber', con, if_exists='replace', index=False)
dff.to_sql('ubereat', con, if_exists='replace', index=False)
dfff.to_sql('uberfares', con, if_exists='replace', index=False)
dfiv.to_sql('uber_ride_price', con, if_exists='replace', index=False)
dfv.to_sql('rideshare', con, if_exists='replace', index=False)
"""
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
Calcula el precio promedio de los viajes de Uber en Nueva York durante las 
horas pico (7-9 am y 4-6 pm) para cada día de la semana, considerando solo 
los viajes que se realizaron con un número de pasajeros mayor a 2.
"""

query_1 = """
with -- Subconsulta para obtener los viajes realizados durante las horas pico
     viajes_hora_pico as(
         select
         fare_amount,
         passenger_count,
         strftime('%w', substr(pickup_datetime, 1, 19)) AS dia_semana,
         strftime('%H', substr(pickup_datetime, 1, 19)) AS hora
         from uber_ride_price
         where (strftime('%H', substr(pickup_datetime, 1, 19))>= 7  and 
                strftime('%H', substr(pickup_datetime, 1, 19)) <= 9) or
               (strftime('%H', substr(pickup_datetime, 1, 19))>= 16  and 
                      strftime('%H', substr(pickup_datetime, 1, 19)) <= 18) 
               and passenger_count > 2
         )
-- Consulta principal para calcular el precio promedio por día de la semana
select
dia_semana,
avg(fare_amount) as precio_promedio
from viajes_hora_pico
group by dia_semana
order by dia_semana, precio_promedio
"""
df_1 = sq(query_1)
df_1





"""
# 2.-
Calcula el top 10 de los conductores de Uber que han realizado 
la mayor cantidad de viajes en Nueva York durante el año 2019, 
considerando solo los viajes que se realizaron con un número 
de pasajeros mayor a 1 y un precio mayor a $10. Además, 
calcula el porcentaje de viajes que cada conductor ha 
realizado en relación con el total de viajes realizados 
en Nueva York durante el año 2019. Ordénalos por el número 
de viajes descendente y, en caso de empate, ordénalos por 
el porcentaje de viajes ascendente
"""

query_2 = """
with viajes_realizados as(
        select
        *
        from uber_ride_price
        where strftime('%Y', substr(pickup_datetime, 1, 19)) = '2010'
        and passenger_count > 1 and
            fare_amount > 10
        ),
      conductores_viajes as(
          select
          key,
          count(*) as num_viajes
          from viajes_realizados
          group by key
          ),
      conductores_porcentajes as(
          select
          key,
          num_viajes,
          (num_viajes * 100 / (select count(*) from conductores_viajes)) as porcentaje_viajes
          from conductores_viajes
          ),
      top_conductores as(
          select
          key,
          num_viajes,
          porcentaje_viajes,
          rank() over(order by num_viajes desc, porcentaje_viajes asc) as rank
          from conductores_porcentajes
          )
select
key,
num_viajes,
porcentaje_viajes
from top_conductores
where rank < 10
"""
df_2 = sq(query_2)
df_2




"""
# 3.-
Calcula el promedio de la tarifa (Fare_amount) para cada 
hora del día, considerando solo los viajes que se 
realizaron en el año 2019. Ordena los resultados por 
hora del día.
"""

query_3 = """
select
strftime('%H', substr(pickup_datetime, 1, 19)) as hora ,
avg(fare_amount) as media_tarifas
from uber_ride_price
where strftime('%Y', substr(pickup_datetime, 1, 19)) = '2019'
group by hora
order by hora 
"""
df_3 = sq(query_3)
df_3







