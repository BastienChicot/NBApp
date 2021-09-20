# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 12:36:51 2021

@author: basti
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from joblib import dump, load

data = pd.read_csv("base_ML_complet.csv", sep=";")
df = data.copy()
matCorr = df.corr()
indexNames = df[ (df['GS'] != '1') & (df['GS'] != '0')].index

df.drop(indexNames , inplace=True)

df['GS']=df.GS.astype(float)
df.info()

count = df.groupby('full_name').count().reset_index()
count = count[['full_name', 'Tm']]
count = count.rename(columns={"Tm":"count"})
indexNames = count[ (count['count'] < 50)].index
count.drop(indexNames , inplace=True)

df = pd.merge(df, count, on='full_name')

df = df.dropna() 
y = df[['FGA']]

#min_max_scaler = MinMaxScaler()
#y_scaled = min_max_scaler.fit_transform(y)
#y = pd.DataFrame(y_scaled)
#y = y[0]

X = df[['full_name',
        #'Tm',
        'GS',
        #'Domicile',
        #'month',
        #'cluster_coach',
        #'cluster_player',
        #'cluster_team',
        #'age',
        'minutes',
        #'FGA','TOV','PF',
        'count'
        ]]

numeric_data = [#'age',
                'minutes',
                #'FGA','TOV','PF'
                'count'
                ]
object_data = ['full_name',
               #'Tm',
               'GS',
               #'Domicile',
               #'month',
               #'cluster_coach',
               #'cluster_player',
               #'cluster_team'
               ]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler(),
                                 SelectKBest(f_regression,k=5))
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

Lin_Reg = make_pipeline(preprocessor, LinearRegression())
MLP = make_pipeline(preprocessor, MLPRegressor(max_iter=200, hidden_layer_sizes=(20,),
                                               activation='relu',solver='adam',
                                               alpha=0.0001,learning_rate='adaptive'))

dict_of_models = {
                  "Lin_reg":Lin_Reg,
                  "Neural": MLP,
                 }

hyper_params = {'mlpregressor__hidden_layer_sizes': [(20,)],
                'mlpregressor__activation': ['relu'],
                'mlpregressor__solver': ['adam'],
                'mlpregressor__alpha': [0.0001],
                'mlpregressor__learning_rate': ['adaptive'],
                }

def evaluation (model):
    model.fit(X_train, y_train.values.ravel())
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test.values.ravel(), y_pred)
    print(mse)
    print (model.score(X_test, y_test.values.ravel()))
    
for name, model in dict_of_models.items():
    print(name)
    evaluation(model)  

MLP.fit(X,y.values.ravel())
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test.values.ravel(), y_pred)
print(mse)

dump(MLP, 'MLP_FGA_pred.joblib')
    
grid = RandomizedSearchCV(MLP, hyper_params, cv=4,
                          n_iter=4)

evaluation(grid)

print(grid.best_params_)

X['FGA_pred'] = model.predict(X)
fga_pred = X.copy()