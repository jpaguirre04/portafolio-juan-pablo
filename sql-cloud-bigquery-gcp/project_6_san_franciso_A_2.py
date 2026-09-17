# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:09:40 2024

@author: Juan Pablo Aguirre
"""



# recordemos que los B mayúsculas son los que voy a tomar para 
# ponerlos en mi archivo.

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
table_ref_1 = dataset_ref.table("street_trees")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=10).to_dataframe()      

tabla_1.columns


"""
# este es similar al curso de eficiencia de query 
# https://www.kaggle.com/code/desaivaibhav1995/san-francisco-open-data-bigquery
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
#########---- table:  -----########
"""


# Which neighborhoods have the highest proportion of offensive graffiti?
# ¿Qué barrios tienen la mayor proporción de graffitis ofensivos?

query_00 = """
select
neighborhood,
round(100*countif(strpos(descriptor,
      "- Not_offensive")> 0) / count(*), 2) as not_offensive_pct,
round(100*countif(strpos(descriptor,
      "- Offensive")> 0) / count(*), 2) as offensive_pct,
count(*) as total_count
from  bigquery-public-data.san_francisco.311_service_requests
where strpos(category, "Graffiti") > 0
group by neighborhood
order by offensive_pct desc
"""
df_query_00 = sq(query_00)
df_query_00



query_00_1 = """
select
strpos(descriptor,"- not_offensive") as not_offensive,
strpos(descriptor,"- offensive") as not_offensive,
strpos(category, "Graffiti") as graffitti
from  bigquery-public-data.san_francisco.311_service_requests
limit 100000;
"""
df_query_00_1 = sq(query_00_1)
df_query_00_1



# Which complaint is most likely to be made using Twitter and in which neighborhood?
# ¿Qué denuncia es más probable que se haga a través de Twitter y en qué barrio?
query_01 = """
select
neighborhood,
complaint_type,
count(*) as total_count
from  bigquery-public-data.san_francisco.311_service_requests
where source= 'Twitter'
group by neighborhood, complaint_type
order by total_count desc
"""
df_query_01 = sq(query_01)
df_query_01



# What are the most complained about Muni stops in San Francisco?
# ¿Cuáles son las paradas de Muni que más se quejan en 
# San Francisco?

query_02 = """
select
descriptor,
incident_address,
count(*) as total_count
from  bigquery-public-data.san_francisco.311_service_requests
where category = 'MUNI Feedback' and incident_address != 'Not associated with a specific address'
group by incident_address, descriptor
order by total_count desc
limit 10;
"""
df_query_02 = sq(query_02)
df_query_02


# What are the top 10 incident types that the San Francisco Fire 
# Department responds to?

# ¿Cuáles son los 10 principales tipos de incidentes a los que responde el 
# Departamento de Bomberos de San Francisco?

query_03 = """
select
call_type,
count(*) as call_type_count
from bigquery-public-data.san_francisco.sffd_service_calls
where call_type != ''
group by call_type
order by call_type_count desc
"""
df_query_03 = sq(query_03)
df_query_03


# How many medical incidents and structure fires are there in each neighborhood?

query_04 = """
select
neighborhood_district,
countif(call_type = "Medical Incident") as medical_incident_count,
countif(call_type = "Structure Fire") as structure_fire_count,
count(*) as total_count
from bigquery-public-data.san_francisco.sffd_service_calls
group by neighborhood_district
order by total_count desc
"""
df_query_04 = sq(query_04)
df_query_04



# What’s the average response time for each type of dispatched vehicle?

# ¿Cuál es el tiempo promedio de respuesta para cada tipo de vehículo 
# despachado?

query_05 = """
select
round(avg(timestamp_diff(on_scene_timestamp, received_timestamp, minute)), 2)
as latency,
count(*) as total_count
from bigquery-public-data.san_francisco.sffd_service_calls
where extract(date from received_timestamp) = extract(date from on_scene_timestamp)
group by unit_type
order by latency desc;
"""
df_query_05 = sq(query_05)
df_query_05



# Which category of police incidents have historically been the most common 
# in San Francisco?

# ¿Qué categoría de incidentes policiales han sido históricamente los más 
# comunes en San Francisco?

query_06 = """
select
category,
count(*) as incident_count
from bigquery-public-data.san_francisco.sfpd_incidents
group by category
order by incident_count desc
"""
df_query_06 = sq(query_06)
df_query_06


# agregar ranking de categorías
query_06_01 = """
with ranking_h as(
        select
        category,
        count(*) as incident_count
        from bigquery-public-data.san_francisco.sfpd_incidents
        group by category
       )
select
category, 
incident_count,
rank() over(order by incident_count) as ranking
from ranking_h 
order by ranking desc
"""
df_query_06_01 = sq(query_06_01)
df_query_06_01


# What were the most common police incidents in the category of 
# LARCENY/THEFT in 2016?

# ¿Cuáles fueron los incidentes policiales más comunes en la 
# categoría de HURTO/ROBO en 2016?

query_07 = """
select
descript,
count(*) incident_count_2016
from bigquery-public-data.san_francisco.sfpd_incidents
where category = 'LARCENY/THEFT'
and extract(year from timestamp) = 2016
group by descript
order by incident_count_2016 desc
limit 10;
"""
df_query_07 = sq(query_07)
df_query_07


# Which non-criminal incidents saw the biggest reporting change 
# from 2015 to 2016?

# ¿Qué incidentes no delictivos experimentaron el mayor cambio 
# en los informes de 2015 a 2016?

query_08 = """
select
descript,
countif(extract(year from timestamp)= 2016) -
countif(extract(year from timestamp)= 2015) as yoy_change,
countif(extract(year from timestamp)= 2016) as count_2016
from bigquery-public-data.san_francisco.sfpd_incidents
where category != 'non_criminal'
group by descript
order by abs(yoy_change) desc
limit 10;
"""
df_query_08 = sq(query_08)
df_query_08



# What is the diameter of the average tree in the city of San Francisco?
# ¿Cuál es el diámetro del árbol promedio en la ciudad de San Francisco?

query_09 = """
select
round(avg(cast(dbh as float64)), 2) as avg_width
from bigquery-public-data.san_francisco.street_trees
where dbh != '';
"""
df_query_09 = sq(query_09)
df_query_09



# What is the largest number of a particular species of tree 
# planted in a single year?

# ¿Cuál es la mayor cantidad de una especie particular de árbol 
# plantada en un solo año?

query_10 = """
select
extract(year from plant_date) as plantdate,
species,
count(*) as count
from bigquery-public-data.san_francisco.street_trees
where plant_date is not null and species != 'Tree(s) ::'
group by plantdate, species
order by count desc
limit 10; 
"""
df_query_10 = sq(query_10)
df_query_10



# Which San Francisco locations feature the largest number of trees?

# ¿Qué ubicaciones de San Francisco cuentan con la mayor 
# cantidad de árboles?

query_11 = """
select
latitude,
longitude,
count(*) as count
from bigquery-public-data.san_francisco.street_trees
where latitude is not null and 
      longitude is not null 
group by latitude, longitude
order by count desc
limit 20;
"""
df_query_11 = sq(query_11)
df_query_11


