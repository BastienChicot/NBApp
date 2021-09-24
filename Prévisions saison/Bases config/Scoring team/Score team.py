# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 17:16:03 2021

@author: basti
"""

import pandas as pd

adv=pd.read_csv("advanced.txt",sep=",")
opp=pd.read_csv("Opponent.txt",sep=",")
per=pd.read_csv("per_game.txt",sep=",")

opp=opp.rename(columns={"FG%":"FG%opp","3P%":"3P%opp","2P%":"2P%opp","TRB":"TRBopp",
                        "AST":"ASTopp","STL":"STLopp","BLK":"BLKopp","TOV":"TOVopp",
                        "PTS":'PTSopp'})

del per["MP"]
del per["PF"]

import numpy as np

croissant=adv[["Team","TOV%"]]
del adv["TOV%"]
adv['TOVopp']=opp["TOVopp"]
del opp["TOVopp"]
opp["TOV"]=per["TOV"]
del per["TOV"]

opp=opp.merge(croissant,on="Team")
per=per.merge(adv,on="Team")

for col in per.columns:
    new_col=str("score_")+col
    per[new_col]=per[col].rank()

for col in opp.columns:
    new_col=str("score_")+col
    opp[new_col]=opp[col].rank(ascending=False)
    
per=per.set_index("Team")
opp=opp.set_index("Team")
per.info()
opp.info()
calc_per=per[per.columns[13:25]]    
calc_opp=opp[opp.columns[11:21]]
calc_per=calc_per.reset_index()
calc_opp=calc_opp.reset_index()

calc = pd.merge(calc_per,calc_opp,on="Team")
calc=calc.set_index("Team")
calc['total']=calc.sum(axis=1)
calc=calc.reset_index()

np.mean(per["PTS"])
np.std(calc['total'])
np.var(per['PTS'])
16/112

###14% de modif max
calc["indice"]=(calc["total"]-min(calc['total']))/(max(calc['total'])-min(calc['total']))
calc["test"]=calc["indice"].rank()
l = list(np.arange(0.85,1.15,0.01))
score=pd.DataFrame(l)
score["test"]=score[0].rank()
score.loc[(score["test"]==11), "test"]=11.5
score.loc[(score["test"]==20), "test"]=20.5

calc=calc.merge(score,on="test")

calc=calc[["Team",0]]
calc=calc.rename(columns={0:"indice"})

np.unique(calc["Team"])
Tm=pd.DataFrame({"Team":['Atlanta Hawks*', 'Boston Celtics*', 'Brooklyn Nets*',
       'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers',
       'Dallas Mavericks*', 'Denver Nuggets*', 'Detroit Pistons',
       'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
       'Los Angeles Clippers*', 'Los Angeles Lakers*',
       'Memphis Grizzlies*', 'Miami Heat*', 'Milwaukee Bucks*',
       'Minnesota Timberwolves', 'New Orleans Pelicans',
       'New York Knicks*', 'Oklahoma City Thunder', 'Orlando Magic',
       'Philadelphia 76ers*', 'Phoenix Suns*', 'Portland Trail Blazers*',
       'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
       'Utah Jazz*', 'Washington Wizards*'],"Tm": ["atl","bos","bkn","cha","chi","cle","dal","den","det","gs","hou","ind","lac","lal",
                                     "mem","mia","mil","min","no","ny","okc","orl","phi","pho","por","sac",
                                     "sa","tor","utah","wsh"]})
                                                   
calc=calc.merge(Tm,on="Team")

calc=calc[["Tm",'indice']]

calc.to_csv("indice_team.csv",sep=";")