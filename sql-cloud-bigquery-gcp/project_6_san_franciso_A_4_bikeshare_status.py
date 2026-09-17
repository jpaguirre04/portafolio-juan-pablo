# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:14:33 2024

@author: Juan Pablo Aguirre
"""

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("san_francisco", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("bikeshare_status")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=10).to_dataframe()      

"""
# it's me
# the follows querys are me, from data
# https://www.kaggle.com/datasets/datasf/san-francisco
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
#########---- table: bikeshare_status -----########
"""


"""
# 1.- 

La empresa de bicicletas compartidas quiere analizar el estado de sus 
estaciones y bicicletas. Necesitan:

1. Las 5 estaciones con mayor cantidad de bicicletas disponibles en promedio 
durante los últimos 30 días.
2. El porcentaje de bicicletas disponibles en cada estación respecto al 
total de bicicletas en la empresa.
3. La cantidad de estaciones con menos de 5 bicicletas disponibles en 
promedio durante los últimos 30 días.
4. El promedio de bicicletas disponibles por día de la semana 
(lunes a domingo).
"""

query_01 = """
with   -- Promedio de bicicletas disponibles por estación en los últimos 30 días  
         promedio_bicicletas_estacion as(
         select     
         station_id,     
         avg(bikes_available) as promedio_bicicletas    
         from bigquery-public-data.san_francisco.bikeshare_status
         where time <= timestamp_sub(current_timestamp, interval 30 day)
         group by station_id
        ),
        -- Total de bicicletas en la empresa
        total_bicicletas as (
           select
             sum(bikes_available) as total
             from bigquery-public-data.san_francisco.bikeshare_status
             where time <= timestamp_sub(current_timestamp, interval 30 day)
            ),
        -- Promedio de bicicletas disponibles por día de la semana
        promedio_bicicletas_dia_semana as(
        select
        station_id,
        extract(dayofweek from time) as dia_semana,
        avg(bikes_available) as promedio_bicicletas
        from bigquery-public-data.san_francisco.bikeshare_status
        where time <= timestamp_sub(current_timestamp, interval 30 day)
        group by station_id, extract(dayofweek from time)
        )
select
-- 5 estaciones con mayor cantidad de bicicletas disponibles en promedio
pb.station_id,
pb.promedio_bicicletas,
-- Porcentaje de bicicletas disponibles en cada estación respecto al total
round((pb.promedio_bicicletas / tb.total)*100, 2) as porcentaje_bicicletas
from promedio_bicicletas_estacion pb
inner join total_bicicletas tb on 1=1
left join promedio_bicicletas_dia_semana pbs ON pb.station_id = pbs.station_id
order by 
pb.promedio_bicicletas desc
"""
df_query_01 = sq(query_01)
df_query_01



"""
Obtener el promedio diario de bicicletas disponibles por estación en las 
últimas 30 días, ordenado por estación con mayor disponibilidad.
"""

query_02 = """
select
station_id,
avg(bikes_available) as promedio_bicicletas
from bigquery-public-data.san_francisco.bikeshare_status
where time <= timestamp_sub(current_timestamp, interval 30 day)
group by station_id
order by promedio_bicicletas desc
 """
df_query_02 = sq(query_02)
df_query_02



"""
Consulta: Obtener las estaciones con mayor variabilidad en la disponibilidad 
de bicicletas durante las últimas 24 horas, considerando solo estaciones con 
más de 5 docks disponibles. Calcula:

1. Promedio de bicicletas disponibles.
2. Desviación estándar de bicicletas disponibles.
3. Porcentaje de ocupación de docks.
"""

tabla_1.columns


# lo haré de dos formas


query_03_a = """
WITH 
  -- Filtrar últimas 24 horas y más de 5 docks disponibles
  filtro AS (
    SELECT 
      station_id,
      bikes_available,
      docks_available,
      time
    FROM 
      bigquery-public-data.san_francisco.bikeshare_status
    WHERE 
      time <= TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 24 HOUR)
      AND docks_available > 5
  ),
  
  -- Calcular promedio y desviación estándar de bicicletas disponibles
  estadisticas AS (
    SELECT 
      station_id,
      AVG(bikes_available) AS promedio_bicicletas,
      stddev(bikes_available) AS desviacion_estandar,
      AVG(docks_available) AS promedio_docks
    FROM 
      filtro
    GROUP BY 
      station_id
  )
SELECT 
  station_id,
  promedio_bicicletas,
  desviacion_estandar,
  -- Porcentaje de ocupación de docks
  ROUND((promedio_bicicletas / promedio_docks) * 100, 2) AS porcentaje_ocupacion
FROM 
  estadisticas
ORDER BY 
  desviacion_estandar DESC;
"""
df_query_03_a = sq(query_03_a)
df_query_03_a




# sucinta
query_03_b = """
with  -- filtrar ultimas 24 horas y mas de 5 docks disponibles  
        estadistica as(
        select        
        station_id,
        avg(bikes_available) as promedio_bikes,
        stddev(bikes_available) as desviacion_bikes,
        avg(docks_available) as promedio_docks
        from bigquery-public-data.san_francisco.bikeshare_status
        where time <= timestamp_sub(current_timestamp, interval 24 hour)
        and docks_available > 5
        group by station_id
        )
select
station_id,
promedio_bikes,
promedio_docks,
round((promedio_bikes / promedio_docks) *100)/2 as porcentaje_ocupacion
from estadistica
order by desviacion_bikes desc
"""
df_query_03_b = sq(query_03_b)
df_query_03_b



"""
Consulta: Obtener las estaciones con mayor demanda de bicicletas durante las 
horas pico (7:00 AM - 9:00 AM y 4:00 PM - 6:00 PM) en los últimos 7 días, 
considerando solo estaciones con más de 10 docks disponibles. Calcula:

1. Promedio de bicicletas disponibles durante horas pico.
2. Promedio de bicicletas disponibles fuera de horas pico.
3. Diferencia porcentual entre horas pico y fuera de horas pico.


Pista:

- Utiliza funciones de agregación (AVG, COUNT).
- Utiliza JOIN para combinar resultados.
- Utiliza cálculos aritméticos para el porcentaje de diferencia.
- Utiliza TIMESTAMP_SUB y INTERVAL para definir lapsos de tiempo.
- Utiliza CASE o IF para distinguir horas pico y fuera de horas pico.
"""



query_04_a = """
with   -- obtener última fecha en la base de datos
          ultima_fecha as(
           select
           max(time) as ultima_fecha
           from bigquery-public-data.san_francisco.bikeshare_status
          ),
       -- filtrar últimos 7 dias respecto a la última fecha
       filtro as(
           select
           station_id,
           bikes_available,
           docks_available,
           time
           from bigquery-public-data.san_francisco.bikeshare_status
           where time >= timestamp_sub((select ultima_fecha.ultima_fecha from ultima_fecha), interval 7 day)
           order by time desc
           )
select
*
from filtro
"""
df_query_04_a = sq(query_04_a)
df_query_04_a




query_04_b = """
with   -- obtener última fecha en la base de datos
          ultima_fecha as(
           select
           max(time) as ultima_fecha
           from bigquery-public-data.san_francisco.bikeshare_status
          ),
       -- filtrar últimos 7 dias respecto a la última fecha
       filtro as(
           select
           station_id,
           bikes_available,
           docks_available,
           time
           from bigquery-public-data.san_francisco.bikeshare_status
           where time >= timestamp_sub((select max(time) from bigquery-public-data.san_francisco.bikeshare_status), interval 7 day)
           order by time desc
           )
select
*
from filtro
"""
df_query_04_b = sq(query_04_b)
df_query_04_b



query_04 = """
with   -- obtener última fecha en la base de datos
          ultima_fecha as(
           select
           max(time) as ultima_fecha
           from bigquery-public-data.san_francisco.bikeshare_status
          ),
       -- filtrar últimos 7 dias respecto a la última fecha
       filtro as(
           select
           station_id,
           bikes_available,
           docks_available,
           time
           from bigquery-public-data.san_francisco.bikeshare_status
           where time >= timestamp_sub((select max(time) from bigquery-public-data.san_francisco.bikeshare_status), interval 7 day)
           order by time desc
           ),
       -- calcular promedio bicicletas disponibles durante horas peak
       horas_peak as (
           select
           station_id,
           avg(case when extract(hour from time) between 7 and 9 or 
                         extract(hour from time) between 16 and 18
                         then bikes_available else null end) as promedio_horas_peak
           from filtro
           group by station_id
           ),
       -- Calcular promedio bicicletas disponibles fuera de horas pico
         fuera_horas_peak as(
           select
           station_id,
           avg(case when extract(hour from time) not between 7 and 9 and 
                         extract(hour from time) not between 16 and 18
                         then bikes_available else null end) as promedio_fuera_horas_peak
           from filtro
           group by station_id
           ),
       -- Unir resultados y calcular diferencia porcentual  
       resultado as(
           select
           h.station_id,
           h.promedio_horas_peak,
           f.promedio_fuera_horas_peak,
           round((h.promedio_horas_peak - f.promedio_fuera_horas_peak)/ 
                 f.promedio_fuera_horas_peak * 100, 2) as diferencia_porcentual
           from horas_peak h
           join fuera_horas_peak as f 
           on h.station_id = f.station_id
           )
select
re.station_id,
avg(re.promedio_horas_peak) as promedio_horas_peak,
avg(re.promedio_fuera_horas_peak) as promedio_fuera_horas_peak,
avg(re.diferencia_porcentual) as diferencia_porcentual
from resultado re
inner join filtro as ft 
on re.station_id = ft.station_id
where re.promedio_horas_peak is not null
      and re.promedio_fuera_horas_peak is not null
      and ft.docks_available > 10
group by re.station_id      
order by diferencia_porcentual desc
"""
df_query_04 = sq(query_04)
df_query_04

