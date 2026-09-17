# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:49:32 2024

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
table_ref_1 = dataset_ref.table("bikeshare_trips")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=100000).to_dataframe()      

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

"""
# 0.- 

"""

# en vez de date_trunc en bigquery es timestamp_trunc()
# pero los terminos al reves


query_00 = """
with viajes_inicio as(
        select
        timestamp_trunc(start_date, day) as dia,
        format_date('%Y-%m-01', timestamp_trunc(start_date, month)) as mes,
        extract(day from start_date) as dia_del_mes,
        extract(year from start_date) as year,
        sum(duration_sec)  as duracion_total
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by dia, mes, dia_del_mes, year
        )
select
dia,
mes,
duracion_total,
((duracion_total - lag(duracion_total) over(partition by dia_del_mes order by year))/
lag(duracion_total)over(partition by dia_del_mes order by year)) as 
porcentaje_crecimiento
from viajes_inicio
"""
df_query_00 = sq(query_00)
df_query_00


"""
# 51.-  analisis de viajes por estación 
calcula el porcentaje de viajes que comienzan y terminan en la misma
estación, para las 5 estaciones con más viajes de inicio
"""

query_01 = """
select
start_station_name,
count(*) as total_viajes,
round((sum(if(start_station_name = end_station_name, 1, 0)) / count(*)) * 100, 2) as porcentaje_mismo_lugar
from bigquery-public-data.san_francisco.bikeshare_trips
group by start_station_name
order by porcentaje_mismo_lugar desc
limit 5;
"""
df_query_01 = sq(query_01)
df_query_01



"""
# 52
calcula la duracion promedio de los viajes por hora del dia,
para los dias laborales (de lunes a viernes)
"""

query_52 = """
select
extract(hour from start_date) as hora_del_dia,
extract(dayofweek from start_date) as dia_de_la_semana,
avg(timestamp_diff(end_date, start_date, second)) / 60 as duracion_promedio_minutos
from bigquery-public-data.san_francisco.bikeshare_trips
where extract(dayofweek from start_date) between 2 and 6 --lunes a viernes
group by hora_del_dia, dia_de_la_semana
order by duracion_promedio_minutos
"""
df_query_52 = sq(query_52)
df_query_52



"""
# 53
Calcula el número de viajes que comienzan en cada estación durante las 
horas pico (7-9 am y 4-6 pm) y no pico, para los días laborables.
"""

query_53 = """
select
start_station_name,
case when extract(hour from start_date) between 7 and 9 or
extract(hour from start_date) between 16 and 18 
then 'hora peak'
else 'hora no peak'
end as tipo_hora,
count(*) as num_viajes
from bigquery-public-data.san_francisco.bikeshare_trips
where extract(dayofweek from start_date) between 2 and 6 -- lunes a viernes
group by start_station_name, tipo_hora
order by num_viajes desc
"""
df_query_53 = sq(query_53)
df_query_53



"""
# 54
calcula el porcentaje de viajes largos(más de 30 minutos)
para cada estación, y muestra  solo las estaciones que tienen
un porcentaje mayor al promedio general.  
"""
query_54 = """
with lapso as (
        select
        start_station_name,
        round((sum(if(timestamp_diff(end_date, start_date, second)/60 >30 ,1 ,0))/count(*))*100,2) 
        as porcentaje_viajes_largos
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by start_station_name
        )
select
start_station_name,
porcentaje_viajes_largos
from lapso
where porcentaje_viajes_largos > (select avg(porcentaje_viajes_largos) from lapso)
order by porcentaje_viajes_largos desc
"""
df_query_54 = sq(query_54)
df_query_54




"""
# 55: Estaciones más populares por día de la semana_
Calcula el número de viajes que comienzan en cada estación para cada día de 
la semana y muestra las 3 estaciones más populares para cada día.
"""
query_55_a = """
with  viajes_por_dia_semana as(
        select
        extract(dayofweek from start_date) as dia_semana,
        start_station_name,
        count(*) as num_viajes
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by 
        dia_semana, start_station_name
        )
select
*,
row_number() over(partition by  dia_semana 
order by num_viajes desc) as ranking
from viajes_por_dia_semana
order by dia_semana, num_viajes desc
"""
df_query_55_a = sq(query_55_a)
df_query_55_a


query_55_b = """
with  viajes_por_dia_semana as(
        select
        extract(dayofweek from start_date) as dia_semana,
        start_station_name,
        count(*) as num_viajes
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by 
        dia_semana, start_station_name
        ),
      por_aca as(
          select
          *,
          row_number() over(partition by  dia_semana 
          order by num_viajes desc) as ranking
          from viajes_por_dia_semana
          )
select
*
from por_aca
where ranking <= 3         
order by dia_semana, num_viajes
"""
df_query_55_b = sq(query_55_b)
df_query_55_b



"""
# 56: Estaciones con mayor diferencia entre viajes de ida y vuelta.
Calcula la diferencia entre el número de viajes que comienzan y terminan
en cada estación. Muestra las 5 estaciones con mayor diferencia.
"""

query_56 = """
with viajes_inicio as(
        select
        start_station_name,
        count(*) as cantidad_inicio
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by start_station_name
        ),
     viajes_fin as(
         select
         end_station_name,
         count(*) as cantidad_end
         from bigquery-public-data.san_francisco.bikeshare_trips
         group by end_station_name
         )
select
vi.start_station_name, 
vf.end_station_name,
coalesce(vi.start_station_name, vf.end_station_name) as estacion,
cantidad_inicio, 
cantidad_end,
abs(cantidad_inicio - cantidad_end) as diferencia  
from  viajes_inicio as vi
full outer join viajes_fin as vf
on vi.start_station_name = vf.end_station_name
order by  diferencia desc
limit 5;
"""
df_query_56 = sq(query_56)
df_query_56



"""
# 57: distribucion de duracion de viajes por hora del día
Calcula la distribución de duración de viajes en (minutos) 
por hora del día. Muestra la hora del dia con mayor numero de viajes 
y la duracion promedio de esos viajes
"""

query_57_a = """
with distribucion as (
        select
        extract(hour from start_date) as hour,
        avg(timestamp_diff(end_date, start_date, minute)) as duracion_promedio_minutos,
        count(*) as numero_de_viajes
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by hour
        )
select
*
from distribucion
order by numero_de_viajes
limit 1;
"""
df_query_57_a = sq(query_57_a)
df_query_57_a


query_57_b = """
with distribucion as (
        select
        extract(hour from start_date) as hour,
        timestamp_diff(end_date, start_date, minute) as duracion_minutos,
        from bigquery-public-data.san_francisco.bikeshare_trips
        )
select
hour, 
count(*) num_viajes,
avg(duracion_minutos) duracion_promedio
from distribucion
group by hour
order by num_viajes
limit 1;
"""
df_query_57_b = sq(query_57_b)
df_query_57_b



"""
# 58: Análisis de patrones de viajes entre estaciones_
Calcula el número de viajes directos y el número de viajes con traslado 
entre cada par de estaciones. Muestra las 5 parejas de estaciones con mayor 
número de viajes directos y el porcentaje de viajes con traslado.
"""

query_58 = """
with viajes_directos as(
        select
        start_station_name,
        end_station_name,
        count(*) as num_viajes_directos
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by start_station_name, end_station_name
        ),
     viajes_con_traslado as(
         select    
         start_station_name,
         end_station_name,
         count(*) as num_viajes_con_traslado
         from bigquery-public-data.san_francisco.bikeshare_trips t1
         where t1.start_station_name != t1.end_station_name
         and exists(
                select 1
                from bigquery-public-data.san_francisco.bikeshare_trips  t2
                where t2.start_station_name = t1.end_station_name
                  and t2.end_station_name =  t1.start_station_name
             )
         group by start_station_name, end_station_name
         )
select
vd.start_station_name,
vd.end_station_name,
vd.num_viajes_directos,
coalesce(num_viajes_con_traslado, 0) as num_viajes_con_traslado,
round(coalesce(num_viajes_con_traslado, 0)*100/ num_viajes_directos, 2) as  porcentaje_traslado
from viajes_directos vd
left join viajes_con_traslado vct
on vd.start_station_name = vct.start_station_name
and vd.end_station_name = vct.end_station_name
order by num_viajes_directos desc
"""
df_query_58 = sq(query_58)
df_query_58

# https://www.youtube.com/watch?v=LkC3dxe_NVw
# podscat magement< line management

"""
# 59: estaciones mas populares por dia de la semana 
calcule las 3 estaciones mas populares para iniciar un viaje en cada dia
de la semana
"""


query_59 = """
with frecuencia as(
        select 
        extract(dayofweek from start_date) as dia_semana,
        start_station_name,
        count(*) as conteo
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by dia_semana, start_station_name
        ),
       por_aca as(
        select
        *,
        row_number() over(partition by  dia_semana 
        order by conteo desc) as ranking
        from frecuencia 
       )
select
*
from por_aca
where ranking <= 3
order by dia_semana, conteo
"""
df_query_59 = sq(query_59)
df_query_59


"""
# 60 top 5 de las estaciones con mayor duración promedio de viajes.
calcula las 5 estaciones con mayor duración promedio de viajes.
"""

query_60 = """
with frec as(
         select
         start_station_name,
         avg(duration_sec) as duracion_promedio,
         from bigquery-public-data.san_francisco.bikeshare_trips   
         group by start_station_name
        ),
       duracion_media as(
         select
         *,
         rank() over(partition by start_station_name 
         order by duracion_promedio desc) as ranking
         from frec
        )
select
*
from duracion_media
where ranking <= 5
order by duracion_promedio
"""
df_query_60 = sq(query_60)
df_query_60



query_60_a = """
with frec as(
         select
         start_station_name,
         avg(duration_sec) as duracion_promedio,
         from bigquery-public-data.san_francisco.bikeshare_trips   
         group by start_station_name
         order by duracion_promedio desc
        )
select
*
from frec
limit 5;
"""
df_query_60_a = sq(query_60_a)
df_query_60_a



"""
# 61: Viajes por hora del día
Calcula la cantidad de viajes realizados por hora del día, considerando 
solo los días laborables (de lunes a viernes).
"""

query_61 = """
with hour as (
        select
        extract(hour from start_date) as hora,
        count(*) as viajes
        from bigquery-public-data.san_francisco.bikeshare_trips
        where extract(dayofweek from start_date) between 1 and 5
        group by hora
        )
select
hora,
viajes
from hour
order by hora asc
"""
df_query_61 = sq(query_61)
df_query_61



"""
# 62: estaciones mas populares por membresía
Calcule las 5 estaciones mas populares para los usuarios con memeresia
(Suscriber)  y sin membresía (Customer), considerando solo los 
viajes realizados en el año 2018.
"""

query_62 = """
with populares as(
        select
        subscriber_type,
        start_station_name,
        count(*) as estacion_popular,
        row_number() over (partition by subscriber_type 
                           order by count(*) desc) as row_num
        from bigquery-public-data.san_francisco.bikeshare_trips
        where (subscriber_type = 'Subscriber' or
              subscriber_type = 'Customer') and
              extract(year from start_date) = 2016
        group by subscriber_type, start_station_name
        )
select
*
from populares
where row_num<= 5
order by subscriber_type, estacion_popular desc;
"""
df_query_62 = sq(query_62)
df_query_62


"""
# 63: 
viajes y estaciones
Calcula la cantidad de viajes realizados en cada estación.
Además, incluye la dirección y la ciudad de cada estación.
"""

query_63 = """
with viajes_estacion as(
        select
        start_station_id,
        count(*) as viajes
        from bigquery-public-data.san_francisco.bikeshare_trips
        group by start_station_id
        )
select
t2.start_station_id,
t1.landmark,
t1.name,
t2.viajes
from bigquery-public-data.san_francisco.bikeshare_stations t1
join viajes_estacion as t2
on t2.start_station_id =  t1.station_id
order by t2.viajes desc
"""
df_query_63 = sq(query_63)
df_query_63



"""
# 68: 
Calcula la cantidad de viajes realizados por:

1. Suscriptores (subscribers) durante las horas pico (7-9 am y 4-6 pm) 
en los días laborables (lunes a viernes).

2. Clientes (customers) durante el mismo período.
"""

query_68 = """
select
subscriber_type,
count(*) viajes
from bigquery-public-data.san_francisco.bikeshare_trips
where (extract(hour from start_date) between 7 and 9) or
      (extract(hour from start_date) between 14 and 18)
group by subscriber_type
order by viajes desc
"""
df_query_68 = sq(query_68)
df_query_68

