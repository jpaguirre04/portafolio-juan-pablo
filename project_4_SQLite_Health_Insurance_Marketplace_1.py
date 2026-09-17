# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 16:36:13 2025

@author: Juan Pablo Aguirre
"""


import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# https://www.kaggle.com/datasets/hhs/health-insurance-marketplace

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(table)


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

query_0 = """
select
*
from ServiceArea
"""
df_0 = sq(query_0)
# df_0.columns


query_1 = """
select
*
from PlanAttributes
limit 100;
"""
df_1 = sq(query_1)
# df_1.columns



"""
# 1.-
Identifica a los 3 estados con la mayor cantidad de planes de seguro de 
salud que ofrecen cobertura dental y tienen un promedio de primas 
mensuales superiores a $700. Además, solo considera los planes que 
tienen un rating de 4 o 5 estrellas y que están disponibles en áreas 
de servicio que cubren más del 50% del estado.
"""

query_1 = """
with planescoberturadental as(
        select
        pa.planid,
        pa.businessyear,
        sa.statecode,
        r.individualrate
        from planattributes pa
        inner join servicearea sa on pa.issuerid = sa.issuerid
        inner join rate r on pa.planid = r.planid
        where pa.dentalonlyplan = 'yes' and
              pa.Benefitpackageid = 4 or pa.Benefitpackageid = 5
        )
select
*
from planescoberturadental
"""
df_1 = sq(query_1)
df_1




