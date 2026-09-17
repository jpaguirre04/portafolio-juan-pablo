# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:10:49 2024

@author: Juan Pablo Aguirre
"""

#  https://www.kaggle.com/datasets/ncaa/ncaa-basketball?select=mbb_players_games_sr


# base de datos !!, data base!!
# https://www.kaggle.com/datasets/ncaa/ncaa-basketball

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("ncaa_basketball", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)


from project_4_basketball_B import tabla_1, tabla_2, tabla_3, tabla_4
from project_4_basketball_B import tabla_5, tabla_6, tabla_7, tabla_8
from project_4_basketball_B import tabla_9, tabla_10, sq



tabla_1.columns


#  what types of mascots are most popular

query_01 = """
select
mascot,
count(*) as total
from bigquery-public-data.ncaa_basketball.mascots
group by mascot
order by total desc
"""

df_query_01 = sq(query_01)
df_query_01


# serching if mascot name are repeated in the database, add ranking
# by mascot name


query_02 = """
with rankking as (
        select
        mascot_name,
        count(*)  as count
        from bigquery-public-data.ncaa_basketball.mascots
        where not (mascot_name = 'None')
        group by 1
        having count > 1
        order by 2 desc
        )
select 
*,
rank() over(order by count desc) as ranking
from rankking
order by ranking 
"""
df_query_02 = sq(query_02)
df_query_02




# query left join between team_colors and mbb_teams

query_03 = """
select
c.code_ncaa as id,
c.market as name_market,
c.color as name_color,
t.alias as name_alias,
t.school_ncaa as school_ncaa
from bigquery-public-data.ncaa_basketball.team_colors as c
left join  bigquery-public-data.ncaa_basketball.mbb_teams as t
on c.code_ncaa = t.code_ncaa
"""

df_query_03 = sq(query_03)
df_query_03


# query 

query_04 = """
with o as (
        select
        game_id,
        avg(field_goals_pct) as mean_field_goals_pct,
        from bigquery-public-data.ncaa_basketball.mbb_teams_games_sr
        where field_goals_pct is not null
        group by  game_id
        order by mean_field_goals_pct desc
        ),
        t as(
        select 
        game_id,
        min(scheduled_date) as scheduled_date,
        min(load_timestamp) as load_timestamp,
        count(*) as gogo
        from bigquery-public-data.ncaa_basketball.mbb_pbp_sr
        group by game_id
        )
select
o.game_id,
o.mean_field_goals_pct,
rank() over(order by o.mean_field_goals_pct desc) as ranking_mean,
t.scheduled_date,
t.load_timestamp,
from o 
inner join t
on  o.game_id = t.game_id      
"""
df_query_04 = sq(query_04)
df_query_04



# este esta interesante
# https://www.linkedin.com/pulse/everything-analytic-functions-advanced-sql-queries-arash-atarzadeh/

# son funciones avanzadas en sql 


# frecuency of venu3_city
# RANK and DENSE_RANK
query_05 = """
select
game_id,
venue_city,
row_number() over(order by venue_city) row_number,
rank() over(order by venue_city) rank,
dense_rank() over(order by venue_city) dense_rank
from bigquery-public-data.ncaa_basketball.mbb_teams_games_sr
"""

df_query_05 = sq(query_05)
df_query_05



query_06 = """
select
game_id,
venue_city,
row_number() over(partition by venue_city order by venue_city) row_number,
rank() over(partition by venue_city order by venue_city) rank,
dense_rank() over(partition by venue_city order by venue_city) dense_rank
from bigquery-public-data.ncaa_basketball.mbb_teams_games_sr
order by venue_city, dense_rank
"""

df_query_06 = sq(query_06)
df_query_06


# venue_city

# table_2 or mbb_games_sr
query_07 = """
select
game_id,
venue_city,
venue_state,
rank() over(partition by venue_state order by venue_city) ranking
from bigquery-public-data.ncaa_basketball.mbb_games_sr
where  game_id is not null and venue_city is not null 
       and  venue_state is not null
order by  ranking 
"""

df_query_07 = sq(query_07)
df_query_07


# window
query_08 = """
select
game_id,
venue_city,
venue_state,
h_field_goals_pct,
max(h_field_goals_pct) over(order by venue_state 
                            rows between unbounded preceding 
                            and 1 preceding) max_before,
max(h_field_goals_pct) over(order by venue_state
                            rows between 1 following and unbounded 
                            following) max_after
from bigquery-public-data.ncaa_basketball.mbb_games_sr
where game_id is not null and  venue_state is not null 
      and venue_city is not null and h_field_goals_pct is not null -- hola acá escribo tranquilo
"""

df_query_08 = sq(query_08)
df_query_08



# revisar la funcion extract con el tipo de dato de fecha


query_09 = """
SELECT
column_with_timestamp,
EXTRACT(DAY FROM column_with_timestamp)
FROM `bigquery-public-data.imaginary_dataset.imaginary_table`
limit 1000;
"""
df_query_09 = sq(query_09)
df_query_09


