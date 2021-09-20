import pandas as pd
import numpy as np


players_base = pd.read_csv('nba_players.csv', sep=";")
players_base = players_base.drop(["first_name","last_name","lettre"], axis=1)
players_base = players_base.rename(columns={'code': 'joueur'})

coach = pd.read_csv('nba_coaches.csv', sep=",")

annees = [#'2006','2007','2008','2009','2010',
          #'2011','2012','2013',
          #'2014','2015','2016',
          #'2017','2018',
          #'2019',
          '2020',
          '2021'
         ]
df = []
dfoppteam=[]
dfoppplayer=[]
dfoppcoach=[]

for annee in annees :
    data=pd.read_csv('nba_players_stats_'+(annee)+'.csv', sep=",")
    

    data = data.drop(["Unnamed: 0", "FG%", "3P%", "FT%"], axis=1)
    if annee<'2022' :
        indexNames = data[ data['Rk'] == 'Rk' ].index
        # Delete these row indexes from dataFrame
        data.drop(indexNames , inplace=True)
    
    if annee== '2021':        
        indexNames2 = data[ data['GS'] == 'Did Not Dress' ].index
        indexNames3 = data[ data['GS'] == 'Did Not Play' ].index
        indexNames4 = data[ data['GS'] == 'Inactive' ].index
        indexNames5 = data[ data['GS'] == 'Not With Team' ].index
        data.drop(indexNames2 , inplace=True)
        data.drop(indexNames3 , inplace=True)
        data.drop(indexNames4 , inplace=True)
        data.drop(indexNames5 , inplace=True)

    data['Domicile'] = data['Unnamed: 5'].apply(lambda x: '1' if x =="@" else '0')
    data = pd.merge(data, players_base, how="inner", on=["joueur"])
    data= pd.merge(data, coach, how = "inner", on = ["annee", "Tm"])
    data[['year','month', 'day']] = data.Date.str.split("-",expand=True,)
    data['year']=str(annee)
    
    data['id_joueur'] = data["year"]+data["month"]+data["day"]+data["Tm"]+data[
        "Opp"]+data["GS"]+data["position"]
    data['id_opp'] = data["year"]+data["month"]+data["day"]+data["Opp"]+data[
        "Tm"]+data["GS"]+data["position"]
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
    
    data["PTS"] = data.PTS.astype(float)
    data["AST"] = data.AST.astype(float)
    data["TRB"] = data.TRB.astype(float)
    data["FG"] = data.FG.astype(float)
    data["FGA"] = data.FGA.astype(float)
    data["TOV"] = data.TOV.astype(float)
    data["PF"] = data.PF.astype(float)
    data["BLK"] = data.BLK.astype(float)
    data["STL"] = data.STL.astype(float)
    
    df.append(data)
base = pd.concat(df)
base.to_csv('player_stat-20-030421.csv', sep=";")   
 
    stat = data.groupby(['full_name','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()
    stat_oppteam = data.groupby(['full_name','Opp','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()
    stat_oppplayer = data.groupby(['full_name','Opp_name', 'Opp','Opp_Coach','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()
    stat_oppcoach = data.groupby(['full_name','Opp_Coach','annee'])['PTS','AST','TRB','FG','FGA','TOV','PF',
    'BLK','STL'].mean().reset_index()
    
    stat_oppteam = pd.merge(stat_oppteam, stat, how = "left", on=["full_name"])
    stat_oppplayer = pd.merge(stat_oppplayer, stat, how = "left", on=["full_name"])
    stat_oppcoach = pd.merge(stat_oppcoach, stat, how = "left", on=["full_name"])
    
    df_list = [stat_oppteam, stat_oppplayer, stat_oppcoach]
    for df in df_list:
        df["PTS_diff"] = df["PTS_y"]-df["PTS_x"]
        df["AST_diff"] = df["AST_y"]-df["AST_x"]
        df["TRB_diff"] = df["TRB_y"]-df["TRB_x"]
        df["FG_diff"] = df["FG_y"]-df["FG_x"]
        df["FGA_diff"] = df["FGA_y"]-df["FGA_x"]
        df["TOV_diff"] = df["TOV_y"]-df["TOV_x"]
        df["PF_diff"] = df["PF_y"]-df["PF_x"]
        df["BLK_diff"] = df["BLK_y"]-df["BLK_x"]
        df["STL_diff"] = df["STL_y"]-df["STL_x"]
        
    col_list = ['PTS_y','PTS_x','AST_y','AST_x','TRB_y','TRB_x','FG_y','FG_x',
                'FGA_y','FGA_x','TOV_y','TOV_x','PF_y','PF_x','BLK_y','BLK_x',
                'STL_y','STL_x']
    diff_oppteam = stat_oppteam.drop(col_list,axis=1)
    diff_oppplayer = stat_oppplayer.drop(col_list,axis=1)
    diff_oppcoach = stat_oppcoach.drop(col_list,axis=1)
    
    dfoppteam.append(diff_oppteam)
    dfoppplayer.append(diff_oppplayer)
    dfoppcoach.append(diff_oppcoach)
    
final_oppteam = pd.concat(dfoppteam)
final_oppplayer = pd.concat(dfoppplayer)
final_oppcoach = pd.concat(dfoppcoach)

final_oppteam.to_csv("final_oppteam.csv", sep =";")
final_oppplayer.to_csv("final_oppplayer.csv", sep =";")
final_oppcoach.to_csv("final_oppcoach.csv", sep =";")