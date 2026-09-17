# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:44:18 2024

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
table_ref_1 = dataset_ref.table("311_service_requests")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=10).to_dataframe()      

# tabla_1.columns


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
#########---- table: sffd_service_calls -----########
"""

#  el dept de servicios municipales quiere analizar la eficiencia 
# en la resolucion de solicitudes de servicio  por categoria y 
# ubicacion. Necesita identificar:
    
# 1.- las 3 categorias con mayor tiempo promedio de resolucion en cada distrito
# policial.

# 2.- el tiempo promedio de resolucion para cada categoria en cada distrito policial.

# 3.- el número total de solicitudes cerrradas en cada distrito policial.


# tabla_1.columns


query_00 = """
      with solicitudes_cerradas as(
      select 
      police_district,
      category,
      date_diff(closed_date, created_date, day) as tiempo_resolucion
      from  bigquery-public-data.san_francisco.311_service_requests
      where police_district != '' and
            category is not null and
            created_date is not null and 
            closed_date is not null
      ),
      estadisticas_por_distrito as(
      select
      police_district,
      category,
      avg(tiempo_resolucion) as tiempo_promedio_resolucion,
      count(*) as total_solicitudes_cerradas,
      row_number() over(partition by police_district order by avg(tiempo_resolucion) desc) as rn
      from solicitudes_cerradas
      group by police_district, category
      )
select 
*
from estadisticas_por_distrito
where rn >= 3
order by tiempo_promedio_resolucion, total_solicitudes_cerradas
"""
df_query_00 = sq(query_00)
df_query_00
  

# tabla_1.columns

"""
El departamento de servicios municipales quiere analizar la eficiencia 
en la resolución de solicitudes de servicio en diferentes barrios. 
Necesitan:

1. Los 3 barrios con mayor tiempo promedio de resolución de solicitudes.
2. El tiempo promedio de resolución para cada barrio.
3. La cantidad de solicitudes cerradas para cada barrio.
4. El porcentaje de solicitudes resueltas dentro del tiempo promedio 
para cada barrio.
"""


query_02 = """
with solicitudes_cerradas as(
      select
      neighborhood,
      date_diff(closed_date, created_date, day) as tiempo_resolucion
      from  bigquery-public-data.san_francisco.311_service_requests 
      where status = 'Closed'   
      ),
     estadisticas_por_barrio as(
       select
       neighborhood,
       avg(tiempo_resolucion)  as tiempo_promedio_resolucion,
       count(*)   as total_solicitudes_cerradas
       from  solicitudes_cerradas
       group by  neighborhood
       )
select 
  eb.neighborhood,
  eb.tiempo_promedio_resolucion,
  eb.total_solicitudes_cerradas,
  round((count(case when sc.tiempo_resolucion <= eb.tiempo_promedio_resolucion 
    then 1 end) * 100) / eb.total_solicitudes_cerradas, 2) as 
  porcentaje_resueltas_dentro_tiempo_promedio
from
  estadisticas_por_barrio eb
join 
  solicitudes_cerradas sc on eb.neighborhood = sc.neighborhood
group by 
  eb.neighborhood,
  eb.tiempo_promedio_resolucion,
  eb.total_solicitudes_cerradas
order by 
  tiempo_promedio_resolucion DESC
limit 3;
"""
df_query_02 = sq(query_02)
df_query_02



