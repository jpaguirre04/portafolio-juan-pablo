# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 11:38:05 2025

@author: Juan Pablo Aguirre
"""

import sqlite3
import pandas as pd


# credit_record
# https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction?select=credit_record.csv

con = sqlite3.connect('db_ccap.db')
df1 = pd.read_csv('ar.csv')
df2 = pd.read_csv('cr.csv')


df1.to_sql('ar', con, if_exists='replace', index=False)
df2.to_sql('cr', con, if_exists='replace', index=False)


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
from ar
limit 100;
"""
df_0 = sq(query_0)
# df_0.columns


query_00 = """
select
*
from cr
limit 100;
"""
df_00 = sq(query_00)
# df_00.columns


"""
# 1.-
Encuentra el número promedio de hijos que tienen los solicitantes de tarjetas 
de crédito que son propietarios de una casa (Flag_own_realty = 1) y que 
tienen un ingreso total anual superior a $50,000.
"""

query_1 = """
select
avg(cnt_children) media_ninos
from ar
where Flag_own_realty = 'Y' and amt_income_total > 50000
""" 
df_1 = sq(query_1)
df_1


"""
# 2.-
Encuentra el número de solicitantes de tarjetas de crédito que tienen un 
teléfono de trabajo registrado (Flag_work_phone = 1) y que tienen un 
nivel de educación de "Secondary" o "Higher education".
"""

query_2 = """
select
count(*) as solicitantes
from ar
where flag_work_phone = 1 and  
name_education_type in ('Secondary', 'Higher education')
""" 
df_2 = sq(query_2)
df_2


"""
# 3.-
Encuentra el número de registros de crédito que tienen un estado de "C" 
(suponiendo que "C" representa un estado de crédito específico, como 
 "Cerrado" o "Cancelado").
"""

query_3 = """
select
count(*) as numero_registros
from cr
where status = 'C'
""" 
df_3 = sq(query_3)
df_3



"""
# 4.-
¿Cuál es el ingreso total promedio (`Amt_income_total`) para cada tipo 
de ingreso (`Name_income_type`) en la tabla `application_record`?
"""

query_4 = """
select
name_income_type,
avg(Amt_income_total) as ingreso_promedio
from ar
group by name_income_type
""" 
df_4 = sq(query_4)
df_4



"""
# 5.-
¿Cuál es el número promedio de hijos (`Cnt_children`) para cada estado 
civil (`Name_family_status`) en la tabla `application_record`?
"""

query_5 = """
select
a.name_family_status,
avg(a.cnt_children) as promedio_hijos
from ar a
join cr c on a.id = c.id
group by a.name_family_status
""" 
df_5 = sq(query_5)
df_5


"""
# 6.-
¿Cuántos clientes tienen un ingreso total (`Amt_income_total`) mayor a 
500,000 y son propietarios de una vivienda (`Flag_own_realty` = 'Y')?
"""

query_6 = """
select
count(*) as clientes_solicitudes
from ar
where amt_income_total > 500000 and flag_own_realty = 'Y'
""" 
df_6 = sq(query_6)
df_6


"""
# 7.-
¿Cuál es el tipo de ocupación (`Occupation_type`) más común entre los 
clientes que tienen un teléfono de trabajo (`Flag_work_phone` = '1')?
"""

query_7 = """
select
occupation_type,
count(*) as frecuencia
from ar
where flag_work_phone = 1
group by occupation_type
order by frecuencia desc
limit 1;
""" 
df_7 = sq(query_7)
df_7



"""
# 8.-
Encuentra los 10 clientes (`Id`) con mayor ingreso total (`Amt_income_total`) 
que tengan un crédito aprobado (`Status` = '0' o 'C') en la tabla 
`credit_record` y que también tengan un nivel de educación superior 
(`Name_education_type` = 'Higher education'). Muestra el `Id`, 
el ingreso total y el número de créditos aprobados para cada cliente.
"""

query_8 = """
select
a.id,
sum(a.amt_income_total) as ingreso_total,
count(*) as numero_creditos_aprobados
from ar a
join cr c on a.id = c.id
where c.status in ('0', 'C') and a.name_education_type = 'Higher education'
group by a.id
order by numero_creditos_aprobados desc
limit 10;
""" 
df_8 = sq(query_8)
df_8



"""
# 9.-
Encuentra los clientes (`Id`) que tienen un patrón de pago irregular en sus
créditos. Un patrón de pago irregular se define como un cliente que tiene
al menos 3 créditos con estado diferente a '0' o 'C' (aprobado) en un
período de 6 meses consecutivos en la tabla `credit_record`. Muestra 
el `Id` del cliente, el número de créditos con problemas de pago y 
el rango de fechas (meses) en los que se produjeron estos problemas.
"""

query_9 = """
with pagos_irregulares as(
        select
        id,
        min(months_balance) as minimo,
        max(months_balance) as maximo,
        status,
        count(*) as numero_creditos
        from cr
        group by id
        )
select
id,
numero_creditos,
(maximo - minimo)  as rango
from pagos_irregulares
where status in ('0', 'C') and (maximo - minimo) >= 6
""" 
df_9 = sq(query_9)
df_9




"""
# 10.-
Encuentra el promedio de ingresos (`Amt_income_total`) por tipo de 
ocupación (`Occupation_type`) para los clientes que tienen un crédito 
aprobado (`Status` = '0' o 'C') en la tabla `credit_record`. Muestra 
el tipo de ocupación y el promedio de ingresos.
"""

query_10 = """
select
a.occupation_type,
avg(a.amt_income_total) as total
from ar a
join cr c on a.id = c.id
where c.status in ('0', 'C') and a.occupation_type not in ('None')
group by a.occupation_type
""" 
df_10 = sq(query_10)
df_10





"""
# 11.-
Encuentra los clientes que tienen un aumento en su ingreso total 
(`Amt_income_total`) en relación con su edad (`Days_birth`). 
Especificamente, busca clientes que tengan un ingreso total mayor 
que el promedio de ingresos de personas de su misma edad
(calculada en años). Muestra el `Id`, la edad y el ingreso 
total de estos clientes.
"""

query_11 = """
with years as(
        select
        id,
        -(days_birth)/365 as edad,
        amt_income_total
        from ar
        ),
     ingreso_medio_edad as(
         select
         edad,
         avg(amt_income_total) as ingreso_medio
         from years
         group by edad
         )
select
id,
edad,
amt_income_total
from years
where amt_income_total > (select ingreso_medio from ingreso_medio_edad)
""" 
df_11 = sq(query_11)
df_11




"""
# 15.-
Encuentra los tipos de ocupación (`Occupation_type`) que tienen una mayor 
proporción de clientes con ingresos altos (`Amt_income_total` > 50000) y 
que también tienen una mayor cantidad de hijos (`CNT_children`). Además, 
muestra la cantidad de clientes que tienen un crédito aprobado 
(`Status` = '0' o 'C') en la tabla `credit_record`.
"""

query_15 = """
with clientes as(
        select
        id,
        count(*) as clientes_aprobados
        from cr
        where status in ('0', 'C')
        group by id
        ) 
select
a.occupation_type,
sum(case when amt_income_total > 50000 then 1 end) /
(select count(*) from ar) as proporcion,
c.clientes_aprobados,
sum(cnt_children) as cantidad_hijos
from ar a
join clientes c on a.id = c.id
group by a.occupation_type
order by cantidad_hijos
limit 1;
""" 
df_15 = sq(query_15)
df_15



"""
# 16.-
Encuentra los clientes (`Id`) que tienen un patrón de pago irregular en 
sus créditos durante un período de 12 meses consecutivos. Un patrón de 
pago irregular se define como un cliente que tiene al menos 2 créditos 
con estado '2' (retraso de pago) o '3' (pago parcial) en la tabla 
`credit_record`. Muestra el `Id` del cliente, el número de créditos 
con problemas de pago y el rango de fechas (meses) en los que se 
produjeron estos problemas.

*Desafío:*

Utiliza funciones de ventana o subconsultas para identificar los períodos 
de 12 meses consecutivos y calcular el número de créditos con problemas 
de pago.

*Requisitos:*

1. Identifica los períodos de 12 meses consecutivos para cada cliente.
2. Calcula el número de créditos con problemas de pago (estado '2' o '3') 
en cada período.
3. Muestra solo los clientes que tienen al menos 2 créditos con problemas 
de pago en un período de 12 meses.
4. Muestra el rango de fechas (meses) en los que se produjeron los 
problemas de pago.
"""

query_16 = """
with meses as(
        select
        id,
        min(months_balance) as minimo,
        max(months_balance) as maximo,
        count(*) as numero_problemas_de_pago,
        status
        from cr
        where status in ('2', '3')
        group by id
        having count(*) >= 2
        )
select
id,
numero_problemas_de_pago,
(maximo - minimo) as rango
from meses
where (maximo - minimo) >= 12
order by numero_problemas_de_pago desc
""" 
df_16 = sq(query_16)
df_16





"""
# 17.-
Encuentra los clientes que tienen un teléfono de trabajo 
(`Flag_work_phone` = 1) y un ingreso total (`Amt_income_total`) mayor 
que el promedio de ingresos de su mismo tipo de ocupación 
(`Occupation_type`). Muestra el `Id` del cliente, el tipo de 
ocupación y el ingreso total.
"""

query_17 = """
select
id,
occupation_type,
amt_income_total
from ar 
where flag_work_phone = 1 and
amt_income_total > (select
                    avg(t.amt_income_total)
                    from ar as t
                    where ar.occupation_type = t.occupation_type
                    and flag_work_phone = 1
                    group by t.occupation_type)
""" 
df_17 = sq(query_17)
df_17





"""
# 18.-
Encuentra los 5 tipos de ocupación (`Occupation_type`) que tienen la mayor 
proporción de clientes con ingresos altos (`Amt_income_total` > 50000) y 
que también tienen una cantidad promedio de hijos (`Cnt_children`) mayor 
que la cantidad promedio de hijos de todos los clientes.
"""

query_18 = """
with aux as(
        select
        occupation_type,
        avg(cnt_children) as media_hijos,
        1.0 * sum(case when amt_income_total > 50000 then 1 end)/
        (select count(*) from ar) as prop
        from ar
        group by occupation_type
        )
select
occupation_type,
media_hijos,
prop
from aux
where media_hijos > (select avg(cnt_children) from ar) 
order by prop desc
limit 5;
""" 
df_18 = sq(query_18)
df_18




"""
#####################################################

#####################################################
"""


"""
# 19.-
Encuentra los clientes que tienen un ingreso total (`Amt_income_total`) 
que se encuentra en el percentil 90 o superior de su mismo tipo de 
ocupación (`Occupation_type`). Muestra el `Id` del cliente, el tipo 
de ocupación y el ingreso total.
"""

query_19 = """
with clientes as(
        select
        id,
        occupation_type,
        ntile(100) over(partition by occupation_type
                        order by amt_income_total desc) as percentil
        from ar
        group by occupation_type
        )
select
*
from clientes
where percentil >= 80
order by percentil desc
""" 
df_19 = sq(query_19)
df_19



"""
# 20.-
Encuentra los clientes que tienen un ingreso total (`Amt_income_total`) 
que se encuentra por encima del percentil 75 de todos los clientes con 
el mismo tipo de ingreso (`Name_income_type`) y que también tienen 
una cantidad de hijos (`Cnt_children`) mayor que 1. Muestra el `Id` 
del cliente, el tipo de ingreso y el ingreso total.
"""

query_20 = """
with clientes as(
        select
        id, 
        name_income_type,
        amt_income_total,
        ntile(100) over(partition by name_income_type
                        order by amt_income_total desc) as percentil
        from ar
        where cnt_children > 1
        )
select
*
from clientes
where percentil > 75
""" 
df_20 = sq(query_20)
df_20




"""
# 21.-
Encuentra los 3 tipos de ocupación (`occupation_type`) que tienen la mayor 
cantidad de clientes con ingresos altos (`amt_income_total` > 50000) y que 
también tienen una edad promedio (`days_birth / 365`) menor que 40 años.
 Muestra el tipo de ocupación y la cantidad de clientes con ingresos altos.

*Requisitos:*

1. Calcula la edad promedio de cada tipo de ocupación.

2. Filtra los tipos de ocupación que tienen una edad promedio menor 
que 40 años.

3. Cuenta la cantidad de clientes con ingresos altos 
(`amt_income_total` > 50000) para cada tipo de ocupación.

4. Muestra los 3 tipos de ocupación con la mayor cantidad de 
clientes con ingresos altos.
"""



query_21 = """
with edad_clientes as(
        select 
        occupation_type,
        count(*) as cantidad_clientes_ingresos_altos,
        avg(-(days_birth /365))  as edad_media
        from ar
        where amt_income_total > 50000 and occupation_type != 'None'
        group by occupation_type
        )
select
*
from edad_clientes
where edad_media < 40
order by  cantidad_clientes_ingresos_altos desc
limit 3;
""" 
df_21 = sq(query_21)
df_21



"""
# 22.-
Encuentra los clientes que tienen un ingreso total (`amt_income_total`) 
que es mayor que el ingreso promedio de su mismo tipo de ocupación 
(`occupation_type`) y que también tienen una cantidad de hijos 
(`cnt_children`) mayor que la cantidad promedio de hijos de todos 
los clientes. Muestra el `id` del cliente, el tipo de ocupación 
y el ingreso total.

*Requisitos:*

1. Calcula el ingreso promedio para cada tipo de ocupación.
2. Calcula la cantidad promedio de hijos de todos los clientes.
3. Filtra los clientes que tienen un ingreso total mayor que el 
ingreso promedio de su tipo de ocupación y que también tienen 
una cantidad de hijos mayor que la cantidad promedio de hijos.
"""


query_22 = """
with clientes as(
        select
        occupation_type,
        avg(amt_income_total) as ingreso_medio,
        avg(cnt_children) as media_hijos
        from ar
        where occupation_type != 'None'
        group by occupation_type
        )
select
a.id,
a.occupation_type,
a.amt_income_total
from ar a
where a.amt_income_total > (select
                          c.ingreso_medio
                          from clientes c
                          where a.occupation_type = c.occupation_type)
and a.cnt_children > (select
                      media_hijos
                      from clientes  c
                      where a.occupation_type = c.occupation_type)
""" 
df_22 = sq(query_22)
df_22





"""
# 23.-
Quieres encontrar los 10 tipos de ocupación más comunes entre los 
clientes que tienen un ingreso total mayor que el promedio y que 
tienen un valor de "0" en la columna "STATUS" de la tabla credit_record, 
considerando que "0" indica un buen historial crediticio.
"""

query_23 = """
select
ar.occupation_type,
count(*) frecuencia
from ar 
join (select
      id
      from cr
      where status in ('0')
      ) as c on c.id = ar.id
where ar.amt_income_total > (select 
                             avg(amt_income_total) 
                             from ar)
and occupation_type != 'None'
group by ar.occupation_type
order by count(*) desc
limit 10;
""" 
df_23 = sq(query_23)
df_23




"""
# 24.-
Quieres encontrar los 5 tipos de educación más comunes entre 
los clientes que tienen un ingreso total mayor que el promedio de 
ingresos de los clientes que tienen hijos (Cnt_children > 0) y
que no tienen un automóvil (Flag_own_car = 'N').
"""

query_24 = """
select
name_education_type,
count(*) frecuencia
from ar
where amt_income_total > (select
                         avg(amt_income_total)
                         from ar
                         where cnt_children > 0 and
                         flag_own_car = 'N'
                         )
group by name_education_type
order by count(*) desc
limit 5;
""" 
df_24 = sq(query_24)
df_24





"""
# 25.-
Quieres analizar la relación entre el tipo de ingreso y el promedio de 
ingresos de los clientes que tienen un automóvil y una casa. Para ello, 
deseas calcular el promedio de ingresos para cada tipo de ingreso y 
clasificarlos en tres categorías: "Alto" si el promedio de ingresos 
es mayor que 1,5 veces el promedio general de ingresos, "Medio" si 
está entre 0,75 y 1,5 veces el promedio general de ingresos, y "Bajo" 
si es menor que 0,75 veces el promedio general de ingresos.

*Tabla:* `application_record` (ar)

*Columnas:* `Name_income_type`, `Amt_income_total`, `Flag_own_car`, 
`Flag_own_realty`

*Requisitos:*

- Utilizar una consulta con `WITH` para calcular el promedio general de
 ingresos.
- Utilizar `INNER JOIN` para combinar la tabla `application_record` 
con una tabla derivada que contenga el promedio de ingresos para 
cada tipo de ingreso.
- Utilizar `CASE` para clasificar los tipos de ingreso en las tres 
categorías mencionadas.
- Calcular el promedio de ingresos para cada tipo de ingreso y categoría.
"""


query_25 = """
with ingreso_promedio as(
        select
        name_income_type,
        avg(amt_income_total) as ingreso_medio
        from ar
        where flag_own_car = 'Y' and flag_own_realty = 'Y'
        group by name_income_type
        )
select
a.name_income_type,
case
    when i.ingreso_medio < 0.75 * (select avg(a.amt_income_total) from ar) then 'bajo'
    when i.ingreso_medio < 1.5 * (select avg(a.amt_income_total) from ar) 
    and i.ingreso_medio > 0.75 * (select avg(a.amt_income_total) from ar) then 'medio' 
    else 'alto'
end as rango_ingreso
from ar a
inner join ingreso_promedio i on a.name_income_type = i.name_income_type
""" 
df_25 = sq(query_25)
df_25




"""
# 26.-
Desafío:* Quieres analizar la relación entre la edad de los clientes y su 
tipo de ingreso. Para ello, deseas calcular la edad promedio de los clientes 
para cada tipo de ingreso y clasificarlos en tres categorías: "Joven" 
(menor de 30 años), "Adulto" (entre 30 y 60 años) y "Mayor" (mayor de 60 años).

*Pistas:*

- La columna `Days_birth` representa el número de días desde la fecha 
de nacimiento hasta la fecha actual.
- Para calcular la edad en años, puedes dividir el número de días por 365.
- Utiliza un `CASE` statement para clasificar a los clientes en las tres 
categorías de edad.

*Tu turno:* Intenta resolver el desafío y te ayudaré a revisar tu consulta.
"""

query_26 = """
with ingreso as(
        select
        name_income_type,
        -(days_birth)/365 as edad
        from ar
        group by name_income_type
        )
select
name_income_type,
case 
    when edad <= 30 then 'joven'
    when edad > 30 and edad <= 60 then 'adulto'
    else 'mayor'
end  as categoria 
from ingreso
""" 
df_26 = sq(query_26)
df_26



