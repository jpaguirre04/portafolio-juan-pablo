# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:13:30 2024

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
table_ref_1 = dataset_ref.table("post_links")
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


"""
# 1.- 
¿ Cómo podrías obtener el ID del post origen y el ID del post destino para 
todos los enlaces de tipo "duplicado" ?
"""
# tabla_1.columns

query_01 = """
select
post_id,
related_post_id
from bigquery-public-data.stackoverflow.post_links
where link_type_id = 3     
"""
df_query_01 = sq(query_01)
df_query_01



"""
# 2.- 
¿ Cómo podrías obtener el número total de enlaces de tipo "relacionado" y
  "duplicado" en la tabla post_links ?
"""
# tabla_1.columns

query_02 = """
select
sum(case when link_type_id = 1 then 1 else 0 end) as relacionado,
sum(case when link_type_id = 3 then 1 else 0 end) as duplicado
from bigquery-public-data.stackoverflow.post_links
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- 
¿Cómo podrías obtener el ID del post que tiene el mayor número de enlaces 
relacionados en la tabla post_links?
"""
# tabla_1.columns

query_03 = """
select
post_id,
count(*) as relacionado
from bigquery-public-data.stackoverflow.post_links
where link_type_id = 1
group by post_id
order by count(*) desc
limit 1;
"""
df_query_03 = sq(query_03)
df_query_03


"""
# 4.- 
¿Cómo podrías obtener el número total de posts que tienen al menos un enlace 
relacionado en la tabla post_links?
"""
# tabla_1.columns

query_04 = """
select
count(*) as relacionado
from bigquery-public-data.stackoverflow.post_links
where link_type_id = 1
"""
df_query_04 = sq(query_04)
df_query_04


"""
# 5.- 
¿Cómo podrías obtener el ID del post que tiene el mayor número de enlaces 
relacionados y, al mismo tiempo, obtener el ID del post relacionado que 
aparece con más frecuencia en esos enlaces?
"""
# tabla_1.columns

query_05 = """
WITH relacionados AS (
  SELECT post_id, related_post_id
  FROM bigquery-public-data.stackoverflow.post_links
  WHERE link_type_id = 1
),
max_relacionados AS (
  SELECT post_id, COUNT(related_post_id) AS num_relacionados
  FROM relacionados
  GROUP BY post_id
  ORDER BY num_relacionados DESC
  LIMIT 1
),
max_apariciones AS (
  SELECT related_post_id, COUNT(post_id) AS num_apariciones
  FROM relacionados
  GROUP BY related_post_id
  ORDER BY num_apariciones DESC
  LIMIT 1
)
SELECT 
  (SELECT post_id FROM max_relacionados) AS post_id_max_relacionados,
  (SELECT related_post_id FROM max_apariciones) AS post_id_max_apariciones
"""
df_query_05 = sq(query_05)
df_query_05


# tarea task english 23_12_2024
# https://padlet.com/monipenia01/alianza-interactive-classwork-a1-a2-8wczvw1i6ohbad6r
