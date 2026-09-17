# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:07:44 2024

@author: Juan Pablo Aguirre
"""

# https://www.kaggle.com/datasets/bigquery/ebi-chembl/data

import os
from google.cloud import bigquery
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'probar_este.json'

client = bigquery.Client()

# Construct a reference to the "san_francisco" dataset
dataset_ref = client.dataset("ebi_chembl", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)

# Construct a reference to the "bikeshare_trips" table
table_ref_1 = dataset_ref.table("tissue_dictionary_23")
# API request - fetch the table
table_1 = client.get_table(table_ref_1)
# Preview the first five lines of the table
tabla_1 = client.list_rows(table_1, max_results=5).to_dataframe()      



# query function, función de query
def sq(query_a):
      return client.query(query_a).result().to_dataframe()

"""
#########---- table: country_series_definitions -----########
"""

# ver después
# https://www.kaggle.com/code/goha2097/ml-gorin-petrushenko


query_01 = """
select 
pref_name
from  bigquery-public-data.ebi_chembl.tissue_dictionary_23
limit 20
"""
df_query_01 = sq(query_01)
df_query_01


query_02_0 = """
select
*
from `patents-public-data.ebi_chembl.ligand_eff_23`
inner join `patents-public-data.ebi_chembl.activities_23`
using(`activity_id`)
limit 100000;
"""
df_query_02_0 = sq(query_02_0)
df_query_02_0


query_02_1 = """
select
*
from `patents-public-data.ebi_chembl.ligand_eff_23`
limit 100000;
"""
df_query_02_1 = sq(query_02_1)
df_query_02_1


query_02_2 = """
SELECT bei, molregno, tid
            FROM 
                `patents-public-data.ebi_chembl.ligand_eff_23`
                    INNER JOIN
                `patents-public-data.ebi_chembl.activities_23`
                    USING (`activity_id`)
                    INNER JOIN
                `patents-public-data.ebi_chembl.assays_23`
                    USING (`assay_id`)
                    INNER JOIN
                `patents-public-data.ebi_chembl.target_dictionary_23`
                    USING (`tid`)
                    INNER JOIN
                `patents-public-data.ebi_chembl.target_type_23`
                    USING (`target_type`)
            WHERE bei IS NOT NULL AND parent_type = 'PROTEIN'"""
df_query_02_2 = sq(query_02_2)
df_query_02_2




