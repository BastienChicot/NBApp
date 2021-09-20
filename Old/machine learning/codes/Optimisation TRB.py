# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 19:26:50 2021

@author: basti
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import Ridge
from joblib import dump, load

data = pd.read_csv("base_ML_complet.csv", sep=";")
df = data.copy()
indexNames = df[ (df['GS'] != '1') & (df['GS'] != '0')].index
indexNames2 = df[ (df['cluster_player'] == 9)].index

df.drop(indexNames , inplace=True)
df.drop(indexNames2 , inplace=True)

df['GS']=df.GS.astype(float)
df.info()

count = df.groupby('full_name').count().reset_index()
count = count[['full_name', 'Tm']]
count = count.rename(columns={"Tm":"count"})
indexNames = count[ (count['count'] < 50)].index
count.drop(indexNames , inplace=True)

df = pd.merge(df, count, on='full_name')
matcorr = df.corr()
df = df.dropna() 
#df=pd.merge(df, fga_pred, how='inner', on=['full_name','GS','minutes'])
df = df.drop_duplicates(['full_name','age','annee','month','minutes','PTS_diff',
                         'Opp','Opp_Coach'],keep= 'last')
y = df[['TRB']]

#min_max_scaler = MinMaxScaler()
#y_scaled = min_max_scaler.fit_transform(y)
#y = pd.DataFrame(y_scaled)
#y = y[0]

X = df[['full_name',
        'Tm',
        'GS',
        'Domicile',
        'month',
        'cluster_team',
        'cluster_player',
        'age',
        'minutes',
        'FGA','TOV_moy','PF','annee'
        ]]

numeric_data = ['age',
                'minutes',
                'FGA','TOV_moy','PF','annee'
                ]
object_data = ['full_name',
               'Tm',
               'GS',
               'Domicile',
               'month',
               'cluster_team',
               'cluster_player',
               ]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler(),SelectKBest(f_regression,
                                                                                    k=10))
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

#MODELE (R² = 59.5)
Lin_ridge =  make_pipeline(preprocessor, Ridge(alpha=0.1,copy_X=True,max_iter=100,
                                               solver='auto'))


dict_of_models = {'Ridge': Lin_ridge
                 }

Ridge
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
    
Lin_ridge.fit(X,y.values.ravel())
y_pred = Lin_ridge.predict(X_test)
mse = mean_squared_error(y_test.values.ravel(), y_pred)
mae = mean_absolute_error(y_test.values.ravel(), y_pred)
print(mse)
print(mae)
print (Lin_ridge.score(X_test, y_test.values.ravel()))

dump(Lin_ridge, 'Ridge_TRB_pred.joblib')

hyper_params = {'ridge__copy_X' : ['True','False'],
                'ridge__tol': [0.0001,0.001],
                'ridge__solver' : ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'],
                'ridge__max_iter' : [100,10,5],
                'ridge__alpha' : [0.01,0.1]
                }

grid = GridSearchCV(Lin_ridge, hyper_params, cv=5)

evaluation(grid)

print(grid.best_params_)