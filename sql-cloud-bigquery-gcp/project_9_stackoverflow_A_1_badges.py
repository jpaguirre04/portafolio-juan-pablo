# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:57:15 2024

@author: Juan Pablo Aguirre
"""


import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("stackoverflow", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("badges")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=1000).to_dataframe()      

"""
# it's me
# the follows querys are me, from data
# https://www.kaggle.com/datasets/stackoverflow/stackoverflow
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
¿ cual es el nombre del badge que se otorga a los usuarios que responden una
pregunta con una respuesta aceptada por el autor de la pregunta ?
"""

# tabla_1.columns

query_01 = """
select        
name,
count(*) as cuantas_buenas_preguntas
from bigquery-public-data.stackoverflow.badges
where name = 'Nice Answer'
group by name
"""
df_query_01 = sq(query_01)
df_query_01



"""
# 2.- 
¿ cuál es el número total de badges que se han otorgado a los usuarios 
de stackoverflow ?
"""

query_02 = """
select        
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- 
¿cual es el nombre del badge que se otorga con mayor frecuencia a los 
usuarios de StackOverflow ?
"""

query_03 = """
select        
name,
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
group by name
order by total_badges desc
limit 1;
"""
df_query_03 = sq(query_03)
df_query_03


query_03_b = """
select name       
from (select
      name,
      count(*) as total_badges
      from bigquery-public-data.stackoverflow.badges
      group by name
      )
where total_badges = (
                      select
                      max(total_badges)
                      from(
                      select name, count(*) as total_badges
                      from bigquery-public-data.stackoverflow.badges
                      group by name
                      )
);
"""
df_query_03_b = sq(query_03_b)
df_query_03_b


"""
# 4.- 
¿Cuál es el nombre del badge que se otorga a los usuarios que han realizado 
una cierta cantidad de ediciones en la plataforma?
"""

query_04 = """
select        
name,
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
where lower(name) like '%editor%' or lower(name) like '%edit%'
group by name
order by total_badges desc;
"""
df_query_04 = sq(query_04)
df_query_04



"""
# 5.- 
¿ cuál es el año en el que se otorgan mas badges en stackoverflow ?
"""

query_05 = """
select        
extract(year from date) as year,
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
group by year
order by total_badges desc
limit 1;
"""
df_query_05 = sq(query_05)
df_query_05



"""
# 6.- 
¿ cuál es el nombre del badge que se otorga a los usuarios
que han obtenido una cierta cantidad de votos positivos
en sus respuestas ?
"""

query_06 = """
select        
name, 
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
where lower(name) like '%positive%'
group by name
order by total_badges desc
"""
df_query_06 = sq(query_06)
df_query_06



"""
# 7.- 
¿ cuál es el día de la semana en donde se otorga mas badges
en stackpverflow ?
"""

query_07 = """
select
extract(dayofweek from date) as dia_semana,
count(*) as total_badges
from bigquery-public-data.stackoverflow.badges
group by dia_semana
order by total_badges
limit 1;
"""
df_query_07 = sq(query_07)
df_query_07



"""
8.-
¿Cuál es el porcentaje de badges que se otorgan a usuarios que han obtenido 
al menos 10 badges en total, en relación con el total de badges otorgados 
en la plataforma?
"""

query_08 = """
with badges_por_usuarios as(
        select user_id,
        count(*) as total_badges
        from bigquery-public-data.stackoverflow.badges
        group by user_id
        ),
      usuarios_con_10_o_mas_badges as(
        select
        count(*) as total_usuarios
        from badges_por_usuarios
        where total_badges > 10  
        ),
      total_badges_otorgados as(
        select count(*) as total_badges
        from bigquery-public-data.stackoverflow.badges
       )
select
(total_usuarios * 1.0 /total_badges) *100 as porcentaje_badges
from usuarios_con_10_o_mas_badges, total_badges_otorgados;
"""
df_query_08 = sq(query_08)
df_query_08




