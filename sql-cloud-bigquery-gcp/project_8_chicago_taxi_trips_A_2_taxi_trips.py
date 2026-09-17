# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:47:02 2024

@author: Juan Pablo Aguirre
"""


import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("chicago_taxi_trips", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("taxi_trips")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=1000).to_dataframe()      

"""
# it's me
# the follows querys are me, from data
# https://www.kaggle.com/code/cesardushimimana/chicago-taxi-trips-analysis-project
"""

from google.cloud import bigquery
from time import time

client = bigquery.Client()

def show_amount_of_data_scanned(query):
    # dry_run lets us see how much data the query uses without running it
    dry_run_config = bigquery.QueryJobConfig(dry_run=True)
    query_job = client.query(query, job_config=dry_run_config)
    print('Data processed: {} GB'.format(round(query_job.total_bytes_processed / 10**9, 3)))
    
def show_time_to_run(query):
    time_config = bigquery.QueryJobConfig(use_query_cache=False)
    start = time()
    query_result = client.query(query, job_config=time_config).result()
    end = time()
    print('Time to run: {} seconds'.format(round(end-start, 3)))



# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()


"""
#########---- table: taxi_trips -----########
"""


# english pod 17
# https://www.youtube.com/watch?v=S09L4zoEgeU

"""
# 1.- 
¿ cual es el dia de la semana en el que se realizaron
más viajes en taxi en la ciudad de Chicago en el año 2019 ?
"""

# tabla_1.columns

query_01 = """
with day_week as(
        select        
        format_date('%u', trip_start_timestamp) as dia_semana,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019
        group by dia_semana
        )
select
*
from day_week
order by viajes desc
"""
df_query_01 = sq(query_01)
df_query_01


"""
# 2.- 
¿ cuál es el porcentaje de viajes en  taxi  que se realizaron en cada 
una de las 5 areas más concurridas de la ciudad de chicago en el año 
2019 ?
"""

query_02 = """
with comunidad as(
        select        
        pickup_community_area as comuna,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019 and
              pickup_community_area is not null
        group by comuna
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
          where extract(year from trip_start_timestamp) = 2019
          )
select
*,
row_number() over(order by viajes desc) as ranking,
(viajes/ (select total from total_viajes)) * 100 as porcentaje
from comunidad
limit 5;
"""
df_query_02 = sq(query_02)
df_query_02




"""
# 3.- 
cuales son los detalles de los viajes en taxi que se realizaron
en las areas con mas de 1000 viajes 
"""

query_03 = """
select
*
from bigquery-public-data.chicago_taxi_trips.taxi_trips
where pickup_community_area in (
    select
    pickup_community_area
    from bigquery-public-data.chicago_taxi_trips.taxi_trips
    where extract(year from trip_start_timestamp) = 2019
    group by pickup_community_area
    having count(*) > 1000
    )
and extract(year from trip_start_timestamp) = 2019;
"""
df_query_03 = sq(query_03)
df_query_03



query_03_b = """
with areas_comunes as(
        select
        pickup_community_area
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019
        group by pickup_community_area
        having count(*) > 1000
        )
select
t.pickup_community_area,
t.trip_start_timestamp
from bigquery-public-data.chicago_taxi_trips.taxi_trips as t
inner join areas_comunes on t.pickup_community_area = areas_comunes.pickup_community_area
where extract(year from t.trip_start_timestamp) = 2019;
"""
df_query_03_b = sq(query_03_b)
df_query_03_b



tabla_1.columns

"""
# 4.- 
¿Cuáles son los 10 community areas de Chicago con mayor probabilidad de 
tener un viaje en taxi con un pago en efectivo durante el año 2019, 
considerando solo los viajes que tuvieron un pago total mayor a $20?
"""

query_04 = """
with comunidad as(
        select        
        pickup_community_area as comuna,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019 and
              pickup_community_area is not null
              and fare > 20
        group by comuna
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
          where extract(year from trip_start_timestamp) = 2019
          )
select
*,
row_number() over(order by viajes desc) as ranking,
(viajes/ (select total from total_viajes)) * 100 as porcentaje
from comunidad
limit 10;
"""
df_query_04 = sq(query_04)
df_query_04



"""
# 5.- 
¿Cuál es la hora del día en la que se realizan más viajes en taxi en Chicago 
durante el año 2019, y qué porcentaje de los viajes totales se realizan 
durante esa hora?
"""

# tabla_1.columns

query_05 = """
with comunidad as(
        select        
        extract(hour from trip_start_timestamp) as hora,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019
        group by hora
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
          where extract(year from trip_start_timestamp) = 2019
          )
select
*,
row_number() over(order by viajes desc) as ranking,
(viajes/ (select total from total_viajes)) * 100 as porcentaje
from comunidad
limit 1;
"""
df_query_05 = sq(query_05)
df_query_05



query_05_a = """
with comunidad as(
        select        
        extract(hour from trip_start_timestamp) as hora_num,
        format_timestamp("%I:%M %p", trip_start_timestamp) as hora,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019
        group by hora_num, hora
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
          where extract(year from trip_start_timestamp) = 2019
          )
select
hora,
viajes,
row_number() over(order by viajes desc) as ranking,
(viajes/ (select total from total_viajes)) * 100 as porcentaje
from comunidad
"""
df_query_05_a = sq(query_05_a)
df_query_05_a



"""
# 6.- 
¿Cuál es el porcentaje de viajes de taxi que se realizan en la ciudad de 
Chicago durante las horas pico (7am-9am y 4pm-6pm) en comparación con el 
resto del día, considerando solo los viajes que se realizan en el año 2019 
y que tienen una tarifa mayor a $20?
"""

# tabla_1.columns

query_06 = """
with lapso_cerrado as(
        select        
        count(*) as viajes_cerrado
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where (extract(hour from trip_start_timestamp) between 7 and 9) or
              (extract(hour from trip_start_timestamp) between 16 and 18) and
              fare > 20 
              
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
          where extract(year from trip_start_timestamp) = 2019 and
                fare > 20 
          ),
      lapso_abierto as (
      select
      *,
      (viajes_cerrado/ (select total from total_viajes)) /3600 as porcentaje_cerrado
      from lapso_cerrado
      )
select
porcentaje_cerrado,
(1 - porcentaje_cerrado) as  porcentaje_abierto
from lapso_abierto
"""
df_query_06 = sq(query_06)
df_query_06


tabla_1.columns

"""
# 7.- 
¿Cuáles son los 5 aeropuertos con mayor cantidad de viajes en taxi en Chicago, 
y qué porcentaje del total de viajes representan?
"""

# tabla_1.columns

query_07 = """
with aero as (
        select
        pickup_location,
        count(*) as viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        group by pickup_location
        ),
      total_viajes as(
          select
          count(*) as total,
          from bigquery-public-data.chicago_taxi_trips.taxi_trips
         )
select
*,
row_number() over(order by viajes desc) as ranking,
(viajes/ (select total from total_viajes)) * 100 as porcentaje
from aero
limit 5;
"""
df_query_07 = sq(query_07)
df_query_07









