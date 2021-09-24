# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 15:52:54 2021

@author: basti
"""

import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, PowerTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.compose import make_column_transformer
from sklearn.linear_model import RidgeCV
from joblib import dump
import numpy as np

data = pd.read_csv("data_ML.csv", sep=";")
df1['pred']=Ridge.predict(df1)
test=df1.loc[df1['full_name']=="Anfernee Simons"]
df = data.copy()
df["Tm"]=df['Tm'].str.lower()
df.loc[(df["Tm"]=="brk"),"Tm"]='bkn'
df.loc[(df["Tm"]=="cho"),"Tm"]='cha'
df.loc[(df["Tm"]=="gsw"),"Tm"]='gs'
df.loc[(df["Tm"]=="nop"),"Tm"]='no'
df.loc[(df["Tm"]=="nyk"),"Tm"]='ny'
df.loc[(df["Tm"]=="sas"),"Tm"]='sa'
df.loc[(df["Tm"]=="uta"),"Tm"]='utah'
df.loc[(df["Tm"]=="was"),"Tm"]='wsh'

np.unique(df['Tm'])
df['log_pts']=np.log(df['PTS'])
df1=df.replace([np.inf, -np.inf], np.nan)
df1=df1.dropna()
y = df1[['log_pts']]

X = df1[['full_name',
        'Tm',
        'GS','minutes',
        #'Domicile',
        'month',
        'cluster_coach',
        'cluster_player',
        'age',
        'FGA_moy','TOV_moy','PF_moy',
        'Prod_mean_opp'
        ]]

numeric_data = ['age','minutes',
                'FGA_moy','TOV_moy','PF_moy',
                'Prod_mean_opp'
                ]
object_data = ['full_name',
               'Tm','GS',
               #'Domicile',
               'month',
               'cluster_coach',
               'cluster_player'
               ]

numeric_pipeline = make_pipeline(PolynomialFeatures(2),PowerTransformer(method="yeo-johnson"),SelectKBest(f_regression,
                                                                                    k=10))
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

Ridge = make_pipeline(preprocessor,RidgeCV(alphas=[0.61],cv=5))  
Ridge.fit(X, y.values.ravel())
dump(Ridge, '../Ridge_PTS.joblib')
print("Entrainement du modèle de prediction des points")
    
