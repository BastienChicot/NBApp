import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


players_base = pd.read_csv('nba_players.csv', sep=";")
# players_base = players_base.drop(["first_name","last_name","lettre"], axis=1)
players_base = players_base[['code','full_name']]
players_base = players_base.rename(columns={'code': 'joueur'})

coach = pd.read_csv('nba_coaches.csv', sep=",")

annees = ['2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',
          '2016','2017','2018','2019','2020','2021'
         ]

df=[]

for annee in annees :
    data=pd.read_csv('nba_players_stats_'+(annee)+'.csv', sep=",")
    if annee<'2022' :
        indexNames = data[ data['Rk'] == 'Rk' ].index
# Delete these row indexes from dataFrame
        data.drop(indexNames , inplace=True)
    try:        
        indexNames2 = data[ data['GS'] == 'Did Not Dress' ].index
        indexNames3 = data[ data['GS'] == 'Did Not Play' ].index
        indexNames4 = data[ data['GS'] == 'Inactive' ].index
        indexNames5 = data[ data['GS'] == 'Not With Team' ].index
        indexNames6 = data[ data['GS'] == 'Player Suspended' ].index
        data.drop(indexNames2 , inplace=True)
        data.drop(indexNames3 , inplace=True)
        data.drop(indexNames4 , inplace=True)
        data.drop(indexNames5 , inplace=True)
        data.drop(indexNames6 , inplace=True)
    except:
        pass
        
    data = pd.merge(data, players_base, how="inner", on=["joueur"])
    
    data[['year','month','day']] = data.Date.str.split("-",expand=True,)
    data['periode']=data['year']+data['month']
    
    data["PTS"] = data.PTS.astype(float)
    data["AST"] = data.AST.astype(float)
    data["TRB"] = data.TRB.astype(float)
    data["TOV"] = data.TOV.astype(float)
    data["PF"] = data.PF.astype(float)
    data["BLK"] = data.BLK.astype(float)
    data["STL"] = data.STL.astype(float)
    data["periode"]=data.periode.astype(float)
    
    data['PRP']=data['PTS']+data['TRB']+data['AST']
    data['DEF']=data['BLK']+data['STL']
    data['MIS']=data['TOV']+data['PF']
        
    #data=data[['full_name','periode','MP','PRP','DEF','MIS']]

    data['MP'] = data['MP'].str.replace(':','.')
    data["MP"] = data.MP.astype(float)
    
    data = data.groupby(['full_name','year'])['PRP','DEF','MIS','MP'].mean().reset_index()
    data = data.drop_duplicates(['full_name','year'],keep= 'last')
    
    df.append(data)
    
carriere = pd.concat(df)
carriere = carriere.drop_duplicates(['full_name','year'],keep= 'last')

carriere.to_csv("evo_carriere.csv", sep =";")

test=pd.read_csv("evo_carriere.csv",sep=";")

lbj=test.loc[test['full_name']=="LeBron James"]

