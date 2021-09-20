# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:17:07 2021

@author: basti
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer

data = pd.read_csv("base_machine_learning4.csv", sep=";")
team_stat = pd.read_csv("teamstats.csv", sep=";")
evo_car=pd.read_csv("indice_evolution.csv", sep=";")
team_stat = team_stat.rename(columns={"Unnamed: 1":"annee"})

d={'Team':[
'New York Knicks', 
'Los Angeles Lakers', 
'Utah Jazz',
'Phoenix Suns',
'Los Angeles Clippers', 
'Houston Rockets',
'Boston Celtics',
'Memphis Grizzlies',
'Cleveland Cavaliers',
'Philadelphia 76ers',
'Miami Heat',
'Atlanta Hawks',
'Charlotte Hornets',
'Milwaukee Bucks',
'Toronto Raptors',
'San Antonio Spurs',
'Indiana Pacers',
'Denver Nuggets',
'Orlando Magic',
'New Orleans Pelicans',
'Dallas Mavericks',
'Detroit Pistons',
'Oklahoma City Thunder',
'Golden State Warriors',
'Minnesota Timberwolves',
'Portland Trail Blazers',
'Chicago Bulls',
'Sacramento Kings',
'Brooklyn Nets',
'Washington Wizards']
    ,'Opp':
        ['NYK','LAL','UTA','PHO','LAC','HOU','BOS','MEM','CLE','PHI','MIA','ATL',
         'CHO','MIL','TOR','SAS','IND','DEN','ORL','NOP','DAL','DET','OKC','GSW',
         'MIN','POR','CHI','SAC','BRK','WAS']}

def_rank = pd.DataFrame(data=d)


def_rank = pd.merge(def_rank, team_stat, how='left', on=['Team'])
def_rank = def_rank.drop_duplicates(['Team', 'annee', 'DRtg/A'],keep= 'last')
def_rank.to_csv("teamstats.csv", sep=";")
team_stat = team_stat.rename(columns={"Opp_y":"Opp"})
data = pd.merge(data, team_stat, how='left', on=['Opp','annee'])
data = pd.merge(data, evo_car, how='left', on=['full_name','Date'])
data['Prod'] = data['PTS']+data['AST']+data['TRB']+data['BLK']+data['STL']-(data['TOV']+data[
    'PF']+(data['FGA']-data['FG'])+(data['FTA']-data['FT'])+(data['3PA']-data['3P']))
data = data[["full_name","Date","annee","Tm_x","Opp_x","Opp_name","Opp_Coach",
             "age","minutes","GS_x","Domicile","month_x","PTS","AST","TRB","FGA",
             "TOV","PF","PTS_diff","AST_diff","TRB_diff","FGA_moy","TOV_moy","PF_moy",
             "cluster_coach","cluster_player","cluster_team","Team","Conf",
             "DRtg","DRtg/A","Div","L","MOV","MOV/A","NRtg","NRtg/A",
             "ORtg","ORtg/A","W","W/L%","Prod"]]
data['Prod_min']=data['Prod']/data['minutes']

df2 = data.groupby(['full_name'])['Prod_min'].max().reset_index()

df2 = df2.rename(columns={'Prod_min': 'Prod_min_max'})
df3 = data.groupby(['full_name','annee'])['Prod_min'].mean().reset_index()
df3 = df3.rename(columns={'Prod_min': 'Prod_mean_opp'})
data = pd.merge(data, df2, on='full_name', how='inner')
data = pd.merge(data, df3, on=['full_name','annee'], how='inner')

data['id_Prod']=data['Prod_min']/data['Prod_min_max']

data.info()
data.to_csv("base_ML_complet2.csv", sep=";")

df = data.copy()
indexNames = df[ (df['GS_x'] != '1') & (df['GS_x'] != '0')].index

df.drop(indexNames , inplace=True)

df['GS_x']=df.GS_x.astype(float)
df.info()

count = df.groupby('full_name').count().reset_index()
count = count[['full_name', 'Tm_x']]
count = count.rename(columns={"Tm_x":"count"})
indexNames = count[ (count['count'] < 10)].index
count.drop(indexNames , inplace=True)

df = pd.merge(df, count, on='full_name')

target_datas =  ['PTS','AST','TRB','PTS_diff','AST_diff','TRB_diff']
df = df.rename(columns={"Opp_x":"Opp"})
df = df.rename(columns={"Tm_x":"Tm"})
df = df.rename(columns={"GS_x":"GS"})
df = df.rename(columns={"month_x":"month"})
df.to_csv("data.csv", sep=";")
#CREATION X ET Y
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna() 

y = df[['PTS']]

#min_max_scaler = MinMaxScaler()
#y_scaled = min_max_scaler.fit_transform(y)
#y = pd.DataFrame(y_scaled)
#y = y[0]

X = df[['full_name',
        'Tm_x',
        'GS_x',
        'Domicile',
        'month_x',
        'cluster_coach',
        'cluster_player',
        'cluster_team',
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
               'Tm_x',
               'GS_x',
               'Domicile',
               'month_x',
               'cluster_coach',
               'cluster_player',
               'cluster_team'
               ]


corrMat = data.corr()
#Data exploration
df.dtypes.value_counts().plot.pie()

for target_data in target_datas:
    print(df[target_data].value_counts(normalize=True))

for col in df.select_dtypes('float'):
    plt.figure()
    sns.distplot(df[col])


#PIPELINE

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler())
object_pipeline = make_pipeline(OneHotEncoder())

preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                       (object_pipeline, object_data))

#MODELE

from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV, SGDRegressor
from sklearn.neighbors import KNeighborsRegressor

Lin_Reg = make_pipeline(preprocessor, LinearRegression())
MLP = make_pipeline(preprocessor, MLPRegressor())
RFR = make_pipeline(preprocessor, RandomForestRegressor(n_estimators=20))
KNN = make_pipeline(preprocessor, KNeighborsRegressor())
Ridge = make_pipeline(preprocessor,RidgeCV())
SGD = make_pipeline(preprocessor, SGDRegressor())

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
