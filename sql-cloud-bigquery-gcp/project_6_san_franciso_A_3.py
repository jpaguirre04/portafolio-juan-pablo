# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 08:40:24 2024

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
table_ref_1 = dataset_ref.table("bikeshare_stations")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=10).to_dataframe()      

# tabla_1.columns


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

# Number of stations per Landmark
query_01 = """
select 
distinct
landmark,
count(landmark) as no_of_stations
from  bigquery-public-data.san_francisco.bikeshare_stations
group by landmark
"""
df_query_01 = sq(query_01)
df_query_01



# Total number of docks per landmark

query_02 = """
select 
distinct
landmark,
sum(dockcount) as docks
from  bigquery-public-data.san_francisco.bikeshare_stations
group by landmark
"""
df_query_02 = sq(query_02)
df_query_02


# Installations in San Francisco landmark in the year 2013
query_03 = """
select 
name,
dockcount,
installation_date
from  bigquery-public-data.san_francisco.bikeshare_stations
where landmark = 'San Francisco' and installation_date between '2013-01-01' AND '2014-01-01'
"""
df_query_03 = sq(query_03)
df_query_03


# San Jose dockcount and installation date
query_04 = """
select 
name, 
dockcount,
installation_date
from  bigquery-public-data.san_francisco.bikeshare_stations
where landmark = 'San Jose' and installation_date between '2013-01-01' AND '2014-01-01'
"""
df_query_04 = sq(query_04)
df_query_04



# Distinct titles
query_05 = """
select 
distinct
title
from  bigquery-public-data.san_francisco.film_locations
"""
df_query_05 = sq(query_05)
df_query_05


# Productions companies

query_06 = """
select 
distinct
production_company,
from  bigquery-public-data.san_francisco.film_locations
"""
df_query_06 = sq(query_06)
df_query_06


# Distributors
query_07 = """
select 
distinct
distributor
from  bigquery-public-data.san_francisco.film_locations
"""
df_query_07 = sq(query_07)
df_query_07


# Name of Directors
query_08 = """
select 
distinct
director
from  bigquery-public-data.san_francisco.film_locations
"""
df_query_08 = sq(query_08)
df_query_08


# Films produced and distributed by Metro Goldwyn Mayer company
# le agregue escrita
query_09 = """
select 
distinct
title,
release_year,
writer
from  bigquery-public-data.san_francisco.film_locations
where production_company =  'Metro-Goldwyn-Mayer (MGM)' and distributor = 'Metro-Goldwyn-Mayer (MGM)'
"""
df_query_09 = sq(query_09)
df_query_09



# Films produced and distributed by Warner Bros. Pictures
query_10 = """
select 
distinct
title,
release_year,
writer
from  bigquery-public-data.san_francisco.film_locations
where production_company =  'Warner Bros. Pictures' and distributor = 'Warner Bros. Pictures'
"""
df_query_10 = sq(query_10)
df_query_10



# Films from 1915 to 1950
query_11 = """
select 
distinct
release_year,
title
from  bigquery-public-data.san_francisco.film_locations
where release_year between 1915 and 1950
order by release_year
"""
df_query_11 = sq(query_11)
df_query_11


# Films from 2000 to 2018
query_12 = """
select 
distinct
release_year,
title
from  bigquery-public-data.san_francisco.film_locations
where release_year between 2000 and 2018
order by release_year
"""
df_query_12 = sq(query_12)
df_query_12



# Types of incidents with no. (count) of instances(in descending order)
query_13 = """
select 
distinct
category,
count(unique_key) as incidents
from  bigquery-public-data.san_francisco.sfpd_incidents
group by category
order by incidents desc
"""
df_query_13 = sq(query_13)
df_query_13



# Types of Resolution of crime recorded (descending order)

query_14 = """
select 
resolution,
count(resolution) number
from  bigquery-public-data.san_francisco.sfpd_incidents
group by resolution
order by number desc
"""
df_query_14 = sq(query_14)
df_query_14

df_query_14.set_index('resolution', inplace = True)
df_query_14.head().plot(kind = 'barh', figsize = (12,6), color = 'cyan')



# Incidents by day of the week

query_15 = """
select 
dayofweek,
count(unique_key) as incidents
from  bigquery-public-data.san_francisco.sfpd_incidents
group by dayofweek
order by incidents
"""
df_query_15 = sq(query_15)
df_query_15



# Incidents of crime by PD district

query_16 = """
select 
distinct
pddistrict,
count(unique_key) as incidents
from  bigquery-public-data.san_francisco.sfpd_incidents
group by pddistrict
order by incidents desc
"""
df_query_16 = sq(query_16)
df_query_16



# Incidents by year

query_17 = """
select 
extract(year from timestamp) as year,
count(unique_key) as incidents
from  bigquery-public-data.san_francisco.sfpd_incidents
group by year
order by incidents
"""
df_query_17 = sq(query_17)
df_query_17

# Line chart showing variation in the no. of incidents by year
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

df_query_17.set_index('year', inplace = True)
df_query_17.drop(index = 2018, inplace = True)
plt.plot(df_query_17.index, '-o')

















