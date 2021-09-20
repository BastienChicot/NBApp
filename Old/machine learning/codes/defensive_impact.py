# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 14:15:56 2021

@author: basti
"""

import pandas as pd

#oppcoach = pd.read_csv("diff_oppcoach.csv", sep=";")
#oppplayer = pd.read_csv("diff_oppplayer.csv", sep=";")
#oppteam = pd.read_csv("diff_oppteam.csv", sep=";")
base = pd.read_csv("player_stat-20-030421.csv", sep =";")

#Création des stats annuelles de chaque joueur
stat = base.groupby(['full_name','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()

stat = stat.rename(columns={"PTS":"PTS_moy", "AST":"AST_moy","TRB":"TRB_moy", "FG":"FG_moy",
                            "FGA":"FGA_moy", "TOV":"TOV_moy","PF":"PF_moy", "BLK":"BLK_moy",
                            "STL":"STL_moy"})

base=base[['full_name','annee','Tm','Opp','Opp_name','Opp_Coach','AST','Age','BLK',
           'Date','FG','FGA','GS','MP','PF','PTS','STL','TOV','TRB','joueur',
           'Domicile','Coach','year','month','day','3PA','3P','FTA','FT']]

#Merge 
base = pd.merge(base,stat, on=["full_name","annee"])
base = base.drop_duplicates(['Age', 'Date', 'full_name'],keep= 'last')

import matplotlib.pyplot as plt
import seaborn as sns
corrMat = base.corr()
base.dtypes.value_counts().plot.pie()
for col in base.select_dtypes('float'):
    plt.figure()
    sns.distplot(base[col])

#Calcul de la différence entre la perf du match et les moyennes annuelles
base["PTS_diff"] = base["PTS"]-base["PTS_moy"]
base["AST_diff"] = base["AST"]-base["AST_moy"]
base["TRB_diff"] = base["TRB"]-base["TRB_moy"]
base["FG_diff"] = base["FG"]-base["FG_moy"]
base["FGA_diff"] = base["FGA"]-base["FGA_moy"]
base["TOV_diff"] = base["TOV"]-base["TOV_moy"]
base["PF_diff"] = base["PF"]-base["PF_moy"]
base["BLK_diff"] = base["BLK"]-base["BLK_moy"]
base["STL_diff"] = base["STL"]-base["STL_moy"]

#Calcul des moyennes des différences par Coach, équipe et joueur opposé
coach_impact = base.groupby(['Opp_Coach','annee'])['PTS_diff','AST_diff','TRB_diff',
                                                   'FGA','TOV',
                                                   'PF','BLK_diff','STL_diff'
                                                   ].mean().reset_index()

team_impact = base.groupby(['Opp','annee'])['PTS_diff','AST_diff','TRB_diff',
                                                   'FGA','TOV',
                                                   'PF','BLK_diff','STL_diff'
                                                   ].mean().reset_index()
player_impact = base.groupby(['Opp_name','annee'])['PTS_diff','AST_diff','TRB_diff',
                                                   'FGA','TOV',
                                                   'PF','BLK_diff','STL_diff'
                                                   ].mean().reset_index()

coach_impact.to_csv("diff_oppcoach.csv", sep=";")
team_impact.to_csv("diff_oppteam.csv", sep=";")
player_impact.to_csv("diff_oppplayer.csv", sep=";")

#Graphiques d'observation

import seaborn as sns

sns.pairplot(
    team_impact,
    y_vars=["PTS_diff", "AST_diff","TRB_diff"],
)

sns.pairplot(
    team_impact,
    y_vars=["PTS_diff", "AST_diff","TRB_diff"])


joueur = base.query("full_name == 'Damian Lillard'")
sns.lineplot(data=joueur, x="Date", y="PTS")

#Clustering

from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np

#Coach !
df_coach = coach_impact
df_coach = df_coach[['Opp_Coach','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]
df_coach = df_coach.set_index(['Opp_Coach','annee'])

x = df_coach.values #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#x_scaled = min_max_scaler.fit_transform(x)
#d_scaled = pd.DataFrame(x_scaled)
 
#Choix du nombre de cluster
inertie = []
K_range = range(1, 20)
for k in K_range:
    model = KMeans(n_clusters=k).fit(x)
    inertie.append(model.inertia_)
    
import matplotlib.pyplot as plt

plt.plot(K_range, inertie)
    
kmeans = KMeans(n_clusters=5, random_state=0).fit(x)
kmeans.labels_
df_coach['cluster'] = kmeans.labels_
df_coach.loc[df_coach.cluster == 0].count()

df_coach = df_coach.reset_index()
sns.swarmplot(df_coach.cluster,df_coach.cluster)

#Player !
df_player = player_impact
df_player = df_player[['Opp_name','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]

df_player = df_player.set_index(['Opp_name','annee'])
df_player = df_player.dropna()

xp = df_player.values #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#xp_scaled = min_max_scaler.fit_transform(xp)
#dp_scaled = pd.DataFrame(xp_scaled)

#Choix du nombre de cluster
inertie = []
K_range = range(1, 25)
for k in K_range:
    model = KMeans(n_clusters=k).fit(xp)
    inertie.append(model.inertia_)

plt.plot(K_range, inertie)

kmeansp = KMeans(n_clusters=5, random_state=0).fit(xp)
kmeansp.labels_
df_player['cluster'] = kmeansp.labels_
df_player.loc[df_player.cluster == 0].count()

df_player = df_player.reset_index()
sns.swarmplot(df_player.cluster,df_player.cluster)

#Teams !
df_team = team_impact
df_team = df_team[['Opp','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]

df_team = df_team.set_index(['Opp','annee'])
df_team = df_team.dropna()

xt = df_team.values #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#xp_scaled = min_max_scaler.fit_transform(xp)
#dp_scaled = pd.DataFrame(xp_scaled)

#Choix du nombre de cluster
inertie = []
K_range = range(1, 15)
for k in K_range:
    model = KMeans(n_clusters=k).fit(xt)
    inertie.append(model.inertia_)

plt.plot(K_range, inertie)

kmeansp = KMeans(n_clusters=5, random_state=0).fit(xt)
kmeansp.labels_
df_team['cluster'] = kmeansp.labels_
df_team.loc[df_team.cluster == 0].count()

df_team = df_team.reset_index()
#OU
team_impact['on_offense'] = team_impact['PTS_diff']+team_impact['AST_diff']+team_impact['FGA_diff']+team_impact['TRB_diff']
team_impact['on_play'] = team_impact['TOV_diff']+team_impact['PF_diff']

#prépa des bases merge 

base.info()

import datetime

date = base[['year','month','day']]

base['date'] = datetime.date(base["Date"]).weekday()

base[['age','jour']] = base.Age.str.split("-",expand=True,)
base[['minutes','sec']] = base.MP.str.split(":",expand=True,)

base = base[['full_name','Date','annee','Tm','Opp','Opp_name','Opp_Coach','age','minutes','GS',
             'Domicile','month','PTS','AST','TRB','FGA','TOV','PF','PTS_diff','AST_diff',
             'TRB_diff','FGA_moy','TOV_moy','PF_moy','BLK','STL','FG','FTA','FT',
             '3PA','3P','MP']]

df_coach = df_coach.rename(columns={"cluster":"cluster_coach",})
df_coach = df_coach[['Opp_Coach','annee','cluster_coach']]

df_player = df_player.rename(columns={"cluster":"cluster_player",})
df_player = df_player[['Opp_name','annee','cluster_player']]

df_team = df_team.rename(columns={"cluster":"cluster_team",})
df_team = df_team[['Opp','annee','cluster_team']]
#OU
team_impact = team_impact[['Opp','annee','on_offense','on_play']]

#MERGE

base = pd.merge(base, df_coach, how = "left", on=["Opp_Coach","annee"])
base = pd.merge(base, df_player, how = "left", on=["Opp_name","annee"])
base = pd.merge(base, df_team, how = "left", on=["Opp","annee"])

base.to_csv("base_machine_learning4.csv",sep=";")