# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 15:52:54 2021

@author: basti
"""

import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PowerTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.compose import make_column_transformer
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression, RidgeCV
from joblib import dump
import numpy as np

data = pd.read_csv("data/data_ML.csv", sep=";")

df = data.copy()

def train_model_pts():
    df['log_pts']=np.log(df['PTS'])
    df1=df.replace([np.inf, -np.inf], np.nan)
    df1=df1.dropna()
    y = df1[['log_pts']]
    
    X = df1[['full_name',
            'Tm',
            'GS','minutes',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'FGA_moy','TOV_moy','PF_moy','DRtg',
            'Prod_mean_opp'
            ]]
    
    numeric_data = ['age','minutes',
                    'FGA_moy','TOV_moy','PF_moy','DRtg',
                    'Prod_mean_opp'
                    ]
    object_data = ['full_name',
                   'Tm','GS',
                   'Domicile',
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
    dump(Ridge, 'models/Ridge_PTS.joblib')
    print("Entrainement du modèle de prediction des points")
    
def train_model_ast():
    df['log_ast']=np.log(df['AST'])
    df2=df.replace([np.inf, -np.inf], np.nan)
    df2=df2.dropna()
    y = df2[['log_ast']]

    X = df2[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'minutes',
            'FGA','TOV','PF','DRtg',
            'Prod_mean_opp'
            ]]
    
    numeric_data = ['age',
                    'minutes',
                    'FGA','TOV','PF','DRtg',
                    'Prod_mean_opp'
                    ]
    object_data = ['full_name',
                   'Tm','GS',
                   'Domicile',
                   'month',
                   'cluster_coach',
                   'cluster_player'
                   ]

    numeric_pipeline = make_pipeline(PolynomialFeatures(2),PowerTransformer(method="yeo-johnson"),SelectKBest(f_regression,
                                                                                        k=10))
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                           (object_pipeline, object_data))
    Lin_Reg = make_pipeline(preprocessor, LinearRegression(copy_X=True,
                                                       fit_intercept=False,
                                                       n_jobs=0.1))
    Lin_Reg.fit(X, y.values.ravel())
    dump(Lin_Reg, 'models/Lin_ast.joblib')
    print("Entrainement du modèle de prediction des assists")
    
def train_model_trb():
    df['log_trb']=np.log(df['TRB'])
    df3=df.replace([np.inf, -np.inf], np.nan)
    df3=df3.dropna()
    y = df3[['log_trb']]

    X = df3[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'minutes',
            'FGA','TOV','PF','DRtg',
            'Prod_mean_opp'
            ]]
    
    numeric_data = ['age',
                    'minutes',
                    'FGA','TOV','PF','DRtg',
                    'Prod_mean_opp'
                    ]
    object_data = ['full_name',
                   'Tm','GS',
                   'Domicile',
                   'month',
                   'cluster_coach',
                   'cluster_player'
                   ]
    
    numeric_pipeline = make_pipeline(PolynomialFeatures(2),PowerTransformer(method="yeo-johnson"),SelectKBest(f_regression,
                                                                                        k=10))
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                           (object_pipeline, object_data))
    Lin_Reg = make_pipeline(preprocessor, LinearRegression(copy_X=True,
                                                       fit_intercept=False,
                                                       n_jobs=0.1))
    Lin_Reg.fit(X, y.values.ravel())
    dump(Lin_Reg, 'models/Lin_trb.joblib')
    print("Entrainement du modèle de prediction des rebonds")
    
def train_model_fga():
    y = df[['FGA']]

    X = df[['full_name',
            'GS',
            'minutes',
            'count'
            ]]
    
    numeric_data = [
                    'minutes',
                    'count'
                    ]
    object_data = ['full_name',
                   'GS',
                   ]

    numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler(),
                                     SelectKBest(f_regression,k=5))
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                           (object_pipeline, object_data))
    MLP = make_pipeline(preprocessor, MLPRegressor(max_iter=200, hidden_layer_sizes=(20,),
                                               activation='relu',solver='adam',
                                               alpha=0.0001,learning_rate='adaptive'))
    MLP.fit(X, y.values.ravel())
    dump(MLP, 'models/MLP_FGA_pred.joblib')
    print("Entrainement du modèle de prediction des tirs pris")
