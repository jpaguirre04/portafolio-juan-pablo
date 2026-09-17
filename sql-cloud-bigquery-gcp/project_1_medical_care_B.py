# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 11:05:01 2024

@author: Juan Pablo Aguirre
"""

# https://www.kaggle.com/code/salikhussaini49/cms-insurance-analysis
# https://www.kaggle.com/code/salikhussaini49/cms-insurance-analysis


# buscar el esquema de ejercicios acá
# https://learnsql.com/blog/25-advanced-sql-query-examples/


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

query_1_0 = """
with resultado as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state, 
                 provider_city, 
                 provider_id
        )
select *
from resultado
"""
df_query_1_0 = sq(query_1_0)
df_query_1_0


# ranking de altas médicas por ciudad y estado de prestaciones 

query_1_1 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state, 
                 provider_city, 
                 provider_id
        )
select         
        provider_state, 
        provider_city, 
        provider_id, 
        rank() over(order by total_discharges desc) as ranking
from resultado_ranking
order by ranking
"""
df_query_1_1 = sq(query_1_1)
df_query_1_1

# 1-2 enumerar las primeras 5 filas de un conjunto de resultados

query_1_2 = """
with resultado_ranking as (
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(select         
        provider_state, 
        provider_city, 
        provider_id, 
        rank() over(order by total_discharges desc) as ranking
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id, 
ranking
from ranking_o
where ranking <= 5
order by ranking
"""

df_query_1_2 = sq(query_1_2)
df_query_1_2



# Example #3 - List the Last 5 Rows of a Result Set

query_1_3 = """
with resultado_ranking as (
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(select         
        provider_state, 
        provider_city, 
        provider_id, 
        rank() over(order by total_discharges asc) as ranking
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id, 
ranking
from ranking_o
where ranking <= 5
order by ranking 
"""

df_query_1_3 = sq(query_1_3)
df_query_1_3


# Example #4 - List The Second Highest Row of a Result Set

query_1_4 = """
with resultado_ranking as (
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(select         
        provider_state, 
        provider_city, 
        provider_id, 
        rank() over(order by total_discharges desc) as ranking
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id, 
ranking
from ranking_o
where ranking = 2
order by ranking 
"""

df_query_1_4 = sq(query_1_4)
df_query_1_4



# Example #5 - List the Second Highest Discharges By City

query_1_5 = """
with resultado_ranking as (
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(select         
        provider_state, 
        provider_city, 
        provider_id, 
        rank() over(partition by provider_city order by total_discharges desc) as ranking
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id, 
ranking
from ranking_o
where ranking = 2
order by ranking 
"""

df_query_1_5 = sq(query_1_5)
df_query_1_5



# Example # 6 - List the First 50% Rows in a Result Set

query_1_6 = """
with resultado_ranking as(
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as sum_total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(
        select         
        *,
        ntile(2) over(order by sum_total_discharges) as ntile
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id,
sum_total_discharges
from ranking_o
where ntile = 1
order by sum_total_discharges
"""

df_query_1_6 = sq(query_1_6)
df_query_1_6



# Example # 7 - List the Last 25% Rows in a Result Set

query_1_7 = """
with resultado_ranking as(
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as sum_total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      ),

        ranking_o as(
        select         
        *,
        ntile(4) over(order by sum_total_discharges) as ntile
        from resultado_ranking
      )        
select
provider_state, 
provider_city, 
provider_id,
sum_total_discharges
from ranking_o
where ntile = 4
order by sum_total_discharges
"""

df_query_1_7 = sq(query_1_7)
df_query_1_7



# Example #8 - Number the Rows in a Result Set

query_1_8 = """
with resultado_ranking as(
       select
       provider_state,
       provider_city,
       provider_id,
       sum(total_discharges) as sum_total_discharges
       from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
       group by provider_state, 
                provider_city, 
                provider_id
      )        
select
provider_state, 
provider_city, 
provider_id,
sum_total_discharges,
row_number() over (order by provider_id) as ranking_position
from resultado_ranking
"""

df_query_1_8 = sq(query_1_8)
df_query_1_8



# Example #10 – Join a Table to Itself

query_1_10 = """
select
e1.provider_id ||' '|| e1.provider_name as codigo_proveedor,
e2.provider_city ||' '|| e2.provider_state as nombre_ciudad_estado
from bigquery-public-data.cms_medicare.inpatient_charges_2015 as  e1
join bigquery-public-data.cms_medicare.inpatient_charges_2015  as e2
on e1.provider_id = e2.provider_zipcode
"""

df_query_1_10 = sq(query_1_10)
df_query_1_10



# Example #11 – Show All Rows with an Above-Average Value by provider_id,
#  of suma_total_discharges
# Ejemplo n.º 11: mostrar todas las filas con un valor 
# superior al promedio 


query_1_11 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as suma_total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state,
                 provider_city, 
                 provider_id
        )
        select         
        provider_state, 
        provider_city, 
        provider_id, 
        suma_total_discharges
        from resultado_ranking
        where suma_total_discharges > (select avg(suma_total_discharges) from resultado_ranking)
"""
df_query_1_11 = sq(query_1_11)
df_query_1_11


# Example #12 – Privider with sum_total Higher Than Their State Average
# here i did need an add subquery

query_1_12 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as suma_total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state,
                 provider_city, 
                 provider_id
        )
        select         
        provider_state, 
        provider_city, 
        provider_id, 
        suma_total_discharges
        from resultado_ranking e1
        where suma_total_discharges >
        (select avg(suma_total_discharges) from resultado_ranking e2
                                           where e1.provider_city = e2.provider_city)
"""
df_query_1_12 = sq(query_1_12)
df_query_1_12




# Example #13 – Obtain All Rows Where a Value Is in a Subquery Result
# I need to konw which are the provider_id belonge by state 


query_1_13 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as suma_total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state,
                 provider_city, 
                 provider_id
        )
        select         
        provider_state, 
        provider_city, 
        provider_id, 
        suma_total_discharges
        from resultado_ranking
        where provider_id in (
           select provider_id
           from  resultado_ranking
            where provider_city = 'SPRINGFIELD')
        
"""
df_query_1_13 = sq(query_1_13)
df_query_1_13


# Example #14 – Find Duplicate Rows in SQL
query_1_14 = """
        select         
        provider_state, 
        provider_city, 
        provider_id, 
        total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by 
        provider_state, 
        provider_city, 
        provider_id, 
        total_discharges
        having count(*)>1
"""
df_query_1_14 = sq(query_1_14)
df_query_1_14



# Example #15 – Count Duplicate Rows
query_1_15 = """
        select         
        provider_state, 
        provider_city, 
        provider_id, 
        total_discharges,
        count(*) as number_of_rows
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by 
        provider_state, 
        provider_city, 
        provider_id, 
        total_discharges
        having count(*)>1
"""
df_query_1_15 = sq(query_1_15)
df_query_1_15


# Example #17 – Grouping Data with ROLLUP

query_1_17_a = """
select         
provider_state, 
provider_city, 
provider_id, 
sum(total_discharges) total
from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
group by 
provider_state,
provider_city,
provider_id
"""
df_query_1_17_a = sq(query_1_17_a)
df_query_1_17_a


query_1_17_b = """
select         
provider_state, 
provider_city, 
provider_id, 
sum(total_discharges) total
from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
group by rollup(provider_state,
provider_city,
provider_id
)
"""
# there are missing values 'Nan'
df_query_1_17_b = sq(query_1_17_b)
df_query_1_17_b = df_query_1_17_b.dropna()
df_query_1_17_b



lista_1 = list(tabla_1['provider_state'].unique())
lista_2 = list(tabla_1['provider_city'].unique())
lista_3 = list(tabla_1['provider_id'].unique())



# Example #18 – Conditional avg


query_1_18 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as suma_total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state, 
                 provider_city, 
                 provider_id
        )
select         
avg(case 
    when provider_city in ('SPRINGFIELD', 'LAWRENCE', 'MARLBOROUGH', 'HARTFORD')
    then suma_total_discharges
    else 0 end) as total_a,
avg(case 
    when provider_city in ('MIDDLETOWN', 'GARDNER', 'NEWTON')
    then suma_total_discharges
    else 0 end) as total_a

from resultado_ranking
"""

df_query_1_18 = sq(query_1_18)
df_query_1_18



# Example #19 – Group Rows by a Range

query_1_19 = """
with resultado_ranking as (
        select
        provider_state, 
        provider_city, 
        provider_id, 
        sum(total_discharges) as suma_total_discharges
        from bigquery-public-data.cms_medicare.inpatient_charges_2015 T
        group by provider_state, 
                 provider_city,
                 provider_id
        )
select
case
    when suma_total_discharges <= 5000 then 'low'
    when suma_total_discharges  > 5000 and  suma_total_discharges <=6000 then 'medium'
    when suma_total_discharges < 6000 then 'high'
    end as rangos,
    count(*) as number_discharges
from resultado_ranking
group by
case
    when suma_total_discharges <= 5000 then 'low'
    when suma_total_discharges  > 5000 and  suma_total_discharges <=6000 then 'medium'
    when suma_total_discharges < 6000 then 'high'
end    
"""

df_query_1_19 = sq(query_1_19)
df_query_1_19


# ver este en  kaggle, watch this in kaggle
# https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/input
