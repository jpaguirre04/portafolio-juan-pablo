# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 12:47:48 2025

@author: Juan Pablo Aguirre
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# https://www.kaggle.com/datasets/kaggle/sf-salaries

conn = sqlite3.connect('sf_salaries.sqlite')
c = conn.cursor()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(table)


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################


query_0 = """
select
*
from salaries
"""
df_0 = sq(query_0)
# df_0.columns
df_0.info()
df_0['Basepay'] = pd.to_numeric(df_0['Basepay'], errors = 'coerce')
df_0['Year'] = pd.to_numeric(df_0['Year'], errors = 'coerce')
df_0.dtypes

df_0['Basepay'].describe()



"""
# 1.-
¿Cuáles son los empleados con un pago total mayor que el promedio de los 
empleados que trabajan esten entre el 2011 y 2012?
"""

query_1 = """
select
employeename,
year,
totalpay
from salaries
where totalpay > (select 
                  avg(totalpay) 
                  from salaries 
                  where year >= 2011 and year <= 2012)
"""
df_1 = sq(query_1)
df_1


"""
# 2.-
¿Cuáles son los 10 empleados con mayor pago total (Totalpay) en el año 2020, 
considerando solo aquellos que tienen un estatus de "Active" y que trabajan 
en la agencia "San Francisco"?
"""

query_2 = """
select
employeename,
jobtitle,
totalpay
from salaries
where year = 2020
and status = 'San Francisco'
order by Totalpay desc
limit 10;
"""
df_2 = sq(query_2)
df_2


