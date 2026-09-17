# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:12:53 2024

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
table_ref_1 = dataset_ref.table("post_history")
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
¿Cómo podrías obtener el ID del post y la fecha de la última revisión para 
todos los posts que han sido revisados al menos 5 veces?
"""


"""
select        
post_id,
max(creation_date) as ultima_revision
from bigquery-public-data.stackoverflow.post_history
group by post_id
having count(post_id) >= 5
"""

# tabla_1.columns

query_01 = """
select        
post_id,
creation_date as ultima_revision
from (select
      post_id,
      creation_date,
      row_number() over(partition by post_id order by creation_date desc) as revision_numero
      from bigquery-public-data.stackoverflow.post_history
      )
where revision_numero = 1 and post_id in(
select post_id
from bigquery-public-data.stackoverflow.post_history
group by post_id
having count(post_id) >= 5
)
"""
df_query_01 = sq(query_01)
df_query_01


"""
# 2.- 
¿Cómo podrías obtener el ID del post y el tipo de revisión (por ejemplo, 
"edit", "rollback", etc.) para todos los posts que han sido revisados 
más de una vez?
"""


query_02 = """
select        
post_id,
post_history_type_id as tipo_revision,
count(creation_date) as revisiones 
from bigquery-public-data.stackoverflow.post_history 
group by post_id, post_history_type_id
having count(post_id) > 1
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- 
¿Cómo podrías obtener el ID del post y la fecha de la primera revisión 
para todos los posts que han sido creados en el año 2010 y que han sido 
revisados al menos una vez?
"""


query_03 = """
select        
post_id,
min(creation_date) as fecha_minima
from bigquery-public-data.stackoverflow.post_history 
where extract(year from creation_date) = 2010
group by post_id
having count(post_id) > 1
"""
df_query_03 = sq(query_03)
df_query_03


"""
# 4.- 
¿Cómo podrías obtener el ID del post y el número total de revisiones para 
los 10 posts que han sido revisados más veces?
"""


query_04 = """
select        
post_id,
count(*) as revisiones
from bigquery-public-data.stackoverflow.post_history 
group by post_id
order by revisiones desc
limit 10;
"""
df_query_04 = sq(query_04)
df_query_04


"""
# 5.- 
¿Cómo podrías obtener el ID del post y la fecha de la última revisión para 
todos los posts que han sido revisados en el año 2018?
"""

query_05 = """
select        
post_id,
max(creation_date) as ultima_fecha_revision
from bigquery-public-data.stackoverflow.post_history 
where extract(year from creation_date) = 2018
group by post_id
"""
df_query_05 = sq(query_05)
df_query_05


# new year
# https://www.youtube.com/watch?v=7SwFmMHEV_c