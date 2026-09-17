# -*- coding: utf-8 -*-
"""
Created on Wed May  7 17:15:39 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit_risk_dataset
# https://www.kaggle.com/datasets/laotse/credit-risk-dataset?select=credit_risk_dataset.csv

con = sqlite3.connect('bd_cr.db')
df1 = pd.read_csv('crd.csv')

df1.to_sql('crd', con, if_exists='replace', index=False)

con.commit()
# con.close()

table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", con)
# print(table)


def sq(q):
    return pd.read_sql_query(q, con).rename(columns = lambda x:x.replace(' ','_').capitalize())

##########################################################################################

query_0 = """
select
*
from crd
"""
df_0 = sq(query_0)
# df_0.columns



"""
01.- 
¿Cuál es el promedio de la tasa de interés (`Loan_int_rate`) para los 
préstamos (`Loan_amnt`) que superan los $10,000 y tienen una calificación 
(`Loan_grade`) de "A" o "B"?
"""


query_01 = """
select
avg(loan_int_rate) as promedio_tasa_interes
from crd
where loan_amnt > 10000 and
loan_grade in ('A', 'B')
"""
df_01 = sq(query_01)
# df_01



"""
02.- 
¿Cuáles son los propósitos de préstamo (`Loan_intent`) más comunes para 
los prestatarios que tienen un ingreso (`Person_income`) superior a 
$100,000 y una propiedad de vivienda (`Person_home_ownership`) de "OWN"?
"""

query_02 = """
select
loan_intent
from crd
where person_income > 10000 and 
person_home_ownership = 'OWN'
group by loan_intent
order by count(*) desc
"""
df_02 = sq(query_02)
df_02


"""
03.- 
¿Cuál es la edad promedio (`Person_age`) de los prestatarios que tienen 
una tasa de interés (`Loan_int_rate`) mayor que el 10%?
"""

query_03 = """
select
avg(person_age) as edad_promedio
from crd
where loan_int_rate > 10
"""
df_03 = sq(query_03)
df_03



"""
04.- 
¿Cuántos prestatarios tienen un historial crediticio 
(`Cb_person_cred_hist_length`) mayor que 10 años y un ingreso 
(`Person_income`) superior a $50,000?
"""

query_04 = """
select
count(*) as cuantos
from crd
where Cb_person_cred_hist_length > 10 and 
person_income > 50000
"""
df_04 = sq(query_04)
df_04



"""
05.- 
¿Cuál es la calificación de préstamo (`Loan_grade`) que tiene la mayor 
tasa de incumplimiento (`Loan_status` = 'Default') en comparación con 
el número total de préstamos de esa calificación?
"""

query_05 = """
with clases as(
        select
        loan_grade,
        count(*) as prestamos
        from crd
        group by loan_grade
        )
select
t1.loan_grade,
count(*) / t2.prestamos as tasa_imcumplimientos 
from crd as t1
join clases as t2 on t1.loan_grade = t2.loan_grade
where t1.loan_status = 1
group by t1.loan_grade
order by tasa_imcumplimientos desc
limit 1;
"""
df_05 = sq(query_05)
df_05



query_05_b = """
with defaults as(
        select
        loan_grade,
        count(*) as defaults_count
        from crd
        where loan_status = 1
        group by loan_grade
        ),
     totals as(
         select
         loan_grade,
         count(*) as total_count
         from crd
         group by loan_grade
         )
select
d.loan_grade,
(d.defaults_count * 1.0 / t.total_count) as tasa_incumplimiento
from defaults d     
join totals as t on d.loan_grade = t.loan_grade
order by tasa_incumplimiento desc
limit 1;
"""
df_05_b = sq(query_05_b)
df_05_b



"""
06.- 
¿Cuál es el propósito de préstamo (`Loan_intent`) más común para los 
prestatarios que tienen un ingreso (`Person_income`) superior a $100,000 
y una calificación de préstamo (`Loan_grade`) de 'A' o 'B'?
"""

query_06 = """
select
loan_intent
from crd
where person_income > 100000 and loan_grade in ('A', 'B')
group by loan_intent
order by count(*) desc
limit 1;
"""
df_06 = sq(query_06)
df_06




"""
07.- 
Encuentra los 3 propósitos de préstamo (`Loan_intent`) más comunes para 
cada calificación de préstamo (`Loan_grade`), y muestra los resultados 
en una tabla con las siguientes columnas:
"""

query_07 = """
select
loan_grade,
loan_intent,
count(*),
rank() over(partition by loan_grade order by count(*) desc) as ranking
from (select
      loan_grade,
      loan_intent,
      count(*)
      from crd
      group by loan_grade, loan_intent
      )
"""
df_07 = sq(query_07)
df_07



query_07_b = """
with ranked_loans as(
        select
        loan_grade,
        loan_intent,count(*) as count,
        rank() over(partition by loan_grade order by count(*) desc) as ranking
        from crd
        group by loan_grade, loan_intent
        )
select
loan_grade,
MAX(CASE WHEN ranking = 1 THEN loan_intent END) as Top_1_Loan_intent,
MAX(CASE WHEN ranking = 1 THEN count END) as Top_1_Count,
MAX(CASE WHEN ranking = 2 THEN loan_intent END) as Top_2_Loan_intent,
MAX(CASE WHEN ranking = 2 THEN count END) as Top_2_Count,
MAX(CASE WHEN ranking = 3 THEN loan_intent END) as Top_3_Loan_intent,
MAX(CASE WHEN ranking = 3 THEN count END) as Top_3_Count
from ranked_loans
group by loan_grade
"""
df_07_b = sq(query_07_b)
df_07_b




"""
08.- 
Encuentra los propósitos de préstamo (`Loan_intent`) que tienen una 
tasa de incumplimiento (`Loan_status` = 'Default') superior a la media 
de todos los propósitos de préstamo. Muestra los resultados en una 
tabla con las siguientes columnas:
"""

query_08 = """
with todos as (
        select
        loan_intent,
        count(*) as prestamos
        from crd
        group by loan_intent
        ),
    defaulti as (
        select
        loan_intent,
        count(*) as incumplimientos
        from crd
        where loan_status = 1
        group by loan_intent
        ),
     tasas as(
         select
         d.loan_intent,
         d.incumplimientos / t.prestamos as tasa_incumplimiento
         from todos as t
         join defaulti as d on t.loan_intent = d.loan_intent
       )
select
t.loan_intent,
t.tasa_incumplimiento,
(select avg(tasa_incumplimiento) from tasas) as media_global
from tasas as t
where  tasa_incumplimiento > (select avg(tasa_incumplimiento) from tasas)   
"""
df_08 = sq(query_08)
df_08





"""
# 9.-
Identificar los clientes que tienen un historial de incumplimiento de pagos 
y cuyo ingreso promedio es mayor que el ingreso promedio de todos los 
clientes.
"""


query_09 = """
with clientes_incumplimiento as(
        select
        person_age,
        person_income
        from crd
        where Cb_person_default_on_file = 'Y' and
        person_income > (select avg(person_income) from crd)
        )
select
*
from clientes_incumplimiento
"""
df_09 = sq(query_09)
df_09



"""
# 10.-
Identificar los clientes que tienen un historial de incumplimiento de 
pagos, cuyo ingreso es mayor que el promedio de todos los clientes, y 
asignarles un número de fila según su edad.
"""


query_10 = """
select
person_age,
person_income,
row_number() over(order by person_age asc) as fila
from crd
where Cb_person_default_on_file = 'Y' and 
      person_income > (select avg(person_income) from crd)

"""
df_10 = sq(query_10)
df_10




"""
# 11.-
Identificar los clientes que tienen un historial de incumplimiento de 
pagos y que han solicitado préstamos de más de $10,000. Asignarles una 
categoría según su ingreso en relación con el promedio de ingresos de 
todos los clientes que han solicitado préstamos de más de $10,000. 
Además, asignar un ranking a cada cliente según su ingreso en 
orden descendente.
"""


query_11 = """
select
person_age,
person_income,
case
     when person_income > (select avg(person_income) from crd where loan_amnt > 10000) then 'ingreso_alto'
     when person_income < (select avg(person_income) from crd where loan_amnt > 10000) then 'ingreso_bajo'
     else 'ingreso_medio'
end as categoria_ingreso
from crd
where cb_person_default_on_file = 'Y' and loan_amnt > 10000
"""
df_11 = sq(query_11)
df_11




"""
# 12.-
Ahora que hemos analizado la distribución de los clientes y hemos 
identificado los clientes con un historial de incumplimiento de pagos, 
vamos a segmentar a los clientes según sus características demográficas 
y de comportamiento.

*Pregunta:* ¿Cuáles son los segmentos de clientes que tienen un mayor
 riesgo crediticio y qué características los definen?

Para responder a esta pregunta, podemos utilizar técnicas de segmentación, 
como clustering o regresión logística, para identificar grupos de 
clientes con características similares.
"""


query_12 = """
with clases as(
         select
         person_income,
         person_age,
         case
             when person_age < 30 and person_income < 500000 then 'jovenes_con_ingresos_bajos'
             when person_age >= 30 and person_age < 50 and person_income >= 500000 and person_income < 1000000 then 'adultos_con_ingreso_medio'
             when person_age >= 50 and person_income >= 10000 then 'adulto_con_ingreso_alto'
             else 'otros'
         end as segmento,
         cb_person_default_on_file
         from crd
        )
select
segmento,
count(*) as cantidad_de_clientes,
sum(case when cb_person_default_on_file = 'Y' then 1 else 0 end) as cantidad_de_clientes_con_incumplimiento
from clases
group by segmento
order by cantidad_de_clientes
"""
df_12 = sq(query_12)
df_12



"""
# 13.-
¿Cuál es el propósito de préstamo (`Loan_intent`) que tiene la mayor cantidad 
de préstamos aprobados (`Loan_status = 0`) para personas con un ingreso 
(`Person_income`) superior a $100,000?
"""


query_13 = """
select
loan_intent
from crd
where loan_status = 0 and person_income > 100000
group by loan_intent 
order by count(*) desc
limit 1;
"""
df_13 = sq(query_13)
df_13












