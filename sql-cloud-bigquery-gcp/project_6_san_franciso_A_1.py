# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 19:52:12 2024

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
table_ref_1 = dataset_ref.table("bikeshare_status")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=5).to_dataframe()      

tabla_1.columns


# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()

"""
#########---- table: country_series_definitions -----########
"""

query_01 = """
select 
station_id,
avg(bikes_available) as mean_bikes_available,
avg(docks_available) as mean_docks_available,
min(time) as minimo,
max(time) as maximo
from  bigquery-public-data.san_francisco.bikeshare_status
group by station_id
order by station_id
"""
df_query_01 = sq(query_01)
df_query_01



query_02 = """
select 
*
from  bigquery-public-data.san_francisco.311_service_requests
limit 1000;
"""
df_query_02 = sq(query_02)
df_query_02


# revisar estos notebooks, para construir mi último proyecvto en sql biquery

# ver después
# 2 https://www.kaggle.com/code/paultimothymooney/how-to-query-the-san-francisco-open-data
# 3 https://www.kaggle.com/code/desaivaibhav1995/san-francisco-open-data-bigquery
# 4 https://www.kaggle.com/code/shubhamsugara22/analytics-functions-scratchpad


"""
# este es similar al curso de eficiencia de query 
# https://www.kaggle.com/code/moranp/sql-adv-4/notebook
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



#choosing all columns VS choosing only the columns we need
star_query = "SELECT * FROM `bigquery-public-data.github_repos.contents`"
show_amount_of_data_scanned(star_query)

basic_query = "SELECT size, binary FROM `bigquery-public-data.github_repos.contents`"
show_amount_of_data_scanned(basic_query)


# read more VS less data
more_data_query = """
                  SELECT MIN(start_station_name) AS start_station_name,
                      MIN(end_station_name) AS end_station_name,
                      AVG(duration_sec) AS avg_duration_sec
                  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
                  WHERE start_station_id != end_station_id 
                  GROUP BY start_station_id, end_station_id
                  LIMIT 10
                  """
df_more_data_query = sq(more_data_query)
df_more_data_query
show_amount_of_data_scanned(more_data_query)
show_time_to_run(more_data_query)

less_data_query = """
                  SELECT start_station_name,
                      end_station_name,
                      AVG(duration_sec) AS avg_duration_sec                  
                  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
                  WHERE start_station_name != end_station_name
                  GROUP BY start_station_name, end_station_name
                  LIMIT 10
                  """
df_less_data_query = sq(less_data_query)
df_less_data_query

show_amount_of_data_scanned(less_data_query)



#using 1:1/ N:1/ N:N Join 
big_join_query = """
                 SELECT repo,
                     COUNT(DISTINCT c.committer.name) as num_committers,
                     COUNT(DISTINCT f.id) AS num_files
                 FROM `bigquery-public-data.github_repos.commits` AS c,
                     UNNEST(c.repo_name) AS repo
                 INNER JOIN `bigquery-public-data.github_repos.files` AS f
                     ON f.repo_name = repo
                 WHERE f.repo_name IN ( 'tensorflow/tensorflow', 
                                       'facebook/react', 'twbs/bootstrap', 
                                       'apple/swift', 'Microsoft/vscode', 
                                       'torvalds/linux')
                 GROUP BY repo
                 ORDER BY repo
                 """
df_big_join_query = sq(big_join_query)
df_big_join_query

show_time_to_run(big_join_query)
show_amount_of_data_scanned(big_join_query)



small_join_query = """
                   WITH commits AS
                   (
                   SELECT COUNT(DISTINCT committer.name) AS num_committers, repo
                   FROM `bigquery-public-data.github_repos.commits`,
                       UNNEST(repo_name) as repo
                   WHERE repo IN ( 'tensorflow/tensorflow', 'facebook/react', 'twbs/bootstrap', 'apple/swift', 'Microsoft/vscode', 'torvalds/linux')
                   GROUP BY repo
                   ),
                   files AS 
                   (
                   SELECT COUNT(DISTINCT id) AS num_files, repo_name as repo
                   FROM `bigquery-public-data.github_repos.files`
                   WHERE repo_name IN ( 'tensorflow/tensorflow', 'facebook/react', 'twbs/bootstrap', 'apple/swift', 'Microsoft/vscode', 'torvalds/linux')
                   GROUP BY repo
                   )
                   SELECT commits.repo, commits.num_committers, files.num_files
                   FROM commits 
                   INNER JOIN files
                       ON commits.repo = files.repo
                   ORDER BY repo
                   """
df_small_join_query = sq(small_join_query)
df_small_join_query

show_time_to_run(small_join_query)
show_amount_of_data_scanned(small_join_query)





