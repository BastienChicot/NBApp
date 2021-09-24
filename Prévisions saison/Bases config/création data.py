# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 19:16:37 2021

@author: basti
"""
import pandas as pd
import numpy as np
from joblib import load

model=load("Ridge_PTS.joblib")
roster=pd.read_csv("roster.csv",sep=";")
data=pd.read_csv("data_ML.csv",sep=";")

data['pred']=model.predict(data)
data['pred_pts']=np.exp(data['pred'])
data['error']=data['PTS']-data['pred_pts']

np.mean(data['error'])
np.percentile(data['error'],97.5)

### Erreur moyenne modèle == 0.7347
### IC 5 % -8.74 et 12.13 ==> on fera +- 5 

df=data.loc[data["annee"]==2021]
klay = data.loc[data['full_name']=="Klay Thompson"]

df=pd.concat([df,klay], ignore_index=True)

team_liste = ['atl','bos','brk','cho','cha','ind','was','phi','mia','mil',
              'orl','det','nyk','cle','tor','lal','lac','pho','uta','por',
              'sac','mem','nop','den','hou','sas','dal','gsw','okc','min']
t=pd.DataFrame(team_liste)
t[0]=t[0].str.upper()
t=t.rename(columns={0:"Opp"})

player=pd.DataFrame(np.unique(df['full_name'])).rename(columns={0:"full_name"})

t['key'] = 0
player['key'] = 0

t=t.merge(player, on='key', how='outer')
del t['key']

p_mean = df.groupby("full_name").mean().reset_index()
p_mean_opp=df.groupby(["full_name","Opp"]).mean().reset_index()
p_mean_opp=pd.merge(p_mean_opp,t, on=("Opp","full_name"),how="outer")

NANdf = p_mean_opp[p_mean_opp.isna().any(axis=1)]
NANdf=NANdf[['full_name',"Opp"]]
NANdf=NANdf.merge(p_mean,on="full_name",how="left")

p_mean_opp=p_mean_opp.dropna()
p_mean=p_mean.dropna()
fini2=p_mean
fini=pd.concat([p_mean_opp, NANdf], ignore_index=True)

cluster_p=df[["Opp_name","cluster_player"]]
cluster_p=cluster_p.drop_duplicates(['Opp_name'],keep="last")
cluster_p=cluster_p.rename(columns={"Opp_name":"full_name","cluster_player":"cluster_def"})

cluster_c=df[['Opp_Coach',"cluster_coach"]]
cluster_c=cluster_c.drop_duplicates(['Opp_Coach'],keep="last")
cluster_c=cluster_c.rename(columns={"Opp_Coach":"coach","cluster_coach":"cluster_c"})

coachs=pd.read_csv("coachs.csv",sep=";")
coachs=coachs.loc[coachs['annee']==2021]
coachs=coachs[["Coach","Tm"]]
coachs=coachs.rename(columns={"Coach":"coach"})

cluster_c=cluster_c.merge(coachs,on="coach",how="left")
cluster_c=cluster_c.dropna()
cluster_c

cluster_c.drop( cluster_c[ cluster_c['coach'] == "Lloyd Pierce"].index, inplace=True)

fini2=fini2.merge(cluster_p,on="full_name",how="left")
roster=roster[['full_name','Tm','starter']]
fini2=fini2.merge(roster,on="full_name",how="left")

def change_tm(df):
    df["Tm"]=df['Tm'].str.lower()
    df.loc[(df["Tm"]=="brk"),"Tm"]='bkn'
    df.loc[(df["Tm"]=="cho"),"Tm"]='cha'
    df.loc[(df["Tm"]=="gsw"),"Tm"]='gs'
    df.loc[(df["Tm"]=="nop"),"Tm"]='no'
    df.loc[(df["Tm"]=="nyk"),"Tm"]='ny'
    df.loc[(df["Tm"]=="sas"),"Tm"]='sa'
    df.loc[(df["Tm"]=="uta"),"Tm"]='utah'
    df.loc[(df["Tm"]=="was"),"Tm"]='wsh'
change_tm(cluster_c)
np.unique(cluster_c['Tm'])

fini=fini.merge(cluster_c,on="Tm",how="left")
fini2=fini2.merge(cluster_c,on="Tm",how="left")

fini['age']=fini["age"]+1
fini2['age']=fini2["age"]+1


fini['Opp']=fini['Opp'].str.lower()
fini.loc[(fini["Opp"]=="was"),"Opp"]='wsh'
np.unique(fini['Opp'])

final=fini[["full_name","Tm","starter","minutes","cluster_c","cluster_def","age",
            "FGA","TOV",'PF',"Prod_mean_opp","Opp"]]

final2=fini2[["full_name","Tm","starter","minutes","cluster_c","cluster_def","age",
            "FGA","TOV",'PF',"Prod_mean_opp"]]

final.to_csv("Base_fini.csv",sep=";")

final2.to_csv("Base_fini2.csv",sep=";")

### VERIF
player=np.unique(df['full_name'])
player=pd.DataFrame(player)
player=player.rename(columns={0:"full_name"})

player=pd.merge(player,roster,on='full_name',how='outer')