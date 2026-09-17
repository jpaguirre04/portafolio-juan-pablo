# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:06:16 2024

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
table_ref_1 = dataset_ref.table("sffd_service_calls")
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

# how address had most emergency's calls, desc
# in all data
query_00 = """
select 
address,
count(address) count_calls
from  bigquery-public-data.san_francisco.sffd_service_calls
group by address
order by count_calls desc
"""
df_query_00 = sq(query_00)
df_query_00




# ¡ cuál es el tipo de servicio más comunmente solicitado en San Francisco
# y cuantas veces se han solicitado en el último año?



# ¿ cuantos incidentes de incendio (call type = ''Fire)
# ocurrieron en el año 2015 en la ciudad de san francisco?

query_01_1 = """
select 
count(*) as total_llamadas
from  bigquery-public-data.san_francisco.sffd_service_calls
where call_type = 'Vehicle Fire' and extract(year from call_date) = 2015
"""
df_query_01_1 = sq(query_01_1)
df_query_01_1


# ¿ Cuáles  son los 5 barrios (address) con más incidentes
# de emergencia médica (call type = Medical Incident) en la zona 
# norte de la ciudad (Battalion = north) ?

query_01_2 = """
select 
address,
count(*) as total_address
from  bigquery-public-data.san_francisco.sffd_service_calls
where call_type = 'Medical Incident' 
group by address
order by total_address desc
limit 5;
"""
df_query_01_2 = sq(query_01_2)
df_query_01_2




# qué tipo de llamadas (call_type) tienen más de 
# 500 incidentes en la ciudad de San Francisco

query_01_3 = """
select 
call_type,
count(*) as total_llamadas
from  bigquery-public-data.san_francisco.sffd_service_calls
group by call_type
having total_llamadas >= 500
order by total_llamadas desc
"""
df_query_01_3 = sq(query_01_3)
df_query_01_3




# ¿ qué batallones (battalion) tienen un promedio de más
# de 50 incidentes por día en el año 2015 ?

query_01_4 = """
select 
call_type,
count(*) /count(distinct call_date) as promedio
from  bigquery-public-data.san_francisco.sffd_service_calls
where extract(year from call_date) = 2014
group by call_type
having  promedio > 50;
"""
df_query_01_4 = sq(query_01_4)
df_query_01_4




# ¿Cuáles son los 5 tipos de  (battalion)
# más incidentes en la ciudad de San Francisco en el año 2008,
# ordenados de mayor a menor frecuencia ?

query_01_5 = """
select 
battalion,
count(*)  as count_battalion
from  bigquery-public-data.san_francisco.sffd_service_calls
where extract(year from call_date) = 2008
group by battalion
order by count_battalion desc
"""
df_query_01_5 = sq(query_01_5)
df_query_01_5


# ¿Qué 10 estaciones  (staion_are) tienen la mayor cantidad de 
#  incidentes de emergencia médica (call_type = "Medical Incident" 
# en el año 2020,  ordenados de menor a mayor tiempo de respuesta ?

query_01_6 = """
select 
station_area,
count(*) count_emergency_medical
from  bigquery-public-data.san_francisco.sffd_service_calls
where call_type = 'Medical Incident'
group by station_area
order by count_emergency_medical desc
limit 10;
"""
df_query_01_6 = sq(query_01_6)
df_query_01_6






# avanzado, advanced

# cuales son los 5 batallones (battalion) que tuvieron la mayor aumento
# en la cantidad de incidentes de incedio (call_category = 'Fire') entre
# 1 de enero de 2020 y el 31 de dic del 2020, comparados con el 
# mismo periodo del 2019 ?


query_01_7 = """
with incidents_2009 as(
     select
     battalion,
     count(*) as total_2009
     from  bigquery-public-data.san_francisco.sffd_service_calls
     where call_type = 'Vehicle Fire' and 
           extract(year from call_date) = 2009
     group by battalion      
     ),
    incidents_2010 as(
         select
         battalion,
         count(*) as total_2010
         from  bigquery-public-data.san_francisco.sffd_service_calls
         where call_type = 'Vehicle Fire' and 
               extract(year from call_date) = 2010
         group by battalion      
         )
select
i1.battalion,
i1.total_2009,
i2.total_2010,
((i2.total_2010 - i1.total_2009)/ i1.total_2009) *100 as high_pecent
from incidents_2009 i1
join incidents_2010 i2
on i1.battalion = i2.battalion
order by high_pecent desc
limit 5;
"""
df_query_01_7 = sq(query_01_7)
df_query_01_7




# ¿ cuales son los 5 meses con mayor cantidad de incidentes
# de emergencia médica (call_category = 'Medical Emergency')
# en la ciudad de San Francisco entre el 1 de enero de 1995
# y el 31 de dic de 2005, considerando solo los inciddentes en
# que ocurrieron entre las 8pm y las 2 am, y muestra el porcentaje
# de aumento en la cantidad de incidentes en 
# comparación con el mismo mes del año anterior ?



tabla_1['received_timestamp'].unique()



# revisar mañana acá
query_01_8 = """
with incidentes_anuales as(
        select
        extract(year from received_timestamp) as agno,
        extract(month from received_timestamp) as mes,
        count(*) as total_incidentes
        from bigquery-public-data.san_francisco.sffd_service_calls
        where call_type = 'Medical Incident'
        and
        extract(hour from received_timestamp)
        between 20 and 23
        or extract(hour from received_timestamp)
        between 0 and 2
        and call_date between '2003-01-01' and '2005-12-31'
        group by extract(year from received_timestamp), 
                 extract(month from received_timestamp) 
        ),
      incidencia_comparativas as (
        select
        *,
        lag(total_incidentes) over(partition by mes order by agno) as incidentes_anterior
        from incidentes_anuales
        )    
select
mes,
agno,
total_incidentes,
((total_incidentes - incidentes_anterior)/incidentes_anterior)* 100 as aumento_porcentual
from incidencia_comparativas
where incidentes_anterior is not null
order by aumento_porcentual desc
limit 5;
"""
df_query_01_8 = sq(query_01_8)
df_query_01_8

 




# 9.- El dept de comberons de san francisco quiere analizar la distribucion
#  de incidentes por tipo de emergencia y hora del dia.

# 1.- tipo de emergencia más comunes durante las hora punta
# (4 pm - 6 pm)
# 2.- el numero total de incidentes para cada tipo de emergencia durante
# las horas de punta
# 3.- la hora del dia con mas  incidentes para cada tipo de emergencia



query_01_9 = """
with incidentes_hora_punta as(
        select
        call_type,
        extract(hour from received_timestamp) as hora,
        count(*) as total_incidentes
        from bigquery-public-data.san_francisco.sffd_service_calls
        where
             extract(hour from received_timestamp)
             between 7 and 9
             or extract(hour from received_timestamp)
             between 16 and 18
        group by call_type, hora
        ),
       max_incidentes_por_hora as(
          select    
          call_type,
          hora,
          total_incidentes,
          row_number() over(partition by call_type 
                            order by total_incidentes desc) as rn
          from  incidentes_hora_punta
          )
select
call_type,
sum(total_incidentes) as total_incidentes,
max(case when rn=1 then hora end) as hora_max_incidents
from max_incidentes_por_hora
group by call_type
order by total_incidentes
limit 3;
"""
df_query_01_9 = sq(query_01_9)
df_query_01_9


