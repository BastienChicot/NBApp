# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 15:42:13 2021

@author: basti
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("evo_carriere.csv", sep = ";")
data.info()
data['Prod'] = data['PTS']+data['AST']+data['TRB']+data['BLK']+data['STL']-(data['TOV']+data[
    'PF']+(data['FGA']-data['FG'])+(data['FTA']-data['FT'])+(data['3PA']-data['3P']))
data['Prod_min']=data['Prod']/data['MP']

df2 = data.groupby(['full_name'])['Prod_min'].max().reset_index()

df2 = df2.rename(columns={'Prod_min': 'Prod_min_max'})

data = pd.merge(data, df2, on='full_name', how='inner')

data['id_Prod']=data['Prod_min']/data['Prod_min_max']

test = data.groupby(['full_name','periode'])['id_PRP'].mean().reset_index()
test=test.rename(columns={'id_PRP':'id_PRP_moy'})
data = pd.merge(data, test, on=['full_name','periode'], how='inner')

data[['year','month','day']] = data.Date.str.split("-",expand=True,)
data['annee_2']=data['year'].str[2:]
data['date_time']=data['annee_2']+data['month']+data['day']
data["date_time"]=data.date_time.astype(float)

data['date'] = pd.to_datetime(data['Date'])

data = data.dropna()
data["id_PRP_moy"]=data.id_PRP_moy.astype(float)
data.info()

full_name = "Damian Lillard"
graphbase= data.loc[data['full_name'] == full_name]

#ax = sns.lineplot(x = 'date', y = 'id_PRP_moy', data = graphbase, label='Evolution PRP par minute',
                 # color='red', linewidth=2.5)
ax = sns.regplot(x = 'date', y = 'id_Prod', data = graphbase, label='Evolution de la production par minute')
plt.title("Indices d'évolution en carrière de "+ full_name)
plt.ylabel("indice en carriere")
plt.xlabel('Date : AAMMJJ')
ax.legend(loc='upper left', borderpad=.2)
plt.show()

data = data[['Date','Age','Tm','Opp','GS','MP','joueur','full_name','year','month',
             'day','periode','Prod','Prod_min','Prod_min_max','id_Prod']]

data.to_csv("indice_evolution.csv", sep=";")
