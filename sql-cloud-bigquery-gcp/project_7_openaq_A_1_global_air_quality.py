# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:10:37 2024

@author: Juan Pablo Aguirre
"""

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("openaq", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("global_air_quality")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=100).to_dataframe()      

"""
# it's me
# the follows querys are me, from data
# https://www.kaggle.com/datasets/datasf/san-francisco?select=bikeshare_trips
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
cual es la ciudad con peor calidad de aire (mayor indice de contaminacion)
en promedio durante el año 2020 segun la tabla global_air_quality ?
"""

query_01 = """
     with prom as(
            select
            city,
            value
            from bigquery-public-data.openaq.global_air_quality
            where extract(year from timestamp) = 2020
            order by value desc
            )
select
*
from prom
limit 1;
"""
df_query_01 = sq(query_01)
df_query_01


"""
# 2.- cual es la locacion ocn mayor cantidad de registros de calidad de aire
en la base de datos
"""

query_02 = """
     with prom as(
            select
            location,
            count(*) as cuantos
            from bigquery-public-data.openaq.global_air_quality
            group by location
            )
select
*
from prom
order by cuantos desc
limit 1;
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- cual ha sido el promedio de particulas PM2.5 en la atmosfera en las ultimas
24 horas en la ciudad más contaminada del mundo , segun los datos de la 
openaq.
"""

query_03_a = """
with more as(
        select
        city,
        value,
        timestamp
        from bigquery-public-data.openaq.global_air_quality
        where timestamp = (select max(timestamp) 
                           from bigquery-public-data.openaq.global_air_quality
                           )
        )
select
city,
extract(hour from timestamp) as hora,
value
from more
order by value desc
limit 1;
"""
df_query_03_a = sq(query_03_a)
df_query_03_a



"""
# 4.- 
¿ cuál es el promedio de concentración de NO2 (dioxido de nitrógeno) en
Alemania en los ultimos 30 dias ? 
"""

query_04_a = """
with more as(
        select
        country,
        avg(value) as promedio
        from bigquery-public-data.openaq.global_air_quality
        where timestamp >= timestamp_sub(timestamp, interval 30 day)
              and country = 'DE'
              and pollutant = 'no2'
        group by country
        )
select
*
from more
"""
df_query_04_a = sq(query_04_a)
df_query_04_a


"""
# 5.- 
¿ Cuál es el porcentaje de incremento en la concentración promedio de NO2 
en las ciudades de Alemania en comparación con el mismo período del año 
anterior ?
"""

query_05_a = """
with comprar as(
        select
        extract(year from timestamp) as year,
        avg(value) as promedio,
        
        from bigquery-public-data.openaq.global_air_quality
        where country = 'DE'
              and pollutant = 'no2'
        group by year
        )
select
year,
round((promedio - lag(promedio) over(order by year))/ lag(promedio) over(order by year), 2)*100  as difference
from comprar
"""
df_query_05_a = sq(query_05_a)
df_query_05_a





