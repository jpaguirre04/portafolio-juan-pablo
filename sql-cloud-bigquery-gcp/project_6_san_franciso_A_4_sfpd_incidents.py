# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:20:09 2024

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
table_ref_1 = dataset_ref.table("sfpd_incidents")
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
# 1.- Calcule el número total de incidentes (incidents) por tipo 
(incident_type) y día de la semana (day_of_week) en los últimos 6 meses 
en el distrito financiero (Financial District) de San Francisco. Ordene 
los resultados por tipo de incidente y frecuencia descendente.
"""

# tabla_1.columns

query_00 = """
select
category as incident_type,
dayofweek as dia_semana,
count(*) as numero_total_incident
from bigquery-public-data.san_francisco.sfpd_incidents
where pddistrict = 'PARK' and
timestamp <= timestamp_sub((select max(timestamp) from bigquery-public-data.san_francisco.sfpd_incidents), 
                           interval 180 day)
group by incident_type, dia_semana
order by numero_total_incident desc
"""
df_query_00 = sq(query_00)
df_query_00



query_01 = """
select
category as incident_type,
dayofweek as dia_semana,
count(*) as numero_total_incident
from bigquery-public-data.san_francisco.sfpd_incidents
where pddistrict = 'PARK' and
extract(month from timestamp) >= extract(month from  current_timestamp()) - 6
group by incident_type, dia_semana
order by numero_total_incident desc
"""
df_query_01 = sq(query_01)
df_query_01


"""
# 2.-  obtener el total de inciddentes registrados en la tabla sfpd_incidents
durante los ultimos 30 días desde la última fecha registrada en la tabla
"""

query_02 = """
select
count(*) total
from bigquery-public-data.san_francisco.sfpd_incidents
where
timestamp >= (select max(timestamp) - interval 30 day 
              from bigquery-public-data.san_francisco.sfpd_incidents)
"""
df_query_02 = sq(query_02)
df_query_02



"""
3.- 
"Se necesita una consulta SQL que muestre el número de incidentes ocurridos 
en un día específico (15 de marzo de 2022) en la tabla 'dfpd_incidents'."
Otra más:
"¿Cómo obtener el recuento de incidentes registrados en la tabla 
'dfpd_incidents' para el día 15 del mes 3 del año 2022?"
"""

query_03 = """
select
count(*) total_incidentes
from bigquery-public-data.san_francisco.sfpd_incidents
where
timestamp >= '2022-03-15 00:00:00'
and
timestamp < '2022-03-16 00:00:00'
"""
df_query_03 = sq(query_03)
df_query_03



"""
¿ como obtener el recuento de incidentes registrados en la tabla incidents, 
para el segundo semestre del año 2016 ?
"""

query_04 = """
select
count(*) as total_incidents
from bigquery-public-data.san_francisco.sfpd_incidents
where timestamp > '2016-01-01 07:29:00+00:00'
and timestamp < '2016-10-01 07:29:00+00:00'
"""
df_query_04 = sq(query_04)
df_query_04



"""
Obtener el total de incidentes registrados en la tabla incidents durante 
los meses de enero, febrero, y marzo de culquier año
"""

query_05 = """
select
count(*) total_incidents
from bigquery-public-data.san_francisco.sfpd_incidents
where extract(month from timestamp) in (1,2,3)
"""
df_query_05 = sq(query_05)
df_query_05


tabla_1.columns

"""
6.- ¿Cuál es el top 5 de categorías de incidentes que tienen la mayor 
proporción de resoluciones por arresto en cada distrito policial de San 
Francisco, considerando solo incidentes reportados entre 2018 y 2020?
"""  

query_06_a = """
with incidentes_arresto as(
        select
        pddistrict as district,
        category, 
        count(case when resolution = 'Arrest' then 1 end) / count(*) as arrest_rate
        from bigquery-public-data.san_francisco.sfpd_incidents
        where timestamp between '2018-01-01' and '2020-12-31'
        group by
        district, category
        )
select
district,
category,
arrest_rate
from(select 
     district, 
     category, 
     arrest_rate,
     row_number() over(partition by district order by arrest_rate desc) as row_num
     from incidentes_arresto
     ) as subquery
     where
     row_num <= 5
     order by
     district, arrest_rate desc;
"""
df_query_06_a = sq(query_06_a)
df_query_06_a


# tabla_1.columns

query_06_b = """
WITH incidentes_arresto AS (
SELECT
pddistrict as district,
category,
COUNT(CASE WHEN resolution = 'ARREST, CITED' THEN 1 END) / COUNT(*) AS arrest_rate
FROM
bigquery-public-data.san_francisco.sfpd_incidents
WHERE
timestamp BETWEEN '2018-01-01' AND '2020-12-31'
GROUP BY
district, category
)
SELECT
district,
category,
arrest_rate
FROM (
SELECT
district,
category,
arrest_rate,
ROW_NUMBER() OVER (PARTITION BY district ORDER BY arrest_rate DESC) AS row_num
FROM
incidentes_arresto
) AS subquery
WHERE
row_num <= 5
ORDER BY
district, arrest_rate DESC;
"""
df_query_06_b = sq(query_06_b)
df_query_06_b


# tabla_1.columns

query_06_c = """
with incidentes_arresto as(
        select
        pddistrict as district,
        category,
        count(case when resolution = 'ARREST, CITED' then 1 end) / count(*) as arrest_rate
        from bigquery-public-data.san_francisco.sfpd_incidents
        where timestamp between '1995-01-01' and '2020-12-31'
        group by  district, category
        ),
      incidente as(
          select
          district,
          category,
          arrest_rate,
          row_number() over(partition by district order by arrest_rate desc) as row_num
          from  incidentes_arresto 
        )
select
*
from incidente
where row_num <= 5
order by district, arrest_rate desc
"""
df_query_06_c = sq(query_06_c)
df_query_06_c




query_06_d = """
select
pddistrict as district,
category,
count(case when resolution = 'ARREST, CITED' then 1 end) / count(*) as arrest_rate
from bigquery-public-data.san_francisco.sfpd_incidents
where timestamp BETWEEN '1995-01-01' AND '2020-12-31'
group by district, category
"""
df_query_06_d = sq(query_06_d)
df_query_06_d




"""
¿Cuál es la hora del día en que se reportan la mayor cantidad de incidentes 
en cada día de la semana en San Francisco, considerando solo incidentes 
reportados entre 2018 y 2020?
"""

query_07_a = """
with incidentes_diarios as(
        select
        extract(dayofweek from timestamp) as dia_semana,
        extract(hour from timestamp) as hora_dia,
        count(*) as total_incidentes
        from bigquery-public-data.san_francisco.sfpd_incidents
        where timestamp between '2018-01-01' and '2020-12-31'
        group by dia_semana, hora_dia
        )
select
dia_semana,
hora_dia,
total_incidentes
from (select
      dia_semana,
      hora_dia,
      total_incidentes,
      row_number() over(partition by dia_semana 
              order by total_incidentes desc) as row_num
      from incidentes_diarios) as subquery
where row_num = 1
order by dia_semana;
"""
df_query_07_a = sq(query_07_a)
df_query_07_a



tabla_1.columns


"""
# 8
¿Cuál es el porcentaje de incidentes resueltos por categoría en cada distrito 
policial de San Francisco, considerando solo incidentes reportados entre 
2018 y 2020?
"""

query_08_a = """
with incidentes_resueltos as(
        select
        pddistrict as distrito,
        category,
        count(case when resolution is not null then 1 end) as resueltos,
        count(*) as total
        from bigquery-public-data.san_francisco.sfpd_incidents
        where timestamp between '2000-01-01' and '2018-01-01'
        group by distrito, category
      )
select
distrito,
category,
(resueltos/total) * 100 as porcentaje_resueltos
from incidentes_resueltos
order by distrito, category;
"""
df_query_08_a = sq(query_08_a)
df_query_08_a



"""
# 9
¿Cuál es la media móvil de 7 días de la cantidad de incidentes diarios 
en cada distrito policial de San Francisco, considerando solo incidentes 
reportados entre 2018 y 2020?
"""


tabla_1.columns

query_09_a = """
with incidentes_diarios as(
        select
        pddistrict as distrito,
        timestamp,
        count(*) as total_incidentes
        from bigquery-public-data.san_francisco.sfpd_incidents
        where timestamp between '2018-01-01' and '2020-12-31'
        group by distrito, timestamp
        )
select
distrito,
timestamp,
total_incidentes,
avg(total_incidentes) over(partition by distrito order by timestamp
                           rows between 6 preceding and current row)
                           as media_movil_7_dias
from incidentes_diarios
order by distrito, timestamp
"""
df_query_09_a = sq(query_09_a)
df_query_09_a


# TABLA street_trees


# Construct a reference to the "bikeshare_trips" table
table_ref_2 = dataset_ref.table("street_trees")
# API request - fetch the table
table_2 = client.get_table(table_ref_2)
# Preview the first five lines of the table
tabla_2 = client.list_rows(table_2, max_results=10).to_dataframe()      



"""
# 10
¿Cuál es la distribución porcentual de los árboles por tipo de cuidado 
(care_taker) en cada rango de diámetro (dbh) en la ciudad de 
San Francisco?
"""


query_10_a = """
with arboles_cuidado as(
        select
        care_taker,
        dbh,
        count(*) as total_arboles
        from bigquery-public-data.san_francisco.street_trees
        group by care_taker, dbh
        )
select
care_taker,
dbh,
total_arboles,
(total_arboles /sum(total_arboles) over (partition by care_taker)) * 100 as procentaje_arboles
from arboles_cuidado
order by care_taker, dbh;
"""
df_query_10_a = sq(query_10_a)
df_query_10_a




