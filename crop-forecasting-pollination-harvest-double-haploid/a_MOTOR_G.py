# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 09:04:36 2022

@author: s1073533
"""


import pandas as pd
import numpy as np
import datetime
from datetime import date

orden = ['fecha_histórica', 'MATID_Ind', 'MAT_GENERATED', 'BARCD_IND', 'REGION_CODE_CONTINENT',
       'DESCRIPTION', 'unidades', 'sector', 'Maturity', 'codigo', 'FECHA_1',
       'periodo_f1', 'mes_año_f1', 'days_poli_est', 'FECHA_2_est', 'FECHA_2',
       'FECHA_POLI', 'tipo_poli', 'semana_B_est', 'mes_año_f2', 'periodo_f2',
       'days_cosecha_est', 'FECHA_3_est', 'FECHA_3', 'SEMANA_SIEMBRA_REAL',
       'SEMANA_FLORACION_ESTIMADA', 'SEMANA_FLORACION_REAL',
       'SEMANA_COSECHA_ESTIMADA', 'SEMANA_COSECHA_REAL', 'error_poli',
       'error_cosecha'
        ]


tabla96 = pd.read_excel('Silicon_Valley_02_09_2022.xlsx')
tabla96 = pd.DataFrame(tabla96)
tabla96['fecha_histórica'] = '2022-09-06'
tabla96 = tabla96[orden]


tabla97 = pd.read_excel('Silicon_Valley_06_09_2022.xlsx')
tabla97 = pd.DataFrame(tabla97)
tabla97['fecha_histórica'] = '2022-09-06'
tabla97 = tabla97[orden]


tabla98 = pd.read_excel('Silicon_Valley_09_09_2022.xlsx')
tabla98 = pd.DataFrame(tabla98)
tabla98['fecha_histórica'] = '2022-09-09'
tabla98 = tabla98[orden]


tabla99 = pd.read_excel('Silicon_Valley_13_09_2022.xlsx')
tabla99 = pd.DataFrame(tabla99)
tabla99['fecha_histórica'] = '2022-09-13'
tabla99 = tabla99[orden]


tabla100 = pd.read_excel('Silicon_Valley_20_09_2022.xlsx')
tabla100 = pd.DataFrame(tabla100)
tabla100['fecha_histórica'] = '2022-09-20'
tabla100 = tabla100[orden]


tabla101 = pd.read_excel('Silicon_Valley_27_09_2022.xlsx')
tabla101 = pd.DataFrame(tabla101)
tabla101['fecha_histórica'] = '2022-09-27'
tabla101 = tabla101[orden]


tabla102 = pd.read_excel('Silicon_Valley_30_09_2022.xlsx')
tabla102 = pd.DataFrame(tabla102)
tabla102['fecha_histórica'] = '2022-09-30'
tabla102 = tabla102[orden]


tabla103 = pd.read_excel('Silicon_Valley_04_10_2022.xlsx')
tabla103 = pd.DataFrame(tabla103)
tabla103['fecha_histórica'] = '2022-10-04'
tabla103 = tabla103[orden]


tabla104 = pd.read_excel('Silicon_Valley_07_10_2022.xlsx')
tabla104 = pd.DataFrame(tabla104)
tabla104['fecha_histórica'] = '2022-10-07'
tabla104 = tabla104[orden]


tabla105 = pd.read_excel('Silicon_Valley_11_10_2022.xlsx')
tabla105 = pd.DataFrame(tabla105)
tabla105['fecha_histórica'] = '2022-10-11'
tabla105 = tabla105[orden]


tabla106 = pd.read_excel('Silicon_Valley_14_10_2022.xlsx')
tabla106 = pd.DataFrame(tabla106)
tabla106['fecha_histórica'] = '2022-10-14'
tabla106 = tabla106[orden]


tabla107 = pd.read_excel('Silicon_Valley_18_10_2022.xlsx')
tabla107 = pd.DataFrame(tabla107)
tabla107['fecha_histórica'] = '2022-10-18'
tabla107 = tabla107[orden]


tabla108 = pd.read_excel('Silicon_Valley_21_10_2022.xlsx')
tabla108 = pd.DataFrame(tabla108)
tabla108['fecha_histórica'] = '2022-10-21'
tabla108 = tabla108[orden]


tabla109 = pd.read_excel('Silicon_Valley_25_10_2022.xlsx')
tabla109 = pd.DataFrame(tabla109)
tabla109['fecha_histórica'] = '2022-10-25'
tabla109 = tabla109[orden]


tabla110 = pd.read_excel('Silicon_Valley_28_10_2022.xlsx')
tabla110 = pd.DataFrame(tabla110)
tabla110['fecha_histórica'] = '2022-10-28'
tabla110 = tabla110[orden]


tabla111 = pd.read_excel('Silicon_Valley_02_11_2022.xlsx')
tabla111 = pd.DataFrame(tabla111)
tabla111['fecha_histórica'] = '2022-11-02'
tabla111 = tabla111[orden]


tabla112 = pd.read_excel('Silicon_Valley_04_11_2022.xlsx')
tabla112 = pd.DataFrame(tabla112)
tabla112['fecha_histórica'] = '2022-11-04'
tabla112 = tabla112[orden]


tabla113 = pd.read_excel('Silicon_Valley_08_11_2022.xlsx')
tabla113 = pd.DataFrame(tabla113)
tabla113['fecha_histórica'] = '2022-11-08'
tabla113 = tabla113[orden]


tabla114 = pd.read_excel('Silicon_Valley_11_11_2022.xlsx')
tabla114 = pd.DataFrame(tabla114)
tabla114['fecha_histórica'] = '2022-11-11'
tabla114 = tabla114[orden]


tabla115 = pd.read_excel('Silicon_Valley_15_11_2022.xlsx')
tabla115 = pd.DataFrame(tabla115)
tabla115['fecha_histórica'] = '2022-11-15'
tabla115 = tabla115[orden]


tabla116 = pd.read_excel('Silicon_Valley_18_11_2022.xlsx')
tabla116 = pd.DataFrame(tabla116)
tabla116['fecha_histórica'] = '2022-11-18'
tabla116 = tabla116[orden]


tabla117 = pd.read_excel('Silicon_Valley_09_12_2022.xlsx')
tabla117 = pd.DataFrame(tabla117)
tabla117['fecha_histórica'] = '2022-12-09'
tabla117 = tabla117[orden]


tabla118 = pd.read_excel('Silicon_Valley_13_12_2022.xlsx')
tabla118 = pd.DataFrame(tabla118)
tabla118['fecha_histórica'] = '2022-12-13'
tabla118 = tabla118[orden]


tabla119 = pd.read_excel('Silicon_Valley_16_12_2022.xlsx')
tabla119 = pd.DataFrame(tabla119)
tabla119['fecha_histórica'] = '2022-12-16'
tabla119 = tabla119[orden]


tabla120 = pd.read_excel('Silicon_Valley_20_12_2022.xlsx')
tabla120 = pd.DataFrame(tabla120)
tabla120['fecha_histórica'] = '2022-12-20'
tabla120 = tabla120[orden]


tabla121 = pd.read_excel('Silicon_Valley_23_12_2022.xlsx')
tabla121 = pd.DataFrame(tabla121)
tabla121['fecha_histórica'] = '2022-12-23'
tabla121 = tabla121[orden]


tabla122 = pd.read_excel('Silicon_Valley_27_12_2022.xlsx')
tabla122 = pd.DataFrame(tabla122)
tabla122['fecha_histórica'] = '2022-12-27'
tabla122 = tabla122[orden]


tabla123 = pd.read_excel('Silicon_Valley_30_12_2022.xlsx')
tabla123 = pd.DataFrame(tabla123)
tabla123['fecha_histórica'] = '2022-12-30'
tabla123 = tabla123[orden]


tabla124 = pd.read_excel('Silicon_Valley_03_01_2023.xlsx')
tabla124 = pd.DataFrame(tabla124)
tabla124['fecha_histórica'] = '2023-01-03'
tabla124 = tabla124[orden]


tabla125 = pd.read_excel('Silicon_Valley_06_01_2023.xlsx')
tabla125 = pd.DataFrame(tabla125)
tabla125['fecha_histórica'] = '2023-01-06'
tabla125 = tabla125[orden]


tabla126 = pd.read_excel('Silicon_Valley_10_01_2023.xlsx')
tabla126 = pd.DataFrame(tabla126)
tabla126['fecha_histórica'] = '2023-01-10'
tabla126 = tabla126[orden]


tabla127 = pd.read_excel('Silicon_Valley_13_01_2023.xlsx')
tabla127 = pd.DataFrame(tabla127)
tabla127['fecha_histórica'] = '2023-01-13'
tabla127 = tabla127[orden]



tabla128 = pd.read_excel('Silicon_Valley_17_01_2023.xlsx')
tabla128 = pd.DataFrame(tabla128)
tabla128['fecha_histórica'] = '2023-01-17'
tabla128 = tabla128[orden]


tabla129 = pd.read_excel('Silicon_Valley_20_01_2023.xlsx')
tabla129 = pd.DataFrame(tabla129)
tabla129['fecha_histórica'] = '2023-01-20'
tabla129 = tabla129[orden]


tabla130 = pd.read_excel('Silicon_Valley_24_01_2023.xlsx')
tabla130 = pd.DataFrame(tabla130)
tabla130['fecha_histórica'] = '2023-01-24'
tabla130 = tabla130[orden]


tabla131 = pd.read_excel('Silicon_Valley_27_01_2023.xlsx')
tabla131 = pd.DataFrame(tabla131)
tabla131['fecha_histórica'] = '2023-01-27'
tabla131 = tabla131[orden]


tabla132 = pd.read_excel('Silicon_Valley_31_01_2023.xlsx')
tabla132 = pd.DataFrame(tabla132)
tabla132['fecha_histórica'] = '2023-01-31'
tabla132 = tabla132[orden]


tabla133 = pd.read_excel('Silicon_Valley_03_02_2023.xlsx')
tabla133 = pd.DataFrame(tabla133)
tabla133['fecha_histórica'] = '2023-02-03'
tabla133 = tabla133[orden]


tabla134 = pd.read_excel('Silicon_Valley_07_02_2023.xlsx')
tabla134 = pd.DataFrame(tabla134)
tabla134['fecha_histórica'] = '2023-02-07'
tabla134 = tabla134[orden]


tabla135 = pd.read_excel('Silicon_Valley_10_02_2023.xlsx')
tabla135 = pd.DataFrame(tabla135)
tabla135['fecha_histórica'] = '2023-02-10'
tabla135 = tabla135[orden]


tabla136 = pd.read_excel('Silicon_Valley_14_02_2023.xlsx')
tabla136 = pd.DataFrame(tabla136)
tabla136['fecha_histórica'] = '2023-02-14'
tabla136 = tabla136[orden]


tabla137 = pd.read_excel('Silicon_Valley_17_02_2023.xlsx')
tabla137 = pd.DataFrame(tabla137)
tabla137['fecha_histórica'] = '2023-02-17'
tabla137 = tabla137[orden]


tabla138 = pd.read_excel('Silicon_Valley_21_02_2023.xlsx')
tabla138 = pd.DataFrame(tabla138)
tabla138['fecha_histórica'] = '2023-02-21'
tabla138 = tabla138[orden]



tabla139 = pd.read_excel('Silicon_Valley_24_02_2023.xlsx')
tabla139 = pd.DataFrame(tabla139)
tabla139['fecha_histórica'] = '2023-02-24'
tabla139 = tabla139[orden]

tabla140 = pd.read_excel('Silicon_Valley_28_02_2023.xlsx')
tabla140 = pd.DataFrame(tabla140)
tabla140['fecha_histórica'] = '2023-02-28'
tabla140 = tabla140[orden]


tabla141 = pd.read_excel('Silicon_Valley_03_03_2023.xlsx')
tabla141 = pd.DataFrame(tabla141)
tabla141['fecha_histórica'] = '2023-03-03'
tabla141 = tabla141[orden]


tabla142 = pd.read_excel('Silicon_Valley_07_03_2023.xlsx')
tabla142 = pd.DataFrame(tabla142)
tabla142['fecha_histórica'] = '2023-03-07'
tabla142 = tabla142[orden]


tabla143 = pd.read_excel('Silicon_Valley_10_03_2023.xlsx')
tabla143 = pd.DataFrame(tabla143)
tabla143['fecha_histórica'] = '2023-03-10'
tabla143 = tabla143[orden]


tabla144 = pd.read_excel('Silicon_Valley_14_03_2023.xlsx')
tabla144 = pd.DataFrame(tabla144)
tabla144['fecha_histórica'] = '2023-03-14'
tabla144 = tabla144[orden]


tabla145 = pd.read_excel('Silicon_Valley_17_03_2023.xlsx')
tabla145 = pd.DataFrame(tabla145)
tabla145['fecha_histórica'] = '2023-03-17'
tabla145 = tabla145[orden]


tablaY = pd.concat([tabla145, tabla144,
                    tabla143, tabla142, tabla141, 
                    tabla140, tabla139, tabla138, 
                    tabla137, tabla136, tabla135,
                    tabla134, tabla133, tabla132,
                    tabla131, tabla130, tabla129,
                    tabla128, tabla127, tabla126, 
                    tabla125, tabla124, tabla123,
                    tabla122, tabla121, tabla120, 
                    tabla119, tabla118, tabla117,
                    tabla116, tabla115, tabla114,
                    tabla113, tabla112, tabla111,
                    tabla110, tabla109, tabla108,
                    tabla107, tabla106, tabla105,
                    tabla104, tabla103, tabla102,
                    tabla101, tabla100, tabla99,
                    tabla98, tabla97, tabla96
                    ]).drop_duplicates(subset='BARCD_IND').reset_index(drop=True)

# tablaY = tablaY.dropna()
tablaY['BARCD_IND'] =  tablaY['BARCD_IND'].astype(str)

"""
start_date = '2022-01-15'
between = (tablaY['INHVDT_est'] >= start_date)
tablaY = tablaY[between]
"""
# tablaY.columns

tablaY = tablaY.sort_values(by=["fecha_histórica"])

# tablaY = tablaY[tablaY['SEMANA_FLORACION_REAL'].notna()]

# k6 = tablaY[tablaY['BARCD_IND']== 'UR293039219']
# print(k6)


# tablaY.to_excel('La_ROCA_reporte_siembra_poli_cosecha.xlsx', index= False)
# tablaY.to_excel('LA_ROCA_reporte_inducción_siembra_poli_cosecha.xlsx', index= False)
# tablaY.to_excel('LA_ROCA_ind_fechas.xlsx', index= False)
  

# tablaY = tablaY.dropna()
# tablaY = tablaY.sort_values(by=["FECHA_3_est"])

import matplotlib.pyplot as plt
# multiple line plots
plt.plot('BARCD_IND' , 'SEMANA_SIEMBRA_REAL', data =  tablaY, marker='o', markerfacecolor='brown', markersize=5, color='lightgreen', linewidth=4, label= "siembra")
plt.plot('BARCD_IND' , 'SEMANA_FLORACION_ESTIMADA', data =  tablaY, marker='o', markerfacecolor='blue', markersize=5, color='orange', linewidth=4, label= "floración_estimada")
plt.plot('BARCD_IND' , 'SEMANA_FLORACION_REAL', data =  tablaY, marker='o', markerfacecolor='blue', markersize=5, color='yellow', linewidth=4, label= "floración_real")
plt.plot( 'BARCD_IND', 'SEMANA_COSECHA_ESTIMADA', data =  tablaY, marker='o', markerfacecolor='yellow', color='blue', linewidth=2, label = "Cosecha_Estimada")
plt.plot( 'BARCD_IND', 'SEMANA_COSECHA_REAL', data =  tablaY, marker='o', markerfacecolor='lightgreen', color='red', linewidth=2, linestyle='dashed', label="Cosecha_Real")
plt.title('Pronóstico desde siembra a cosecha en inducción')
# show legend
plt.legend()# show graphh
plt.show()


"""
####################
#----HASTA AQUÍ----
####################
"""


"""
# tablaY.columns


tablaY['FECHA_2_est'] = pd.to_datetime(tablaY['FECHA_2_est'] , format="%d-%m-%Y")
tablaY['FECHA_2'] = pd.to_datetime(tablaY['FECHA_2'] , format="%d-%m-%Y")
tablaY['FECHA_3_est'] = pd.to_datetime(tablaY['FECHA_3_est'] , format="%d-%m-%Y")
tablaY['FECHA_3'] = pd.to_datetime(tablaY['FECHA_3'] , format="%d-%m-%Y")


tablaY['BARCD_IND'] = tablaY['BARCD_IND'].astype('object')
tablaY['error_poli'] =  (tablaY['FECHA_2'] - tablaY['FECHA_2_est'])
tablaY['error_poli'] = (tablaY['error_poli'].apply(lambda x: x.days))
tablaY['error_poli'].describe()


tablaY['error_cosecha'] =  tablaY['FECHA_3'] - tablaY['FECHA_3_est']
tablaY['error_cosecha'] = (tablaY['error_cosecha'].apply(lambda x: x.days))
tablaY['error_cosecha'].describe()



import pandas as pd
import matplotlib.pyplot as plt

boxplot = tablaY.boxplot(column=['error_poli', 'error_cosecha'])
boxplot.plot()
plt.show()


import matplotlib.pyplot as plt
plt.style.use('Solarize_Light2')
import numpy as np
import pandas as pd

fig = plt.figure()
ax = plt.axes()
plt.title('Errores de Floración (rojo) y Cosecha (azul)')

y = tablaY['error_poli'].values
x = tablaY['BARCD_IND'].values
plt.plot(x, y, 'o' , color = 'red')

l = tablaY['error_cosecha'].values
m = tablaY['BARCD_IND'].values
plt.plot(m, l, 'o' , color = 'blue')

"""



"""
'REGION_CODE_CONTINENT', 'DESCRIPTION',
              'PLACD_IND', 'week_n_INPLTDT',
              'codigo', 'Maturity', 'INSTDCT', 'INPOLCT'
"""

# tablaY.columns

# 'REGION_CODE_CONTINENT', 'DESCRIPTION', 'sector',
#  'Maturity' , 'codigo' , 'FECHA_1' , 'periodo_f1', 'SEMANA_SIEMBRA_REAL'

# cruzar la info
# cruzar el stdcount en inducción y el grupo heterotico






