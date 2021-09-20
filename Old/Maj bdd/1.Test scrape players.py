import requests
from bs4 import BeautifulSoup
import pandas as pd

player_name = pd.read_csv("nba_players.csv", sep = ";")

annee = '2021'

#scrape_nba()
code_list = player_name['code']
lettre_list = player_name['lettre']

df=[]

for code in code_list :
    for lettre in lettre_list :
        code = code
        url = 'https://www.basketball-reference.com/players/a/'+(code)+'01/gamelog/'+str(annee)
  
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