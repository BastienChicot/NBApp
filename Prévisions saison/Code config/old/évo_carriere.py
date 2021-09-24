# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd

path = os.getcwd()
os.chdir(path+'/OneDrive/Bureau/NBA/Prévisions saison')
df = pd.read_csv("base.csv", sep=";")


df1 = df.sort_values(['full_name', 'Date'], ascending=[False, True])
df1['game_rank'] = df1.groupby(['full_name'])['Date'].transform(lambda x: list(map(lambda y: dict(map(reversed, dict(enumerate(x.unique())).items()))[y]+1,x)) )

import matplotlib.pyplot as plt
df1['PTS_scaled'] = (df1['PTS']-df1.groupby('full_name')['PTS'].transform('min'))/(df1.groupby('full_name')['PTS'].transform('max')-df1.groupby('full_name')['PTS'].transform('min'))
df1['carriere']=df1['annee']-df1.groupby('full_name')['annee'].transform('min')
#df_test = df2.loc[df1['full_name']=="Kevin Durant"]
#plt.scatter(df_test['game_rank'],df_test['PTS_scaled'])

#m=df1.corr()

data=df1.copy()
data=data[["full_name","Date","PTS_scaled" , "minutes","age","game_rank","carriere","GS","Prod_mean_opp"]]
data=data.dropna()
df2=df1[["full_name","Date","PTS_scaled" , "minutes","age","game_rank","carriere","GS","Prod_mean_opp",
          "AST","TRB","FGA","PF","TOV","id_Prod"]]
df2 = df2.set_index(['full_name','Date'])
df2=df2.dropna()

data_taff= pd.read_csv("Base_travail.csv",sep=";")
from sklearn.cluster import KMeans
x = df2.values 
#Choix du nombre de cluster
inertie = []
K_range = range(1, 50)
for k in K_range:
    model = KMeans(n_clusters=k).fit(x)
    inertie.append(model.inertia_)

plt.plot(K_range, inertie)
    
kmeans = KMeans(n_clusters=10, random_state=0).fit(x)
kmeans.labels_
df2['cluster'] = kmeans.labels_
df2.loc[df2.cluster == 0].count()

df2 = df2.reset_index()

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
import numpy as np
plt.hist(df2['cluster'])
def histo_log(base, donnees):
    base['log']=np.log(donnees)
    base=base.replace([np.inf, -np.inf], np.nan)
    plt.hist(base['log'])
histo_log(data, data['carriere'])  

df2=df2[["full_name","Date","cluster"]]
df1 = pd.merge(df1,df2, how='inner', on=['full_name','Date'])  
#df1.to_csv("Base1.csv",sep=";")
count = df1.groupby('full_name').count().reset_index()
count = count[['full_name', 'Tm']]
count = count.rename(columns={"Tm":"count"})
indexNames = count[ (count['count'] < 10)].index
count.drop(indexNames , inplace=True)

df1 = pd.merge(df1, count, on='full_name')
df1 = df1.replace([np.inf, -np.inf], np.nan)
#df1=df1.dropna()
df1.to_csv("Base_travail.csv", sep=";")

###########MODELE SCIKIT LEARN######################
#########0.69 R², mse 0.013, mae 0.08
#####& IC à l'arrache [-6.14 / +11.2]
y=df1[['PTS_scaled']]
X=df1[['full_name','cluster',"minutes","age","game_rank","carriere","GS","Prod_mean_opp",
       'Tm','Domicile','month','FGA_moy','TOV_moy','PF_moy','id_Prod',"cluster_coach",
       "cluster_player"]]

numeric_data = ['age','minutes',
                "game_rank","carriere",
                'Prod_mean_opp',"FGA_moy",'TOV_moy','PF_moy','id_Prod'
                ]
object_data = ['full_name',
               'GS','cluster','Tm','Domicile','month',"cluster_coach","cluster_player"
               ]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler(),SelectKBest(f_regression,
                                                                                    k=10))
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor

reg = LinearRegression(normalize=True,fit_intercept=True,
                                                       copy_X=True)
Lin_Reg = make_pipeline(preprocessor, reg)
MLP = make_pipeline(preprocessor, MLPRegressor(solver='adam',learning_rate='adaptive',
                                               hidden_layer_sizes=150, alpha=0.00005,
                                               activation='relu'))
RFR = make_pipeline(preprocessor, RandomForestRegressor(n_estimators=10))
KNN = make_pipeline(preprocessor, KNeighborsRegressor())
Ridge = make_pipeline(preprocessor,RidgeCV(alphas=[0.61],cv=5))
SGD = make_pipeline(preprocessor, SGDRegressor(loss='squared_loss', penalty='l2',
                                               alpha=0.0001,l1_ratio=0.16,epsilon=0.01))

dict_of_models = {'Linéaire': Lin_Reg,
                  "Neural": MLP,
                  "Ridge": Ridge,
                  "SGD" : SGD
                 }

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluation (model):
    model.fit(X_train, y_train.values.ravel())
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test.values.ravel(), y_pred)
    print(mse)
    print(mae)
    print(r2_score)
    print (model.score(X_test, y_test))
    
for name, model in dict_of_models.items():
    print(name)
    evaluation(model)  

reg.coef_
hyper_params = {'linearregression__fit_intercept': [True,False],
                'linearregression__normalize': [True,False],
                'linearregression__copy_X': [True,False],
                'linearregression__n_jobs': [0,1,5,10,20]
                }

from sklearn.model_selection import RandomizedSearchCV
X_test['Tm'] = X_test['Tm'].apply(lambda x: "NOH" if x == "NOK" else x)

grid = RandomizedSearchCV(Lin_Reg, hyper_params,cv=4,
                          n_iter=50)

evaluation(Lin_Reg)

print(grid.best_params_)
reg.coef_

Lin_Reg.fit(X, y.values.ravel())
from joblib import dump
dump(Lin_Reg, 'model_lin.joblib')

df_test = df1.copy()
df_test['pred']=Lin_Reg.predict(df_test)

df_test['PTS_pred']=df_test['pred']*(df_test.groupby('full_name')['PTS'].transform('max')-df_test.groupby('full_name')['PTS'].transform('min'))

df_GG = df_test[['full_name','PTS','PTS_pred','PTS_scaled','pred']]
df_GG['error']=df_GG['PTS']-df_GG['PTS_pred']

plt.hist(df_GG['error'])
np.percentile(df_GG['error'],97.5)

###########MODELE STATS MODEL######## sans id_Prod
###### R² 0.378  MSE = 57,17
###### Interval de confiance à l'arrache 
#### -9.34 / 14.36
#### mean error = -0.1109 ecart type == 5.74
import statsmodels.formula.api as smf

data=pd.read_csv("data_ML.csv",sep=";")

plt.hist(df1['id_Prod'])
def histo_log(base, donnees):
    base['log']=np.log(donnees)
    base=base.replace([np.inf, -np.inf], np.nan)
    plt.hist(base['log'])
histo_log(df1, df1['FGA_moy']) 

data.info()
reg = smf.ols('PTS_diff ~ age+C(cluster_coach)+C(cluster_team)+C(cluster_player)+C(GS)+C(month)',
              data = data)

res=reg.fit()
res.mse_model
txt = res.summary()
a=txt.as_text()
a.to_text("summary_pts_diff.txt")

print(res.summary())
print(res.rsquared)

import statsmodels.api as sm

sm.qqplot(res.resid)

res.conf_int(alpha=0.05, cols=None)
dump(res, 'model_linéaire_standard.joblib')

df_test = df.copy()
df_test['pred']=res.predict(df_test)

df_test['PTS_pred']=df_test['pred']*(df_test.groupby('full_name')['PTS'].transform('max')-df_test.groupby('full_name')['PTS'].transform('min'))
df_GG2 = df_test[['full_name','PTS','PTS_pred','PTS_scaled','pred']]
df_GG2['error']=df_GG2['PTS']-df_GG2['PTS_pred']

plt.hist(df_GG2['error'])
np.percentile(df_GG2['error'],97.5)
np.nanstd(df_GG2['error'])
