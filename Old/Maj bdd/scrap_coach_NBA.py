import requests
from bs4 import BeautifulSoup
import pandas as pd

annees = ['19',
         '20','21']

df=[]

for annee in annees:
    try : 
        url = 'https://www.basketball-reference.com/leagues/NBA_20'+(annee)+'_coaches.html'

        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'NBA_coaches'})
        tab_data = pd.read_html(str(table[0]))[0]
        tab_data['annee'] = '20'+(annee)
     
        df.append(tab_data)
        
    except IndexError:        
        gotdata = 'null'

final_coach = pd.concat(df)
final_coach.to_csv("/home/bastien/Bureau/NBA/Stats joueurs/nba_coaches_stats.csv", sep =";")
