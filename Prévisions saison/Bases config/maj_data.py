# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 17:12:50 2021

@author: basti
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from sklearn.cluster import KMeans
import numpy as np

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

player_name = pd.read_csv("code_player.csv", sep = ";")

annee = "2021"
year=int(year)
#scrape_nba()
code_list = player_name['code']
lettre_list = player_name['letter']

df=[]
df2=[]

### RECUPERATION DES STATS PAR JOUEURS
for code in code_list :
    for lettre in lettre_list :
        code = code
        url = 'https://www.basketball-reference.com/players/a/'+(code)+'/gamelog/'+str(annee)
  
    #for url in url_list :  
    try :
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'pgl_basic'})
        tab_data = pd.read_html(str(table[0]))[0]
      
        tab_data['url'] = url
        tab_data['joueur'] = code
        tab_data['annee'] = annee
     
        df.append(tab_data)
        
    except IndexError:        
        gotdata = 'null'
    
final = pd.concat(df)
final.to_csv("nba_players_stats_"+str(annee)+".csv", sep =",")

### RECUPERATION DES COACHS
annees = [
          year-2,
          year-1,
          year
         ]
for ann in annees :
    try : 
        url = 'https://www.basketball-reference.com/leagues/NBA_'+str(ann)+'_coaches.html'

        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'NBA_coaches'})
        tab_data = pd.read_html(str(table[0]), header=2)[0]
        tab_data['annee'] = ann
     
        df2.append(tab_data)
        
    except IndexError:        
        gotdata = 'null'

final_coach = pd.concat(df2)


### NETTOYAGE DES FICHIERS

player_name = player_name.drop(["Unnamed: 0","letter","Age"], axis=1)
player_name = player_name.rename(columns={'code': 'joueur'})

df_propre = []

for ann in annees :
    data=pd.read_csv('nba_players_stats_'+str(ann)+'.csv', sep=",")
    

    data = data.drop(["Unnamed: 0", "FG%", "3P%", "FT%"], axis=1)
    
    if ann<2022 :
        indexNames = data[ data['Rk'] == 'Rk' ].index
        # Delete these row indexes from dataFrame
        data.drop(indexNames , inplace=True)
    
    if ann== 2021:        
        indexNames2 = data[ data['GS'] == 'Did Not Dress' ].index
        indexNames3 = data[ data['GS'] == 'Did Not Play' ].index
        indexNames4 = data[ data['GS'] == 'Inactive' ].index
        indexNames5 = data[ data['GS'] == 'Not With Team' ].index
        data.drop(indexNames2 , inplace=True)
        data.drop(indexNames3 , inplace=True)
        data.drop(indexNames4 , inplace=True)
        data.drop(indexNames5 , inplace=True)

    data['Domicile'] = data['Unnamed: 5'].apply(lambda x: '1' if x =="@" else '0')
    data = pd.merge(data, player_name, how="inner", on=["joueur"])
    data= pd.merge(data, final_coach, how = "inner", on = ["annee", "Tm"])
    data[['year','month', 'day']] = data.Date.str.split("-",expand=True,)
    data['year']=str(ann)
    
    data['id_joueur'] = data["year"]+data["month"]+data["day"]+data["Tm"]+data[
        "Opp"]+data["GS"]+data["POS"]
    data['id_opp'] = data["year"]+data["month"]+data["day"]+data["Opp"]+data[
        "Tm"]+data["GS"]+data["POS"]
    data['id_coach'] = data["year"]+data["month"]+data["day"]+data["Tm"]+data[
        "Opp"]+data["GS"]
    data['id_oppcoach'] = data["year"]+data["month"]+data["day"]+data["Opp"]+data[
        "Tm"]+data["GS"]
    data = data.drop_duplicates(['Age', 'Date', 'full_name'],keep= 'last')
    
    x = data[["full_name","id_joueur"]]
    x = x.rename(columns={"id_joueur":"id_opp", "full_name":"Opp_name"})
    y = data[["Coach","id_coach"]]
    y = y.rename(columns={"id_coach":"id_oppcoach", "Coach":"Opp_Coach"})
    y = y.drop_duplicates(['id_oppcoach'],keep= 'last')
    x = x.drop_duplicates(['id_opp'],keep= 'last')
    
    data = pd.merge(data, x, how = "left", on=["id_opp"])
    data = pd.merge(data, y, how = "left", on=["id_oppcoach"])

    data["PTS"] = pd.to_numeric(data['PTS'], errors='coerce').convert_dtypes()
    data["AST"] = pd.to_numeric(data['AST'], errors='coerce').convert_dtypes()
    data["TRB"] = pd.to_numeric(data['TRB'], errors='coerce').convert_dtypes()
    data["FG"] = pd.to_numeric(data['FG'], errors='coerce').convert_dtypes()
    data["FGA"] = pd.to_numeric(data['FGA'], errors='coerce').convert_dtypes()
    data["TOV"] = pd.to_numeric(data['TOV'], errors='coerce').convert_dtypes()
    data["PF"] = pd.to_numeric(data['PF'], errors='coerce').convert_dtypes()
    data["BLK"] = pd.to_numeric(data['BLK'], errors='coerce').convert_dtypes()
    data["STL"] = pd.to_numeric(data['STL'], errors='coerce').convert_dtypes()
    
    df_propre.append(data)

base = pd.concat(df_propre)
base.to_csv('player_stat.csv', sep=";") 

base["PTS"] = pd.to_numeric(base['PTS'], errors='coerce').convert_dtypes()
base["AST"] = pd.to_numeric(base['AST'], errors='coerce').convert_dtypes()
base["TRB"] = pd.to_numeric(base['TRB'], errors='coerce').convert_dtypes()
base["FG"] = pd.to_numeric(base['FG'], errors='coerce').convert_dtypes()
base["FGA"] = pd.to_numeric(base['FGA'], errors='coerce').convert_dtypes()
base["TOV"] = pd.to_numeric(base['TOV'], errors='coerce').convert_dtypes()
base["PF"] = pd.to_numeric(base['PF'], errors='coerce').convert_dtypes()
base["BLK"] = pd.to_numeric(base['BLK'], errors='coerce').convert_dtypes()
base["STL"] = pd.to_numeric(base['STL'], errors='coerce').convert_dtypes()
base["3P"] = pd.to_numeric(base['3P'], errors='coerce').convert_dtypes()   
base["3PA"] = pd.to_numeric(base['3PA'], errors='coerce').convert_dtypes()
base["FT"] = pd.to_numeric(base['FT'], errors='coerce').convert_dtypes()
base["FTA"] = pd.to_numeric(base['FTA'], errors='coerce').convert_dtypes()

### CALCUL DE L IMPACT DEFENSIF

stat = base.groupby(['full_name','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()
stat = stat.rename(columns={"PTS":"PTS_moy", "AST":"AST_moy","TRB":"TRB_moy", "FG":"FG_moy",
                            "FGA":"FGA_moy", "TOV":"TOV_moy","PF":"PF_moy", "BLK":"BLK_moy",
                            "STL":"STL_moy"})

base=base[['full_name','annee','Tm','Opp','Opp_name','Opp_Coach','AST','Age','BLK',
           'Date','FG','FGA','GS','MP','PF','PTS','STL','TOV','TRB','joueur',
           'Domicile','Coach','year','month','day','3PA','3P','FTA','FT']]

base = pd.merge(base,stat, on=["full_name","annee"])
base = base.drop_duplicates(['Age', 'Date', 'full_name'],keep= 'last')

base["PTS_diff"] = base["PTS"]-base["PTS_moy"]
base["AST_diff"] = base["AST"]-base["AST_moy"]
base["TRB_diff"] = base["TRB"]-base["TRB_moy"]
base["FG_diff"] = base["FG"]-base["FG_moy"]
base["FGA_diff"] = base["FGA"]-base["FGA_moy"]
base["TOV_diff"] = base["TOV"]-base["TOV_moy"]
base["PF_diff"] = base["PF"]-base["PF_moy"]
base["BLK_diff"] = base["BLK"]-base["BLK_moy"]
base["STL_diff"] = base["STL"]-base["STL_moy"]

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

df_coach = coach_impact
df_coach = df_coach[['Opp_Coach','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]
df_coach = df_coach.set_index(['Opp_Coach','annee'])
df_player = player_impact
df_player = df_player[['Opp_name','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]
df_player = df_player.set_index(['Opp_name','annee'])
df_player = df_player.dropna()
df_team = team_impact
df_team = df_team[['Opp','annee','PTS_diff','AST_diff','TRB_diff','FGA','TOV','PF']]
df_team = df_team.set_index(['Opp','annee'])
df_team = df_team.dropna()

x = df_coach.values
kmeans = KMeans(n_clusters=5, random_state=0).fit(x)
kmeans.labels_
df_coach['cluster'] = kmeans.labels_
df_coach.loc[df_coach.cluster == 0].count()

df_coach = df_coach.reset_index()

xp = df_player.values 
kmeansp = KMeans(n_clusters=5, random_state=0).fit(xp)
kmeansp.labels_
df_player['cluster'] = kmeansp.labels_
df_player.loc[df_player.cluster == 0].count()

df_player = df_player.reset_index()

xt = df_team.values
kmeansp = KMeans(n_clusters=5, random_state=0).fit(xt)
kmeansp.labels_
df_team['cluster'] = kmeansp.labels_
df_team.loc[df_team.cluster == 0].count()

df_team = df_team.reset_index()

df_coach = df_coach.rename(columns={"cluster":"cluster_coach",})
df_coach = df_coach[['Opp_Coach','annee','cluster_coach']]

df_player = df_player.rename(columns={"cluster":"cluster_player",})
df_player = df_player[['Opp_name','annee','cluster_player']]

df_team = df_team.rename(columns={"cluster":"cluster_team",})
df_team = df_team[['Opp','annee','cluster_team']]

### MERGE 

base[['age','jour']] = base.Age.str.split("-",expand=True,)
base[['minutes','sec']] = base.MP.str.split(":",expand=True,)

base = base[['full_name','Date','annee','Tm','Opp','Opp_name','Opp_Coach','age','minutes','GS',
             'Domicile','month','PTS','AST','TRB','FGA','TOV','PF','PTS_diff','AST_diff',
             'TRB_diff','FGA_moy','TOV_moy','PF_moy','BLK','STL','FG','FTA','FT',
             '3PA','3P','MP']]

base = pd.merge(base, df_coach, how = "left", on=["Opp_Coach","annee"])
base = pd.merge(base, df_player, how = "left", on=["Opp_name","annee"])
base = pd.merge(base, df_team, how = "left", on=["Opp","annee"])

### Base cluster

df_coach = df_coach.rename(columns={"cluster_coach":"cluster",})
df_player = df_player.rename(columns={"cluster_player":"cluster",})
df_team = df_team.rename(columns={"cluster_team":"cluster",})
df_coach = df_coach.rename(columns={"Opp_Coach":"Key",})
df_player = df_player.rename(columns={"Opp_name":"Key",})
df_team = df_team.rename(columns={"Opp":"Key",})

cluster = pd.merge(df_coach, df_team, how = "outer")
cluster = pd.merge(cluster, df_player, how = "outer")

cluster.to_csv("cluster.csv", sep=";")


### Base finale pour machine learning

data_ML=base.copy()
test=data_ML.loc[(data_ML['full_name']=="Giannis Antetokounmpo")&(data_ML['annee']==2021)]
data_ML['Prod'] = data_ML['PTS']+data_ML['AST']+data_ML['TRB']+data_ML['BLK']+data_ML['STL']-(data_ML['TOV']+data_ML[
    'PF']+(data_ML['FGA']-data_ML['FG'])+(data_ML['FTA']-data_ML['FT'])+(data_ML['3PA']-data_ML['3P']))
data_ML = data_ML[["full_name","Date","annee","Tm","Opp","Opp_name","Opp_Coach",
             "age","minutes","GS","Domicile","month","PTS","AST","TRB","FGA",
             "TOV","PF","PTS_diff","AST_diff","TRB_diff","FGA_moy","TOV_moy","PF_moy",
             "cluster_coach","cluster_player","cluster_team","Prod"]]

data_ML["minutes"] = pd.to_numeric(data_ML['minutes'], errors='coerce').convert_dtypes()
data_ML['Prod_min']=data_ML['Prod']/data_ML['minutes']
data_ML=data_ML.replace([np.inf, -np.inf], 0)

df2 = data_ML.groupby(['full_name'])['Prod_min'].max().reset_index()

df2 = df2.rename(columns={'Prod_min': 'Prod_min_max'})
df3 = data_ML.groupby(['full_name','annee'])['Prod_min'].mean().reset_index()
df3 = df3.rename(columns={'Prod_min': 'Prod_mean_opp'})
data_ML = pd.merge(data_ML, df2, on='full_name', how='inner')
data_ML = pd.merge(data_ML, df3, on=['full_name','annee'], how='inner')

data_ML['id_Prod']=data_ML['Prod_min']/data_ML['Prod_min_max']
indexNames = data_ML[ (data_ML['GS'] != '1') & (data_ML['GS'] != '0')].index
data_ML.drop(indexNames , inplace=True)

data_ML['GS']=data_ML.GS.astype(float)

count = data_ML.groupby('full_name').count().reset_index()
count = count[['full_name', 'Tm']]
count = count.rename(columns={"Tm":"count"})
indexNames = count[ (count['count'] < 10)].index
count.drop(indexNames , inplace=True)

data_ML = pd.merge(data_ML, count, on='full_name')
data_ML = data_ML.replace([np.inf, -np.inf], np.nan)
data_ML = data_ML.dropna() 
data_ML.to_csv("data_ML.csv", sep=";")