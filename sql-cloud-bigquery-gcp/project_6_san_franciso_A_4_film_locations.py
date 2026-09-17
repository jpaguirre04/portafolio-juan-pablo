# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 10:02:05 2024

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
table_ref_1 = dataset_ref.table("film_locations")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=10000).to_dataframe()      

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
#########---- table: bikeshare_trips -----########
"""

tabla_1.columns
"""
# 1.-  Identifica los 5 barrios (locations) con más filmaciones
(film_count) en San Francisco, filmando solo peliculas (title)
que sean dramas.
"""


query_01 = """
select
locations,
count(*) filmaciones
from bigquery-public-data.san_francisco.film_locations
group by locations
order by filmaciones desc
"""
df_query_01 = sq(query_01)
df_query_01



"""
# 2.-  Calcula la cantidad de total de filmaciones realizadas  en cada
distrito de San Francisco y ordena los resultados de manera descendente. 
Además, incluye solo aquellos distritos que tienen mas de 50 filmaciones.
"""


query_02 = """
with local as(
        select
        locations,
        count(*) filmaciones
        from bigquery-public-data.san_francisco.film_locations
        group by locations
        order by filmaciones desc
      )
select
*
from local
where filmaciones  >= 20
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.-  Calcula el porcentaje de filmaciones realizadas en cada distrito de 
San Francisco respecto al total de filmaciones en la ciudad. Ordena los 
resultados de manera descendente según el porcentaje.
"""


query_03 = """
with total as(
        select
        locations,
        count(*) filmaciones
        from bigquery-public-data.san_francisco.film_locations
        group by locations
        )
select
*,
round(filmaciones/sum(filmaciones)over(), 2)* 100  as promedio
from total
order by promedio desc
"""
df_query_03 = sq(query_03)
df_query_03


"""
# 4.-  
Calcula el top 5 de directores que han filmado en más de un distrito en 
San Francisco, considerando solo películas filmadas después del año 2010.
Muestra el nombre del director, el número de distritos y el título de 
las películas filmadas en cada distrito.
"""

query_04 = """
with directores as(
        select
        director,
        count(distinct locations) as films_por_distrito
        from bigquery-public-data.san_francisco.film_locations
        where release_year >= 2000
        group by director
        order by films_por_distrito desc
        ),
       directores_y_fimls as(
               select
               director,
               title
               from bigquery-public-data.san_francisco.film_locations
               group by  director, title
      )
select
d.director, 
films_por_distrito,
df. title
from directores as d
join directores_y_fimls as df
on d.director = df.director
"""
df_query_04 = sq(query_04)
df_query_04


query_04_a = """
with directores_y_fimls as(
        select
        director,
        title
        from bigquery-public-data.san_francisco.film_locations
        group by  director, title
        )
select
*
from directores_y_fimls
"""
df_query_04_a = sq(query_04_a)
df_query_04_a

# task 11-11-2024
# https://padlet.com/monipenia01/interactive-classwork-level-b1-b2-hc2pe21uetjphkkc

