# -*- coding: utf-8 -*-
"""
Created on Sat May 31 20:59:49 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd

# https://www.kaggle.com/datasets/ruthvikrajamv/home-insurance-dataset?select=Stable+Home+Insurance.csv

con = sqlite3.connect('db_insurance_home.db')
df1 = pd.read_csv('fd.csv')
df2 = pd.read_csv('shi.csv')


df1.to_sql('fd', con, if_exists='replace', index=False)
df2.to_sql('shi', con, if_exists='replace', index=False)


con.commit()
# con.close()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", con)
# print(table)

def sq(q):
    return pd.read_sql_query(q, con).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

df1.columns



"""
# 1.-
¿Cuál es el promedio de la prima anual de seguro (`LAST_ANN_PREM_GROSS`) 
para las propiedades que tienen un valor asegurado de edificios 
(`SUM_INSURED_BUILDINGS`) mayor a 200,000 y que también tienen un 
valor asegurado de contenido (`SUM_INSURED_CONTENTS`) 
mayor a 50,000?
"""

query_1 = """
select
avg(LAST_ANN_PREM_GROSS) as promedio_prima_anual
from fd
where SUM_INSURED_BUILDINGS > 200000 and SUM_INSURED_CONTENTS > 50000
""" 
df_1 = sq(query_1)
df_1


"""
# 2.-
¿Cuántas propiedades tienen un estado de póliza (`POL_STATUS`) de 
"Renewal" y un método de pago (`PAYMENT_METHOD`) de "Direct Debit"?
"""

query_2 = """
select
count(*) as cantidad_propiedades
from fd
where payment_method = 'Direct Debit' and pol_status = 'Renewal'
""" 
df_2 = sq(query_2)
df_2


"""
# 3.-
¿Cuál es el promedio de la suma asegurada de edificios 
(`SUM_INSURED_BUILDINGS`) para las propiedades que tienen un 
tipo de propiedad (`PROP_TYPE`) de "Detached" o "Semi-Detached"?
"""

query_3 = """
select
avg(SUM_INSURED_BUILDINGS) as promedio_edificios
from fd
where prop_type in (1,2,19)
""" 
df_3 = sq(query_3)
df_3



"""
# 4.-
¿Cuál es el número total de propiedades que tienen un valor asegurado 
de edificios (`SUM_INSURED_BUILDINGS`) mayor a 250,000 y que también 
tienen un addon de seguro de hogar (`HOME_EM_ADDON_POST_REN`) 
igual a "Yes"?
"""

query_4 = """
select
count(*) as cantidad_propiedades
from fd
where SUM_INSURED_BUILDINGS > 250000 and 
HOME_EM_ADDON_POST_REN = 'Y'    
""" 
df_4 = sq(query_4)
df_4



"""
# 5.-
¿Cuál es el promedio de la prima anual de seguro (`LAST_ANN_PREM_GROSS`) 
para cada tipo de propiedad (`PROP_TYPE`), considerando solo las propiedades 
que tienen un valor asegurado de edificios (`SUM_INSURED_BUILDINGS`) mayor 
a 200,000 y que también tienen un addon de seguro de hogar 
(`HOME_EM_ADDON_POST_REN`) igual a "Y"? Ordena los resultados por 
el promedio de la prima anual de seguro en orden descendente.
"""

query_5 = """
with renombrar as(
        select
        LAST_ANN_PREM_GROSS,
        case 
           when PROP_TYPE > 0 and PROP_TYPE <= 20 then 'tipo_bajo'
           when PROP_TYPE > 20 and PROP_TYPE <= 50 then 'tipo_medio'
           else 'tipo_alto'
        end as prop_tipo,
        SUM_INSURED_BUILDINGS,
        HOME_EM_ADDON_POST_REN
        from fd        
        )
select
prop_tipo,
avg(last_ann_prem_gross) as promedio_prima_anual
from renombrar
where SUM_INSURED_BUILDINGS > 200000 and HOME_EM_ADDON_POST_REN = 'Y' 
group by prop_tipo
order by promedio_prima_anual desc
""" 
df_5 = sq(query_5)
df_5





"""
# 6.-
 ¿Cuál es el porcentaje de propiedades que tienen un addon de seguro de 
hogar (`HOME_EM_ADDON_POST_REN`) igual a "Y" para cada tipo de propiedad 
(`PROP_TYPE`), considerando solo las propiedades que tienen un valor 
asegurado de edificios (`SUM_INSURED_BUILDINGS`) mayor a 100,000? 
Ordena los resultados por el porcentaje en orden descendente.
"""

query_6 = """
with renombrar as(
        select
        LAST_ANN_PREM_GROSS,
        case 
           when PROP_TYPE > 0 and PROP_TYPE <= 20 then 'tipo_bajo'
           when PROP_TYPE > 20 and PROP_TYPE <= 50 then 'tipo_medio'
           else 'tipo_alto'
        end as prop_tipo,
        SUM_INSURED_BUILDINGS,
        HOME_EM_ADDON_POST_REN
        from fd        
        )
select
prop_tipo,
1.0* sum(case when HOME_EM_ADDON_POST_REN = 'Y' then 1 end) / count(*)
as porcentaje
from renombrar
where SUM_INSURED_BUILDINGS > 100000
group by prop_tipo
order by porcentaje desc
""" 
df_6 = sq(query_6)
df_6



"""
# 7.-
¿Cuál es el tipo de propiedad (`PROP_TYPE`) con mayor promedio de prima 
anual de seguro (`LAST_ANN_PREM_GROSS`) para las propiedades que tienen 
un valor asegurado de edificios (`SUM_INSURED_BUILDINGS`) mayor a 250,000 
y que también tienen un addon de seguro de hogar (`HOME_EM_ADDON_POST_REN`) 
igual a "Y"? 
"""

query_7 = """
with renombrar as(
        select
        LAST_ANN_PREM_GROSS,
        case 
           when PROP_TYPE > 0 and PROP_TYPE <= 20 then 'tipo_bajo'
           when PROP_TYPE > 20 and PROP_TYPE <= 50 then 'tipo_medio'
           else 'tipo_alto'
        end as prop_tipo,
        SUM_INSURED_BUILDINGS,
        HOME_EM_ADDON_POST_REN
        from fd        
        )
select
prop_tipo,
avg(LAST_ANN_PREM_GROSS) as promedio_de_prima
from renombrar
where SUM_INSURED_BUILDINGS > 250000 and HOME_EM_ADDON_POST_REN = 'Y'
group by prop_tipo
order by promedio_de_prima desc
limit 1;
""" 
df_7 = sq(query_7)
df_7


