# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:17:07 2021

@author: basti
"""

import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PowerTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer

data = pd.read_csv("data/data_ML.csv", sep=";")

df = data.copy()
df= df.dropna()
#CREATION X ET Y
y = df[['FGA']]
yeojohnson_scaler = PowerTransformer(method="yeo-johnson")
y_scaled = yeojohnson_scaler.fit_transform(y)
y = pd.DataFrame(y_scaled)
y = y[0]

X = df[['full_name',
        'Tm',
        'GS',
        'minutes',
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
#PIPELINE

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),PowerTransformer(method="yeo-johnson"),SelectKBest(f_regression,
                                                                                    k=10))
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

#MODELE

from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor

Lin_Reg = make_pipeline(preprocessor, LinearRegression(copy_X=True,
                                                       fit_intercept=False,
                                                       n_jobs=0.01))
MLP = make_pipeline(preprocessor, MLPRegressor())
RFR = make_pipeline(preprocessor, RandomForestRegressor(n_estimators=10))
KNN = make_pipeline(preprocessor, KNeighborsRegressor())
Ridge = make_pipeline(preprocessor,RidgeCV(alphas=[0.61],cv=5))
SGD = make_pipeline(preprocessor, SGDRegressor(loss='squared_loss', penalty='l2',
                                               alpha=0.0001,l1_ratio=0.16,epsilon=0.01))

dict_of_models = {'Linéaire': Lin_Reg,
                  "Neural": MLP,
                  "Ridge": Ridge,
                  "SGD" : SGD,
                  "KNN":KNN,
                  "RFR":RFR,
                 }

from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluation (model):
    model.fit(X_train, y_train.values.ravel())
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test.values.ravel(), y_pred)
    print(mse)
    print(mae)
    print (model.score(X_test, y_test))
    
for name, model in dict_of_models.items():
    print(name)
    evaluation(model)  

evaluation(Ridge)
