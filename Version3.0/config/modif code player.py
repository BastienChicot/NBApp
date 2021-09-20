# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 16:58:55 2021

@author: basti
"""

import pandas as pd

### Pour récupérer et obtenir les code des joueurs ==> Prévisions saison
df1=pd.read_csv("data/nba_players.csv",sep=";")
df2=pd.read_csv("data/code_player.csv",sep=";")

del df2['Unnamed: 0']
df2=df2.rename(columns={"POS":"position","letter":"lettre"})

df1.info()
df2.info()

df2.to_csv("data/nba_players.csv",sep=";")