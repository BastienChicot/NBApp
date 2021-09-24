# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:45:26 2021

@author: bchicot
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

team_liste = ['atl','bos','bkn','chi','cha','ind','wsh','phi','mia','mil',
              'orl','det','ny','cle','tor','lal','lac','pho','utah','por',
              'sac','mem','no','den','hou','sa','dal','gs','okc','min']

df=[]
for team in team_liste:
    url = "https://www.espn.com/nba/team/roster/_/name/"+str(team)
    try :
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table')
        tab_data = pd.read_html(str(table[0]))[0]
        
        tab_data['Tm'] = team 
      
        df.append(tab_data)
        
    except IndexError:        
        gotdata = 'null'

name=pd.concat(df)

import re
import string

name['Nom']=name['Name'].astype("string")
clean=[]
txt=list(name['Nom'])
for i in txt:
    t = re.sub(r'[0-9]+', "", i)
    clean.append(re.sub(r"^RT[\s]+", "", t))
name['full_name']=clean
name['full_name']=name['full_name'].astype('string')

name['full_name']=name['full_name'].str.replace(u' Jr.',"")
name['full_name']=name['full_name'].str.replace(u' Sr.',"")
name['full_name']=name['full_name'].str.replace(u' II',"")
name['full_name']=name['full_name'].str.replace(u' III',"")
name['full_name']=name['full_name'].str.replace(u' IV',"")
name['full_name']=name['full_name'].str.replace(u'P.J.',"PJ")
name['full_name']=name['full_name'].str.replace(u'D.J.',"DJ")
name['full_name']=name['full_name'].str.replace(u"'","")


name['name_lower']=name['full_name'].str.lower()

roster=name[["full_name","POS"]]

url="http://www.espn.com/nba/depth"
r = requests.get(url)
r_html = r.text
soup = BeautifulSoup(r_html,'html.parser')
table=soup.find_all('table')
tab_data = pd.read_html(str(table[0]))[0]
t=tab_data.stack()
##nettoyer le fichier avec le code récupération data

roster[['first','last']] = roster.full_name.str.split(" ",expand=True,) 
roster['letter']=roster['first'].str[:1]+". "
roster['name_lower']=(roster['letter']+roster['last']).str.lower()

roster=pd.merge(roster,tab,on="name_lower",how="left")
roster=roster[["full_name","Tm","starter"]]
roster['starter']=roster['starter'].fillna(0)
roster=roster.drop_duplicates(['full_name'],keep="last")
roster.to_csv("roster.csv",sep=";")

name[['First','Last']] = name.name_lower.str.split(" ",expand=True,) 

name['last_code']=name['Last'].str[:5] 
name['first_code']=name['First'].str[:2]

name["code"]=name["last_code"]+name["first_code"]+"01" 
name['letter']=name['last_code'].str[:1]

annee = '2021'

#scrape_nba()

code_list = finish['code']
letter_list=finish['letter']

df2=[]
df_manquant=pd.DataFrame(columns={"code"})

for code in code_list :
    for letter in letter_list:
        code = code  
        url = 'https://www.basketball-reference.com/players/a/'+(code)+'/gamelog/'+str(annee)
    
    try :
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'pgl_basic'})
        tab_data = pd.read_html(str(table[0]))[0]
        
        tab_data['code']=code
        
        df2.append(tab_data)
    
    except IndexError: 
        df_manquant.append({"code":code},ignore_index=True)
        gotdata = 'null'
    
final = pd.concat(df2)

import numpy as np
code_ok=np.unique(final['code'])

code_tot=pd.DataFrame(code_list)
code_fon=pd.DataFrame(code_ok)
code_fon=code_fon.rename(columns={0:"code"})
code_fon['OK']=1
comparaison = pd.merge(code_tot,code_fon,on="code",how='outer')

nan_df=comparaison[comparaison.isna().any(axis=1)]
full_name_df=finish[["full_name","code"]]
nan_df=pd.merge(nan_df,full_name_df,on="code")

finish = name[["full_name","code","letter","POS","Age"]]

finish.loc[(finish["full_name"]=="Wesley Matthews"),"code"]='matthwe02'
finish.to_csv("code_player.csv",sep=";")

final.to_csv("/home/bastien/Bureau/NBA/nba_players_stats"+str(annee)+".csv", sep =";")
