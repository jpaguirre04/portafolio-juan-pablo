# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 20:52:35 2024

@author: Juan Pablo Aguirre
"""


# project_2_How_to_Query_the_Bureau_of_Labor_Statistics

# https://www.kaggle.com/code/paultimothymooney/how-to-query-the-bureau-of-labor-statistics

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("bls", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("cpi_u")

# API request - fetch the table
table_1 = client.get_table(table_ref_1)

# Preview the first five lines of the table
# tabla = client.list_rows(table, max_results=5).to_dataframe()      
tabla_1 = client.list_rows(table_1, max_results=5).to_dataframe()
tabla_1.head()


# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()

# What is the average annual inflation across all US Cities?

query_1 = """
select
*,
round((100*(value-prev_year)/value), 1) rate
from
(
select
year,
lag(value) over(order by year) as prev_year,
round(value, 1) as value,
area_name
from bigquery-public-data.bls.cpi_u
where
period = 'S03'
and item_code = 'SA0'
and area_name = 'U.S. city average'
)
order by year
"""
df_1_query = sq(query_1)
df_1_query



# What was the monthly unemployment rate (U3) in 2016?
# ¿Cuál fue la tasa de desempleo mensual (U3) en 2016?

query_2 = """
select
year,
date,
period,
value,
series_title
from `bigquery-public-data.bls.unemployment_cps`
where
series_id = 'LNS14000000' and year = 2016
order by date
"""
df_2 = sq(query_2)
df_2



# What are the top 10 hourly-waged types of work in Pittsburgh, PA for 2016?
# ¿Cuáles son los 10 principales tipos de trabajo con salario por hora en 
# Pittsburgh, PA para 2016?


query_3 = """
select
year,
period,
value,
series_title
from bigquery-public-data.bls.wm
where series_title like '%Pittsburgh, PA%'
and year = 2016
order by  value desc
limit 10
"""
df_3 = sq(query_3)
df_3


