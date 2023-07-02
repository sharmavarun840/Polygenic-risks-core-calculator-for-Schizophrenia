#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import math
import os
import warnings
warnings.filterwarnings("ignore")


def schizo_genotype_code(x1, x2, x3, y):
    if y == x1:
        return 2  #2
    elif y == x2:
        return 1  #1
    elif y == x3:
        return 0  #0
    else :
        return np.NaN


xls = pd.ExcelFile('Schizo_calci.xlsx')
df = pd.read_excel(xls, 'Sheet1')


schizo_samples_df = pd.read_csv("SCHIZO_DEMO INPUT DATA.csv")

df = df.dropna()

col_list = ['condition name',
 'genes',
 'uniqueid',
 'RAF',
 'OR',
 'Risk allele',
 'Genotype call Dose 2',
 'Genotype call Dose 1',
 'Genotype call Dose 0']

template_df = df[col_list]


for sample_id in list(schizo_samples_df.columns):
    print(sample_id)
    temp_df = pd.concat([template_df, schizo_samples_df[sample_id]], axis=1).dropna()
    temp_df["SCHIZO Genotype code_cal"] = temp_df[['Genotype call Dose 2', 'Genotype call Dose 1', 'Genotype call Dose 0', sample_id]].apply(lambda x: schizo_genotype_code(x["Genotype call Dose 2"], x["Genotype call Dose 1"], x["Genotype call Dose 0"], x[sample_id]), axis=1)
    temp_df["Beta_cal"]              = temp_df["OR"].apply(lambda x: math.log(x))
    temp_df["Population score_cal"]  = temp_df[["Beta_cal", 'RAF']].apply(lambda x: (x['Beta_cal'] * x['RAF']), axis = 1)
    temp_df["Zero center score_cal"] = temp_df[["Beta_cal", "SCHIZO Genotype code_cal", 'Population score_cal']].apply(lambda x: ((x["Beta_cal"] * x["SCHIZO Genotype code_cal"])-x['Population score_cal']), axis = 1)
    temp_df["z score_cal"] = temp_df["Zero center score_cal"]/(temp_df["Population score_cal"].std())
    temp_df["Population score_std"] = temp_df["Population score_cal"].std()
    temp_df["z score avg"] = temp_df["z score_cal"].mean() 
    
    path = "SCHIZO_Outputs"
    if not os.path.exists(path):
        os.makedirs(path)
    sample_file_name = path + "/" + "SCHIZO_" + sample_id + ".csv"
    temp_df.to_csv(sample_file_name, index= False)
