# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 17:15:20 2021

@author: basti
"""

import pandas as pd
from joblib import load
import numpy as np

indice=pd.read_csv("Bases config/Scoring team/indice_team.csv",sep=";")
df=pd.read_csv("Base_fini2.csv",sep=";")

#test2=df.loc[df['full_name']=="Anfernee Simons"]
#df.loc[(df['full_name']=="Devin Booker"), "minutes"]=34
#df.to_csv("Base_fini2.csv",sep=";")
del df['Unnamed: 0']
del indice['Unnamed: 0']
# del df['Unnamed: 0.1']
# df=df.rename(columns={"starter":"GS","FGA":"FGA_moy",
#                        "TOV":"TOV_moy","PF":"PF_moy"})
# df=df.merge(roster,on="full_name",how="left")
# df["code"]=df['POS'].map(str) + df['Tm'].map(str) + df['GS'].map(str)
model=load("Ridge_PTS.joblib")

def absence(donnee):
    donnee['prob']=(0.25/40**4)*(donnee['age']**4)
    donnee['abs']=np.random.binomial(1,donnee['prob'])
    donnee=donnee.drop(donnee.loc[donnee["abs"]==1].index)
    return(donnee)

def blesse(data,equipe,month):
    if (equipe=="lac") & (month>8):
        data=data.drop(data.loc[data['full_name']=="Kawhi Leonard"].index)
    if(equipe=="den")&(month>8):
        data=data.drop(data.loc[data['full_name']=="Jamal Murray"].index)
    if(equipe=="gs")&(month>8):
        data=data.drop(data.loc[data['full_name']=="Klay Thompson"].index)
    if(equipe=="mia")&(month>8 & month<12):
        data=data.drop(data.loc[data['full_name']=="Victor Oladipo"].index)
    else :
        data=data
    return(data)


def create_calendar(team_proj):
    code_tm=pd.read_csv("Calendriers/Codes_Equipes.csv",sep=";")
    calendar=pd.read_csv("Calendriers/"+str(team_proj)+".txt",sep=",")
    calendar['Date'] = pd.to_datetime(calendar.Date)
    calendar['month'] = pd.DatetimeIndex(calendar["Date"]).month
    calendrier=pd.merge(calendar,code_tm,on="Team")
    calendrier = calendrier[['Opp','month','Date']]
    return(calendrier)

# bilan=pd.DataFrame(columns={"Date","Team","Opp","Victoire","Défaite","score_team",
#                     "score_opp"})

### Ecart type minutes == 6.4 minutes
### Ecart type point moyen == 5.74 et moyenne == -0.1109

def simul_match(data,month):
    data["Opp_code"]=data['POS'].map(str) + data['Opp'].map(str) + data['GS'].map(str)

    liste_code = data['Opp_code']
    Opp=(data['Opp'])
    Opp=pd.DataFrame(Opp)
    Opp=Opp.drop_duplicates(["Opp"])
    Opp=str(*Opp["Opp"])
    
    codes=[]
    for code in liste_code:
        df_code=df.loc[df['code']==code]
        df_code=df_code.drop_duplicates(['code'])
        codes.append(df_code)
    X = pd.concat(codes)
    X = X[["code","cluster_def"]]
    X= X.rename(columns={"code":"Opp_code","cluster_def":"cluster_player"})
    Y = df.loc[df['Tm']==Opp]
    Y=Y[["Tm","cluster_c"]]
    Y = Y.drop_duplicates(["cluster_c"])
    Y = Y.rename(columns={"Tm":"Opp","cluster_c":"cluster_coach"})

    data=pd.merge(data,X,on="Opp_code",how="left")
    data=pd.merge(data,Y,on="Opp",how="left")
    data = data.drop_duplicates(['full_name','Tm'],keep= 'last')
    data['cluster_player']=data['cluster_player'].fillna(0)
    
    data['month']=month
    data['bonus_malus']=np.random.normal(0.7347, 4, len(data))
    data['minutes_var']=np.random.normal(0,3,len(data))
    data['minutes']=data['minutes']+data['minutes_var']
    
    data['score']=model.predict(data)
    data['ptspred']=np.exp(data['score'])
    data['pts_pred']=data['ptspred']+data['bonus_malus']
    data["score_tot"]=sum(data["pts_pred"])
    data["score_fin"]=(data['score_tot']/sum(data["minutes"]))*240
    return(data)

def simulation(team_proj):
    equipe=team_proj
    bilan=pd.DataFrame(columns={"Date","Team","Opp","Victoire","Défaite","score_team",
                     "score_opp"})
    calendrier=create_calendar(team_proj)
    for i in range(len(calendrier)):
        try:
            Opp=calendrier.loc[i, "Opp"]
            month=calendrier.loc[i,"month"]
            date = calendrier.loc[i,"Date"]
            df_team=df.loc[(df['Tm']==equipe)]
            df_Opp=df.loc[(df['Tm']==Opp)]
            df_team['Opp']=Opp
            df_Opp['Opp']=equipe
            df_team=blesse(df_team,equipe,month)
            df_Opp=blesse(df_Opp,Opp,month)
            df_team=absence(df_team)
            df_Opp=absence(df_Opp)
            df_team=simul_match(df_team,month)
            df_Opp=simul_match(df_Opp,month)
            
            ind_team=indice.loc[indice["Tm"]==equipe]
            ind_opp=indice.loc[indice["Tm"]==Opp]
            
            score_t = df_team.drop_duplicates(['score_fin'],keep="last")
            score_O = df_Opp.drop_duplicates(['score_fin'],keep="last")
            score_team=float(score_t['score_fin'])*float(ind_team['indice'])
            score_Opp=float(score_O['score_fin'])*float(ind_opp['indice'])
            if score_team>score_Opp:
                Victoire=1
                Defaite=0
            else:
                Defaite=1
                Victoire=0
            bilan=bilan.append({"Date":date,"Team":equipe,"Opp":Opp,"score_team":score_team,
                                "score_opp":score_Opp,"Victoire":Victoire,"Défaite":Defaite},ignore_index=True)
        except:
            pass
    return(bilan)

# bilan=simulation("utah")
# print("Nombre de victoires : " + str(sum(bilan['Victoire'])) + " \nNombre de Défaites : " + str(sum(bilan['Défaite'])))

liste_team=np.unique(df['Tm'])

final=[]

for team in liste_team:
    sim = pd.DataFrame(columns={"Team","simulation","victoire","defaite"})
    for i in range (80):
        bilan=simulation(team)
        sim=sim.append({"Team":team,"simulation":i,"victoire":sum(bilan['Victoire']),"defaite":sum(bilan['Défaite'])},
                       ignore_index=True)   
    final.append(sim)   

liste_east=["atl","bos","cle","cha","chi","det","phi","mia","orl","wsh","ind","bkn",
            "ny","tor","mil"]

df_fin=pd.concat(final)
df_fin.to_csv("50_simu.csv",sep=";")
df_fin['victoire']=df_fin.victoire.astype(float)
df_fin['defaite']=df_fin.defaite.astype(float)
df_fin['total']=df_fin['victoire']+df_fin['defaite']

mean= df_fin.groupby(df_fin['Team']).mean().reset_index()
mean=mean.rename(columns={"victoire":"wins","defaite":"losses","total":"GP"})
conf_east=mean.loc[mean['Team'].isin(liste_east)]
conf_west=mean.drop(mean.loc[mean['Team'].isin(liste_east)].index)
###Introduce rookies and team agreement scores
mean=mean.sort_values(by=['losses'])
conf_east=conf_east.sort_values(by=['losses'])
conf_west=conf_west.sort_values(by=['losses'])
mean.to_csv("80_simu_results.csv",sep=";")

df_team=df.loc[(df['Tm']=="pho")]
df_Opp=df.loc[(df['Tm']=='lac')]
df_team['Opp']="lac"
df_Opp['Opp']="pho"
df_team=blesse(df_team,"pho",10)
df_Opp=blesse(df_Opp,"lac",10)

df_team=absence(df_team)
df_Opp=absence(df_Opp)
    
df_team=simul_match(df_team,10)
df_Opp=simul_match(df_Opp,10)

bilan=simulation('pho')
bilan["Victoire"]=bilan.Victoire.astype(float)
sum(bilan['Victoire'])

mean=df.groupby(['Tm']).mean().reset_index()
mean_opp=df.groupby(["Tm","Opp"]).mean().reset_index()
mean_game=mean_opp.groupby(['Tm']).mean().reset_index()

df.loc[(df['name_lower2']=="malachi flynn"), 'FGA_moy']=4
df=df.append({"full_name":"Klay Thompson","age":32,"POS":"SG","Tm":'gs',
              "minutes":34,"FGA_moy":18,"TOV_moy":1.5,"name_lower2":"klay thompson",
              "carriere":8,"game_rank":615,"cluster":5,"cluster_def":3,"max_pts":60,
              "min_pts":4,"first":"klay","last":"thompson","GS":1,"cluster_coach":3,
              "code":"SGgs1.0"},ignore_index=True)
