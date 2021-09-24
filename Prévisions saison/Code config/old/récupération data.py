# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:20:09 2021

@author: basti
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

liste_team = {"bos","bkn","atl","ny","phi","tor","gs","lac","lal","pho","sac",
              "chi","cle","det","ind","mil","cha","mia","orl","wsh","den","min",
              "okc","por","utah","dal","hou","mem","no","sa"}

df=[]
for team in liste_team :
    url = "https://www.espn.com/nba/team/roster/_/name/"+str(team)
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table')
    tab_data = pd.read_html(str(table[0]))[0]
    tab_data['Tm']=team
    df.append(tab_data)
    
final = pd.concat(df)
    
##STARTERS

url="http://www.espn.com/nba/depth"
r = requests.get(url)
r_html = r.text
soup = BeautifulSoup(r_html,'html.parser')
table=soup.find_all('table')
tab_data = pd.read_html(str(table[0]))[0]
t=tab_data.stack()

import re

final['nom']=final['Name'].astype('string')
final_cleaned = []
txt = list(final['nom'])
for i  in txt:
    t = re.sub(r"[0-9]+", "", i)
    final_cleaned.append(re.sub(r'^RT[\s]+', '', t))
final['full_name'] = final_cleaned
final['full_name'] = final['full_name'].astype('string')

#### STATS

url ="https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"

r = requests.get(url)
r_html = r.text
soup = BeautifulSoup(r_html,'html.parser')
table=soup.find_all('table',{"id":"per_game_stats"})
tab_data = pd.read_html(str(table[0]))[0]

indexNames = tab_data[ tab_data['Rk'] == 'Rk' ].index
# Delete these row indexes from dataFrame
tab_data.drop(indexNames , inplace=True)

tab_data['full_name']=tab_data['Player']
def nettoyage(df):
    df['full_name'] = df['full_name'].str.replace(u" Jr.", "")
    df['full_name'] = df['full_name'].str.replace(u" Sr.", "")
    df['full_name'] = df['full_name'].str.replace(u" II", "")
    df['full_name'] = df['full_name'].str.replace(u" III", "")
    df['full_name'] = df['full_name'].str.replace(u" IV", "")
    df['full_name'] = df['full_name'].str.replace(u"D.J.", "DJ")
    df['full_name'] = df['full_name'].str.replace(u"P.J.", "PJ")
    df['full_name'] = df['full_name'].str.replace(u"'", "")

    df['name_lower'] = df['full_name'].str.lower()
t=pd.DataFrame(t)
t=t.rename(columns={0:"full_name"})
nettoyage(t)
t=t.rename(columns={"full_name":"last"})

nettoyage(final)
tab = pd.DataFrame(t)
tab=tab.rename(columns={0:"full_name"})
nettoyage(tab)
tab['name'] = tab['name_lower2'].str[3:]
tab['starter']=1
# final['name_lower'] = final['full_name'].str.lower()
# tab_data['name_lower'] = tab_data['full_name'].str.lower()

# final['name_lower2']=final['name_lower'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
# tab_data['name_lower2']=tab_data['name_lower'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

result = pd.merge(final, tab_data, on="name_lower2", how="outer")

result = result[["full_name_x","Age_x","POS",'Tm_x',"GS","MP","FGA","TOV","name_lower2"]]

result = result.rename(columns={"full_name_x":"full_name", "Age_x":"age",'Tm_x':"Tm"})

df_ML = pd.read_csv("Base_travail.csv", sep=";")

df_ML=df_ML.loc[df_ML['annee']==2021]

df_coach=df_ML[['Opp_Coach','cluster_coach']]
df_def=df_ML[['Opp_name','cluster_player']]
df_ML = df_ML.drop_duplicates(['annee', 'full_name'],keep= 'last')
df_ML=df_ML[['full_name','carriere','game_rank','cluster']]

df_coach = df_coach.rename(columns={'Opp_Coach':"full_name"})
df_def = df_def.rename(columns={'Opp_name':"full_name",'cluster_player':"cluster_def"})

df_coach = df_coach.drop_duplicates(['full_name','cluster_coach'],keep= 'last')
df_def = df_def.drop_duplicates(['full_name','cluster_def'],keep= 'last')

nettoyage(df_ML)
nettoyage(df_coach)
nettoyage(df_def)

df_ML=df_ML[['name_lower2','carriere','game_rank','cluster']]
result = pd.merge(result, df_ML, on="name_lower2",how='outer')

df_def=df_def[['name_lower2','cluster_def']]
result = pd.merge(result, df_def, on="name_lower2",how="outer")

result = result.drop_duplicates(['full_name','age','Tm'],keep= 'last')

max_pts = pd.read_csv("max_pts.csv",sep=";")

nettoyage(max_pts)
max_pts=max_pts[["name_lower2","max_pts","min_pts"]]

result=pd.merge(result,max_pts,on="name_lower2",how="outer")
result = result.dropna(subset=['full_name'])
result['age']=result['age']+1
result["MP"] = result.MP.astype(float)
result["FGA"] = result.FGA.astype(float)
result["TOV"] = result.TOV.astype(float)

test=result.loc[result['Tm']=='por']

url_coach="http://www.espn.com/nba/coaches"
r = requests.get(url_coach)
r_html = r.text
soup = BeautifulSoup(r_html,'html.parser')
table=soup.find_all('table')
tab_coach = pd.read_html(str(table[0]))[0]

tab_coach = tab_coach.rename(columns={0:"full_name",3:"Tm"})    

nettoyage(tab_coach)
tab_coach=tab_coach[['name_lower2','Tm']]
tab_coach.loc[(tab_coach['Tm']=="Oklahoma City Thunder"), 'name_lower2']="marc daigneault"
df_coach = pd.merge(df_coach,tab_coach,on="name_lower2", how="outer")
df_coach = df_coach.drop_duplicates(['full_name','Tm'],keep= 'last')

df_coach = df_coach.dropna(subset=['Tm'])
tab_coach.loc[(tab_coach['Tm']=="Oklahoma City Thunder"), 'cluster_coach']=3

df_coach=df_coach[['name_lower2','cluster_coach','Tm']]
df_coach = df_coach[df_coach.name_lower2 != "coaches"]
df_coach = df_coach[df_coach.name_lower2 != "name"]
df_coach['cluster_coach']=3

# NANindex=result.index[result.isnull().any(axis=1)]

NANdf = result[result.isna().any(axis=1)]
nan2 = NANdf.loc[NANdf['MP']>=21]

del result['GS']
result.to_csv("base_joueurs.csv",sep=";")
df_coach.to_csv("base_coach.csv",sep=";")
NANdf.to_csv("base_NA.csv",sep=";")

###COMPLETION STATS
result = pd.read_csv("base_joueurs.csv",sep=";")


def creation_stat(full_name):
    
    result.loc[(result['name_lower2']==full_name), 'MP']=30
    result.loc[(result['name_lower2']==full_name), 'FGA']=8
    result.loc[(result['name_lower2']==full_name), 'TOV']=0
    result.loc[(result['name_lower2']==full_name), 'cluster']=6
    result.loc[(result['name_lower2']==full_name), 'cluster_def']=0
    result.loc[(result['name_lower2']==full_name), 'carriere']=0
    result.loc[(result['name_lower2']==full_name), 'game_rank']=0
    result.loc[(result['name_lower2']==full_name), 'max_pts']=20
    result.loc[(result['name_lower2']==full_name), 'min_pts']=0

profil=result.loc[result['name_lower2']=="robert covington"]

creation_stat("moses moody")

df = result.copy()

df= df.dropna()
df[['First','name']] = df.name_lower2.str.split(" ",expand=True,)
tab = tab[["name","starter"]]
del df["Unnamed: 0.1.1"]
d=df.copy()
d=pd.merge(d,tab,on="name",how="left")
d = d.drop_duplicates(['name_lower2'],keep= 'last')
d['starter']=d['starter'].fillna(0)

minutes = df.groupby(['Tm']).sum('MP')

d = d.rename(columns={'starter':"GS"})


d=pd.read_csv("base_test.csv",sep=";")
d = d.rename(columns={"MP":"minutes",'FGA':'FGA_moy','TOV':"TOV_moy"})
d['cluster_coach']=3
d.to_csv("base_test.csv",sep=";")