# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 13:35:16 2022

@author: s1073533
"""

import pandas as pd
import numpy as np
import datetime
# DATA
arica = pd.read_excel('act_tot_18_11_2022.xlsx')
chavi = arica
arica = arica[arica['LOC_NAME'] == 'ARICA']

"""
###----PREPARAR LA DATA  INDUCCIÓN----###
"""
O = arica[['REGION_CODE_CONTINENT', 'MATID_Ind',
           'CPU_ACT', 'MAT_GENERATED', 'BARCD_IND',
           'DESCRIPTION',  'PLACD_IND', 'Maturity', 
           'INPLTDT', 'INPOLDT', 'INHVDT']]

O['PLACD_IND'] = O['PLACD_IND'].astype('object')

def count_unique_values(df):
    return df.nunique()

print (count_unique_values(O))