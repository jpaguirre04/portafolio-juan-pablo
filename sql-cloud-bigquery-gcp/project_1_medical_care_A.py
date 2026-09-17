# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 10:39:35 2024

@author: Juan Pablo Aguirre
"""

# https://www.kaggle.com/code/salikhussaini49/cms-insurance-analysis
# https://www.kaggle.com/code/salikhussaini49/cms-insurance-analysis

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("cms_medicare", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("inpatient_charges_2015")

# API request - fetch the table
table_1 = client.get_table(table_ref_1)


# Set up the query
query_job = client.query(f'select count(*) as row_cnt from bigquery-public-data.cms_medicare.inpatient_charges_2015')

# Preview the first five lines of the table
# tabla = client.list_rows(table, max_results=5).to_dataframe()      
tabla_1 = client.list_rows(table_1, max_results=5).to_dataframe()
tabla_1.head()

# tabla_1.columns


X = tabla_1[['total_discharges', 'average_covered_charges', 
             'average_total_payments', 'average_medicare_payments']]



# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()


# 1. Provider Activity & Volume¶
# 1. Actividad y volumen del proveedor
# What is the total number of discharges by provider city and state?
# ¿Cuál es el número total de altas por ciudad y estado del proveedor?


query_1_1 = """
select
provider_state, provider_city, provider_id, sum(total_discharges) as total_discharges
from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
group by provider_state, provider_city, provider_id
"""

df_query_1_1 = sq(query_1_1)
df_query_1_1
 

# 2.- Find the provider with the most total discharges in each state.
# 2.- Encuentre el proveedor con la mayor cantidad de altas totales en 
# cada estado.


# Set up the query

query_1_2 = """
with agg_discharge_provider_state_city as(
                select provider_state, 
                provider_id, 
                sum(total_discharges) as total_discharges
                from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
                group by provider_state, provider_id
),
top_1_provider as(
    select provider_state, 
    provider_id, 
    total_discharges
    from agg_discharge_provider_state_city
    qualify row_number() over(partition by
                              provider_state
                              order by total_discharges desc)=1
   )         
select *
from top_1_provider
order by total_discharges desc
"""

df_query_1_2 = sq(query_1_2)
df_query_1_2



# 3.- How Many providers have discharged more than 1,000 patients in the 
# last year PER STATE?
# ¿Cuántos proveedores han dado de alta a más de 1,000 pacientes en 
# el último año POR ESTADO?

query_1_3 = """
with agg_discharge_provider_state_city as(
select
provider_state, 
provider_id, 
sum(total_discharges) as total_discharges
from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
group by 
provider_state, provider_id
having total_discharges >  1000
), 
top_provider_cnt as(
    select
       provider_state,
       count(distinct provider_id) as provider_cnt
   from  agg_discharge_provider_state_city   
   group by provider_state 
)
select *
from top_provider_cnt
order by provider_cnt desc
"""

df_query_1_3 = sq(query_1_3)
df_query_1_3


# 4.- What is the average number of discharges per provider in each state?
# 4.- ¿Cuál es el número promedio de altas por proveedor en cada estado?

query_1_4 = """
with agg_discharge_provider_state_city as(
select
provider_state, provider_id, sum(total_discharges) as total_discharges
from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
group by 
provider_state, provider_id
)
, top_provider_cnt as(
    select
       provider_state,
       count(distinct provider_id) as count_provider,
       avg(total_discharges) avg_total_discharges
   from  agg_discharge_provider_state_city 
   group by provider_state 
)
select *
from top_provider_cnt
order by avg_total_discharges desc
"""

df_query_1_4 = sq(query_1_4)
df_query_1_4


# Which provider had the lowest number of discharges for a specific 
# DRG definition?
# ¿Qué proveedor tuvo el menor número de altas para una definición 
# específica de GRD?



# 2. Cost & Payment Analysis
# 2. Análisis de costos y pagos

# Which provider had the highest average total payments for any DRG 
# (Diagnosis-Related Group) definition?

# ¿Qué proveedor tuvo el promedio de pagos totales más alto para cualquier 
# definición de DRG (grupo relacionado con el diagnóstico)?

query_2_1 = """
with agg_provider_drg as(
     select
     drg_definition,
     provider_id,
     sum(average_total_payments)  as sum_total_payments
     from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
     group by drg_definition, provider_id
    ),
top_provider_cnt as(
    select
    drg_definition,
    provider_id,
    sum_total_payments
    from agg_provider_drg
    qualify row_number() over(partition by drg_definition order by sum_total_payments desc)= 1
    )
select *
from top_provider_cnt
order by sum_total_payments desc
"""
df_query_2_1 = sq(query_2_1)
df_query_2_1


# List the top 5 DRG definitions with the highest average Medicare payments.
# Enumere las 5 definiciones principales de DRG con los pagos promedio 
# más altos de Medicare.

query_2_2 = """
with agg_provider_drg as(
     select
     drg_definition,
     sum(average_medicare_payments)  as sum_average_medicare_payments
     from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
     group by drg_definition
    ),
top_provider_cnt as(
select
drg_definition,
sum_average_medicare_payments
from agg_provider_drg
qualify row_number() over(partition by drg_definition order by sum_average_medicare_payments desc) <= 6
)
select *
from top_provider_cnt
order by sum_average_medicare_payments desc
"""

df_query_2_2 = sq(query_2_2)
df_query_2_2


