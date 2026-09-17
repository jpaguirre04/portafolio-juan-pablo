# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

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
#########---- table: global_air_quality -----########
"""


# english pod 17
# https://www.youtube.com/watch?v=S09L4zoEgeU

"""
# 1.- 
¿Cuál es el mes del año con mayor cantidad de viajes en taxi en la ciudad 
de Chicago, considerando solo los años 2017 y 2018?
"""

tabla_1.columns

query_01 = """
with ranki as(
        select
        extract(year from trip_start_timestamp) as year,
        extract(month from trip_start_timestamp) as month,
        count(*) viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2017 or
              extract(year from trip_start_timestamp) = 2018
        group by year, month
        order by viajes desc
        )
select
*
from ranki
limit 1;
"""
df_query_01 = sq(query_01)
df_query_01



"""
# 2.- 
¿Cuál es el día de la semana con mayor cantidad de viajes en taxi en la 
ciudad de Chicago durante las horas pico (7am-9am y 4pm-6pm) en 
el año 2018?
"""


query_02 = """
with ranki as(
        select
        extract(dayofweek from trip_start_timestamp) as dia_semana,
        count(*) viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where (extract(hour from trip_start_timestamp) between 7 and 9) or
              (extract(hour from trip_start_timestamp) between 16 and 18) and
              extract(year from trip_start_timestamp) = 2018
       group by dia_semana
        order by viajes desc
        )
select
*
from ranki
limit 1;
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- 
¿Cuál es la compañía de taxi con mayor cantidad de viajes en la ciudad de 
Chicago en el año 2019?
"""


query_03 = """
with ranki as(
        select
        company,
        count(*) viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2019
        group by company
        order by viajes desc
        )
select
*
from ranki
limit 1;
"""
df_query_03 = sq(query_03)
df_query_03



"""
# 4.- 
¿Cuál es el día del mes con mayor cantidad de viajes en taxi en Chicago 
durante el año 2020, considerando solo los viajes que comenzaron entre las 
7am y 9am?
"""


query_04 = """
with ranki as(
        select
        extract(day from trip_start_timestamp) as dia_mes,
        count(*) viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where (extract(hour from trip_start_timestamp) between 7 and 9) and
              extract(year from trip_start_timestamp) = 2020
       group by dia_mes
        order by viajes desc
        )
select
*
from ranki
limit 1;
"""
df_query_04 = sq(query_04)
df_query_04




"""
# 5.- 
¿Cuál es la media  duración de los viajes en taxi en Chicago 
durante 2020? (Considera solo viajes con duración mayor a 0 minutos)
"""

tabla_1.columns

query_05 = """
with ranki as(
        select
        avg(timestamp_diff(trip_end_timestamp, trip_start_timestamp, minute))
        as mediana,
        count(*) viajes
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2020 and
              timestamp_diff(trip_end_timestamp, trip_start_timestamp, minute) > 0
        )
select
*
from ranki
"""
df_query_05 = sq(query_05)
df_query_05



 
"""
# 6.- 
¿Cuál es el porcentaje de viajes que superan la duración media de los viajes 
en taxi en Chicago durante 2020?

"""

query_06 = """
with ranki as(
        select
        timestamp_diff(trip_end_timestamp, trip_start_timestamp, minute) as lapso
        from bigquery-public-data.chicago_taxi_trips.taxi_trips
        where extract(year from trip_start_timestamp) = 2020 
        )
select
avg(lapso) media_viaje_2020
from ranki
"""
df_query_06 = sq(query_06)
df_query_06



"""
# 7.- 
¿Cuál es el porcentaje de viajes que superan la duración media de los viajes 
en taxi en Chicago durante 2020?
"""

query_07 = """
WITH 
  media_viaje AS (
    SELECT 
      AVG(TIMESTAMP_DIFF(trip_end_timestamp, trip_start_timestamp, MINUTE)) 
      AS media
    FROM 
      bigquery-public-data.chicago_taxi_trips.taxi_trips
    WHERE 
      EXTRACT(YEAR FROM trip_start_timestamp) = 2020
  ),
  viajes_superiores_media AS (
    SELECT 
      COUNT(*) AS viajes_superiores
    FROM 
      bigquery-public-data.chicago_taxi_trips.taxi_trips
    WHERE 
      EXTRACT(YEAR FROM trip_start_timestamp) = 2020 
      AND TIMESTAMP_DIFF(trip_end_timestamp, trip_start_timestamp, MINUTE) >
      (SELECT media FROM media_viaje)
  ),
  total_viajes AS (
    SELECT 
      COUNT(*) AS total
    FROM 
      bigquery-public-data.chicago_taxi_trips.taxi_trips
    WHERE 
      EXTRACT(YEAR FROM trip_start_timestamp) = 2020
  )

SELECT 
  (viajes_superiores / total) * 100 AS porcentaje
FROM 
  viajes_superiores_media, total_viajes
"""
df_query_07 = sq(query_07)
df_query_07


# https://www.collahuasi.cl/quienes-somos/nuestra-compania/


# practical in english
# https://padlet.com/monipenia01/interactive-classwork-level-b1-b2-hc2pe21uetjphkkc

# 25-11-2024
# https://padlet.com/monipenia01/alianza-interactive-classwork-a1-a2-8wczvw1i6ohbad6r