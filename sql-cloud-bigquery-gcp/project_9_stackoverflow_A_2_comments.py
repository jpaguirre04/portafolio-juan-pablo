# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:28:24 2024

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
table_ref_1 = dataset_ref.table("comments")
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
¿ cuál es el usuario que ha realizado la mayor cantidad de comentarios en la 
plataforma de stackoverflow ?
"""

# tabla_1.columns

query_01 = """
select        
id,
count(*) as comentarios
from bigquery-public-data.stackoverflow.comments
where id is not null
group by id
order by comentarios desc
limit 1;
"""
df_query_01 = sq(query_01)
df_query_01


"""
# 2.- 
¿ cuál es el texto del comentario más largo que se ha realizado en la plataforma
de Stack Overflow ? 
"""

# tabla_1.columns

query_02 = """
select        
text
from bigquery-public-data.stackoverflow.comments
where text is not null
order by length(text)  desc
limit 1;
"""
df_query_02 = sq(query_02)
df_query_02


"""
# 3.- 
¿ cuál es el mes y el año en el que se realizaron mas comentarios en 
la plataforma de Stack Overflow ? 
"""

query_03 = """
select        
extract(year from creation_date) as year,
extract(month from creation_date) as mes,
count(*) as comentarios
from bigquery-public-data.stackoverflow.comments
where creation_date is not null
group by year, mes
order by comentarios desc
limit 1;
"""
df_query_03 = sq(query_03)
df_query_03


"""
# 4.- 
¿ cuál es el usuario que ha recibido mas comentarios en sus publicaciones
en la plataforma ?
"""

query_04 = """
select        
post_id,
count(*) as comentarios
from bigquery-public-data.stackoverflow.comments
where post_id is not null
group by post_id
order by comentarios  desc
limit 1;
"""
df_query_04 = sq(query_04)
df_query_04


"""
# 5.- 
¿Cuál es el patrón de comportamiento de los usuarios que realizan 
comentarios en la plataforma de Stack Overflow? Es decir, ¿cuál es 
el porcentaje de usuarios que realizan solo un comentario, dos 
comentarios, tres comentarios, etc.?
"""

query_05 = """
select
comentarios_por_usuario,
count(*) as cantidad_de_usuarios,
round(count(*) * 100 /(select count(distinct user_id) from bigquery-public-data.stackoverflow.comments), 2) as porcentaje
from (select
      user_id,
      count(*) as comentarios_por_usuario
      from bigquery-public-data.stackoverflow.comments
      group by user_id)
group by comentarios_por_usuario
order by comentarios_por_usuario asc;
"""
df_query_05 = sq(query_05)
df_query_05



"""
# 6.- 
¿ cuál es el título del post mas antiguo que se ha realizado en la plataforma?
"""

query_06 = """
select
text
from bigquery-public-data.stackoverflow.comments
order by creation_date 
limit 1;
"""
df_query_06 = sq(query_06)
df_query_06


"""
# 7.- 
¿Cuál es el patrón de distribución de los comentarios en la plataforma de 
Stack Overflow según la hora del día? Es decir, ¿en qué hora del día se 
realizan más comentarios, menos comentarios, etc.?
"""

query_07 = """
select
extract(hour from creation_date) as hora,
count(*) as cantidad_comentarios
from bigquery-public-data.stackoverflow.comments
group by hora
order by cantidad_comentarios desc
"""

df_query_07 = sq(query_07)
df_query_07


"""
# 8.- 
¿Cuál es el promedio de comentarios por pregunta en la tabla 'comments' de 
Stack Overflow, considerando solo las preguntas con más de 10 comentarios?
"""

query_08 = """
select
round(avg(comentarios_por_pregunta), 2) as promedio_de_consultas
from(select
     post_id,
     count(*) as comentarios_por_pregunta
     from bigquery-public-data.stackoverflow.comments
     group by post_id
     having count(*) > 10
     )as subconsulta
"""
df_query_08 = sq(query_08)
df_query_08



"""
# 9.- 
¿Cómo podrías obtener el texto del comentario y el nombre del usuario que lo 
hizo para todos los comentarios que tienen más de 10 likes?
"""

query_09 = """
select
c.text,
u.display_name
from bigquery-public-data.stackoverflow.comments as c
join bigquery-public-data.stackoverflow.users as u 
on c.user_id = u.id
where c.score > 10
"""
df_query_09 = sq(query_09)
df_query_09



"""
# 10.- 
¿Cómo podrías obtener el ID del comentario y el texto del comentario para 
los comentarios que tienen más de 5 likes y que fueron realizados por 
usuarios que tienen más de 1000 puntos de reputación?
"""

query_10 = """
select
c.user_id,
c.text
from bigquery-public-data.stackoverflow.comments as c
join bigquery-public-data.stackoverflow.users as u 
on c.user_id = u.id
where c.score > 10 and
      u.reputation > 1000
"""
df_query_10 = sq(query_10)
df_query_10




# https://padlet.com/monipenia01/alianza-interactive-classwork-a1-a2-8wczvw1i6ohbad6r










