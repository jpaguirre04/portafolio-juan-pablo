# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:55:01 2024

@author: Juan Pablo Aguirre
"""

# https://www.kaggle.com/code/hanelliotphan/exercise-order-by
import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("world_bank_intl_education", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("country_series_definitions")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=5).to_dataframe()      


# Construct a reference to the "bikeshare_trips" table
table_ref_2 = dataset_ref.table("country_summary")
# API request - fetch the table
table_2 = client.get_table(table_ref_2)
# Preview the first five lines of the table
tabla_2 = client.list_rows(table_2, max_results=5).to_dataframe()      


# Construct a reference to the "bikeshare_trips" table
table_ref_3 = dataset_ref.table("international_education")
# API request - fetch the table
table_3 = client.get_table(table_ref_3)
# Preview the first five lines of the table
tabla_3 = client.list_rows(table_3, max_results=5).to_dataframe()      


# Construct a reference to the "bikeshare_trips" table
table_ref_4 = dataset_ref.table("series_summary")
# API request - fetch the table
table_4 = client.get_table(table_ref_4)
# Preview the first five lines of the table
tabla_4 = client.list_rows(table_4, max_results=5).to_dataframe()      


# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()


"""
#########---- table: country_series_definitions -----########
"""

# how many code_country there's by serie_code
query_01 = """
with h_m as(
select
series_code,
count(series_code) how_many,
from  bigquery-public-data.world_bank_intl_education.country_series_definitions
group by  series_code
)
select *,
rank() over (order by how_many desc) as ranking
from h_m
order by ranking
"""
df_query_01 = sq(query_01)
df_query_01



# how many serie code there by country code,  and number the 
# rows in a result set
query_02 = """
with h_m as(
select
country_code,
count(country_code)  how_many
from bigquery-public-data.world_bank_intl_education.country_series_definitions
group by country_code
)

select
*,
row_number() over (order by country_code) as ranking_position
from h_m
"""
df_query_02 = sq(query_02)
df_query_02




# how many descriptions there, and group rows by a range

# Example #19 – Group Rows by a Range
query_03 = """
with h_m as (
select
description,
count(description)  how_many
from bigquery-public-data.world_bank_intl_education.country_series_definitions
group by description
)
select
   case 
   when how_many <= 2   then 'low'
   when how_many > 2 and how_many <= 6 then 'medium'
   when how_many > 6 then 'high'
 end as description_of_category,
count(*) as range_description
from h_m
group by
case 
when how_many <= 2   then 'low'
when how_many > 2 and how_many <= 6 then 'medium'
when how_many > 6 then 'high'
end
"""
df_query_03 = sq(query_03)
df_query_03


"""
#########---- tables: country_series_definitions and country_summary-----########
"""

# used inner or left join is the same

query_04 = """
with h_m as(
select
country_code,
count(country_code)  how_many_country
from bigquery-public-data.world_bank_intl_education.country_series_definitions
group by country_code
)
select
h_m.country_code,
t.short_name, 
table_name,
h_m.how_many_country,
rank() over (order by h_m.how_many_country desc) as ranking_country
from h_m
left join bigquery-public-data.world_bank_intl_education.country_summary as t
on h_m.country_code = t.country_code
order by ranking_country 
"""
df_query_04 = sq(query_04)
df_query_04



"""
#########---- tables: 1) Government expenditure on education -----########
"""

# calculate GDP in education while have benn pandemic, in certain areas

query_05 = """
select
country_name, 
avg(value) as avg_ed_spending_pct
from bigquery-public-data.world_bank_intl_education.international_education
where country_name = 'Chile'  and
      (year >= 2020 or year <= 2022) and
      (indicator_code = 'UIS.GER.123.M'  or  indicator_code = 'LO.TIMSS.MAT8.HI.MA')
group by country_name
order by avg_ed_spending_pct
"""
df_query_05 = sq(query_05)
df_query_05


# chile = tabla_3[tabla_3['country_name']== 'Chile']

query_06 = """
select
indicator_code,
indicator_name, 
count(1) as num_rows
from bigquery-public-data.world_bank_intl_education.international_education
where year = 2016
group by indicator_name, indicator_code
having count(1) <= 175
order by count(1) desc
"""
df_query_06 = sq(query_06)
df_query_06



# return mean value, group by code country and year.
query_07 = """
select
country_code,
year,
avg(value) as mean_year_country
from bigquery-public-data.world_bank_intl_education.international_education
group by country_code, year
order by mean_year_country desc
"""

df_query_07 = sq(query_07)
df_query_07


# analytic function, in table country_series_definitions
# query to count the (cumulative) number of country code.

query_08 = """
with contar as (
     select   
     country_code,   
     count(*) as num_code
     from bigquery-public-data.world_bank_intl_education.country_series_definitions 
     group by country_code
    )
select
*,
sum(num_code)
    over(
        order by country_code
        rows between unbounded preceding and current row
        ) as num_code_cumulative
from contar 
"""

df_query_08 = sq(query_08)
df_query_08

