# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 17:02:37 2021

@author: basti
"""

import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import tkinter as tk
from tkinter import ttk
from joblib import load
from pandastable import Table

df=pd.read_csv("data/data_ML.csv", sep=";")

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")
indice=pd.read_csv("data/indice_team.csv",sep=";")

def prp_en_carriere(full_name):
    data = pd.read_csv("data/evo_carriere.csv", sep =";")
    players_base = pd.read_csv('data/nba_players.csv', sep=";")

    data = pd.merge(data, players_base, how="inner", on = ['full_name'])
    graphbase= data.loc[data['full_name'] == full_name]
    plt.title("Statistiques en carrière de "+full_name)
    plt.plot(graphbase['year'],graphbase['PRP'],"r",marker="+", label="Points + Rebonds + Passes")
    plt.plot(graphbase['year'],graphbase['DEF'],"b",marker="+", label="Contres + interceptions")
    plt.plot(graphbase['year'],graphbase['MIS'],"y",marker="+", label="Balles perdues + Fautes")
    plt.plot(graphbase['year'],graphbase['MP'],"k",marker="+", label = "Minutes jouées")
    plt.xlabel('Années')
    plt.legend()
    plt.show()

def stat_20matchs_splits(code,annee):

    root2 = tk.Tk()
    root2.geometry('1750x500')
    root2.iconbitmap('config/icone.ico')
    root2.title("Statistique au cours des derniers matchs")
    canvas = tk.Canvas(root2)
    
    scrollbar=tk.Scrollbar(canvas,orient="vertical",command=canvas.yview)
    scrollbarix=tk.Scrollbar(canvas,orient="horizontal",command=canvas.xview)
    
    #Création des cadres
    fram0 = tk.LabelFrame(canvas, text="Stat sur les 20 derniers matchs")
    fram0.grid(row=0,column=0)
    fram2 = tk.LabelFrame(canvas, text="Stat splits en carrière")
    fram2.grid(row=0,column=0)
    
    canvas.create_window(0,250,window=fram0, anchor='w')
    canvas.create_window(0,500,window=fram2, anchor='w')
    
    #Stat 15 derniers matchs
    url = 'https://www.basketball-reference.com/players/a/'+str(code)+'/gamelog/'+str(annee)
    
    try :
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'pgl_basic'})
        tab_data = pd.read_html(str(table[0]))[0]
                
        tab_data['url'] = url
        tab_data['joueur'] = code
        tab_data['annee'] = annee
            
    except IndexError:        
        gotdata = 'null'
            
    if annee<"2022" :
        indexNames = tab_data[tab_data['Rk'] == 'Rk' ].index
            # Delete these row indexes from dataFrame
        tab_data.drop(indexNames , inplace=True)
            
    tab_data['Domicile'] = tab_data['Unnamed: 5'].apply(lambda x: '1' if x =="@" else '0')
    
    tab_data[['year','month', 'day']] = tab_data.Date.str.split("-",expand=True,)
    tab_data['year']=str(annee)
    
    tab_data = tab_data[['Date','Opp','PTS','AST','TRB','PF','MP','Domicile']]
    
    tab_data2 = tab_data.tail(20)

    td2 = ttk.Treeview(fram0)
    td2.pack(fill="both", expand=True, side="left")

    scrolly4 = tk.Scrollbar(fram0, orient ="vertical", command=td2.yview)
    scrollx4 = tk.Scrollbar(fram0, orient ="horizontal", command=td2.xview)
    td2.configure(xscrollcommand=scrollx4.set , yscrollcommand=scrolly4.set)
    scrollx4.pack(side="bottom",fill="x")
    scrolly4.pack(side="right",expand=True, fill="y")
    
    td2["column"] = list(tab_data2.columns)
    td2["show"]="headings"
    for column in td2["column"]:
        td2.heading(column, text=column)
    
    tab_data2_rows = tab_data2.to_numpy().tolist()
    for row in tab_data2_rows :
        td2.insert("","end", values = row)
    
    url3 = 'https://www.basketball-reference.com/players/a/'+str(code)+'/splits/'
    df_splits_career=[]

    try :
        r = requests.get(url3)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        tab_career=soup.find_all('table', {'id' : 'splits'})
        df_splits_career = pd.read_html(str(tab_career[0]))[0]
        
    except IndexError:        
        gotdata = 'null'
   
    df_splits_career = df_splits_career.iloc[:, np.r_[1:4,29:33]]
           
    df_splits_career = df_splits_career.groupby(axis = 1, level = 1).sum()
    df_splits_career = df_splits_career.set_index(['Value'])
    df_splits_career = df_splits_career.loc[df_splits_career.index.isin(['Home','Road','Monday','Tuesday','Wednesday','Thursday','Friday',
                                                                             'Saturday','Sunday','0 Days','1 Day','2 Days','3+ Days','Eastern',
                                                                             'Western','Atlantic','Central','Northwest','Southeast','Southwest',
                                                                             'Pacific'])] 
    df_splits_career.reset_index(level=0, inplace=True)

    tssc = ttk.Treeview(fram2)
    tssc.pack(fill="both", expand=True, side="left")

    scrolly0 = tk.Scrollbar(fram2, orient ="vertical", command=tssc.yview)
    scrollx0 = tk.Scrollbar(fram2, orient ="horizontal", command=tssc.xview)
    tssc.configure(xscrollcommand=scrollx0.set , yscrollcommand=scrolly0.set)
    scrollx0.pack(side="bottom",fill="x")
    scrolly0.pack(side="right", expand=True,fill="y")

    tssc["column"] = list(df_splits_career.columns)
    tssc["show"]="headings"
    for column in tssc["column"]:
        tssc.heading(column, text=column)

    df_splits_career_rows = df_splits_career.to_numpy().tolist()
    for row in df_splits_career_rows :
        tssc.insert("","end", values = row)
    
    canvas.update_idletasks()
    
    canvas.configure(scrollregion=canvas.bbox('all'), 
                     yscrollcommand=scrollbar.set, xscrollcommand=scrollbarix.set)
                 
    canvas.pack(expand=True, fill='both', side="left")
    scrollbar.pack(fill='both', side="right")
    scrollbarix.pack(fill='both', side="bottom")
    
    root2.mainloop()

def stat_Opp_team(full_name,Opp):
    root3 = tk.Tk()
    root3.geometry('1500x350')
    root3.iconbitmap('config/icone.ico')
    root3.title("Statistiques contre l'équipe adverse")
    canvas2 = tk.Canvas(root3)
    
    scrollbar=tk.Scrollbar(canvas2,orient="vertical",command=canvas2.yview)
    scrollbarix=tk.Scrollbar(canvas2,orient="horizontal",command=canvas2.xview)
    
    #Création des cadres
    cadre = tk.LabelFrame(canvas2, text="Stat contre " + str(Opp))
    cadre.grid(row=0,column=0)
    
    canvas2.create_window(0,550,window=cadre, anchor='w')

    A = df.loc[(df["full_name"] == full_name) & (df["Opp"] == Opp)]
    A["PTS_diff"] = round(A['PTS_diff'],2)
    A["AST_diff"] = round(A['AST_diff'],2)
    A["TRB_diff"] = round(A['TRB_diff'],2)
    A = A[['Opp',"Opp_name","Opp_Coach","minutes","Domicile","PTS","AST","TRB","FGA",
           'annee','PTS_diff','AST_diff','TRB_diff']]

    tv1 = ttk.Treeview(cadre)
    tv1.pack(fill="both", expand=True, side="left")

    scrolly = tk.Scrollbar(cadre, orient ="vertical", command=tv1.yview)
    scrollx = tk.Scrollbar(cadre, orient ="horizontal", command=tv1.xview)
    tv1.configure(xscrollcommand=scrollx.set , yscrollcommand=scrolly.set)
    scrollx.pack(side="bottom",fill="both")
    scrolly.pack(side="right", expand=True,fill="y")

    tv1["column"] = list(A.columns)
    tv1["show"]="headings"
    for column in tv1["column"]:
        tv1.heading(column, text=column)

    A_rows = A.to_numpy().tolist()
    for row in A_rows :
        tv1.insert("","end", values = row)
    
    
    canvas2.update_idletasks()
    
    canvas2.configure(scrollregion=canvas2.bbox('all'), 
                     yscrollcommand=scrollbar.set, xscrollcommand=scrollbarix.set)
                 
    canvas2.pack(expand=True, fill='both', side="left")
    scrollbar.pack(fill='both', side="right")
    scrollbarix.pack(fill='both', side="bottom")
    
    root3.mainloop()

def stat_teams (player_team,Opp):
    root4 = tk.Tk()
    root4.geometry('1750x200')
    root4.iconbitmap('config/icone.ico')
    root4.title("Comparaison des équipes")
    
    canvas3 = tk.Canvas(root4)
    
    scrollbar=tk.Scrollbar(canvas3,orient="vertical",command=canvas3.yview)
    scrollbarix=tk.Scrollbar(canvas3,orient="horizontal",command=canvas3.xview)
    
    #Création des cadres
    cadre3 = tk.LabelFrame(canvas3, text="Defensive rating from lineups.com")
    cadre3.grid(row=0,column=0)
    
    canvas3.create_window(0,250,window=cadre3, anchor='w')
    
    url4 = "https://www.lineups.com/nba/team-rankings/defense"
    r = requests.get(url4)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table', {'class' : 'multi-row-data-table t-stripped'})
    tab_team = pd.read_html(str(table[0]))[0]

    team_code=pd.read_csv('data/code_team.csv', sep=';')
    
    L = pd.merge(tab_team,team_code, on='TEAM')

    M = L.loc[L['Opp_team'] == player_team]
    N = L.loc[L['Opp_team'] == Opp]

    O = M.append(N)
    O = O[['TEAM','PTS ALLOW','REB ALLOW','AST ALLOW','FG ALLOW','3PT ALLOW',
           'OPP FG%','OPP 3PT%','DEF RTG']]
    
    tvt = ttk.Treeview(cadre3)
    tvt.pack(fill="both", expand=True)
    
    scrollyt = tk.Scrollbar(cadre3, orient ="vertical", command=tvt.yview)
    scrollxt = tk.Scrollbar(cadre3, orient ="horizontal", command=tvt.xview)
    tvt.configure(xscrollcommand=scrollxt.set , yscrollcommand=scrollyt.set)
    scrollxt.pack(side="bottom",fill="both")
    scrollyt.pack(side="right", expand=True,fill="y")
    
    tvt["column"] = list(O.columns)
    tvt["show"]="headings"
    for column in tvt["column"]:
        tvt.heading(column, text=column)

    O_rows = O.to_numpy().tolist()
    for row in O_rows :
        tvt.insert("","end", values = row)

    #ûconfig canvas
    canvas3.update_idletasks()
    
    canvas3.configure(scrollregion=canvas3.bbox('all'), 
                     yscrollcommand=scrollbar.set, xscrollcommand=scrollbarix.set)
                 
    canvas3.pack(expand=True, fill='both', side="left")
    scrollbar.pack(fill='both', side="right")
    scrollbarix.pack(fill='both', side="bottom")
    
    root4.mainloop()
    
def afficher_predictions(full_name, Opp, Opp_player,game_start,domicile,month,
                         minutes):
    root5= tk.Tk()
    root5.iconbitmap('config/icone.ico')
    root5.title("Prédictions statistiques")
    
    try:
        
        cluster = pd.read_csv("data/cluster.csv", sep=";")
        MLP = load('models/MLP_FGA_pred.joblib')
        Points = load('models/Ridge_PTS.joblib')
        Rebounds = load('models/Lin_trb.joblib')
        Assists=load('models/Lin_ast.joblib')
    
        df1=df.copy()
        df1=df1.loc[df1['full_name']==full_name]
        df1 = df1.loc[df['Opp']==Opp]
        df1 = df1.drop_duplicates(['annee', 'count'],keep= 'last')
        df1=df1.nlargest(1, columns=['annee'])
    
        if df1.empty :
            df1=df.copy()
            df1=df1.loc[df1['full_name']==full_name]
            df1['Opp']=str(Opp)
            df1 = df1.drop_duplicates(['annee', 'count'],keep= 'last')
            df1=df1.nlargest(1, columns=['annee'])   
        else :
            pass
    
        team_df = cluster.loc[cluster['Key']==Opp]
        team_df=team_df.nlargest(1, columns=['annee'])
        coach_df = cluster.loc[cluster['Key']==Opp]
        coach_df=coach_df.nlargest(1, columns=['annee'])
        player_df = cluster.loc[cluster['Key']==Opp_player]
        player_df=player_df.nlargest(1, columns=['annee'])
            
        df1['cluster_team']=team_df[['cluster']].values
        if df1['cluster_coach'].empty :
            df1['cluster_coach']=coach_df[['cluster']].values
        else :
            pass
        df1['cluster_player']=player_df[['cluster']].values
        
        df1['month']=month
        df1['minutes']=minutes
        df1['GS']=game_start
        df1['Domicile']=domicile
        
        PTS = df1[['full_name',
                'Tm',
                'GS','minutes',
                'Domicile',
                'month',
                'cluster_coach',
                'cluster_player',
                'age',
                'FGA_moy','TOV_moy','PF_moy','DRtg',
                'Prod_mean_opp'
                ]]
        
        TRB = df1[['full_name',
                'Tm',
                'GS',
                'Domicile',
                'month',
                'cluster_coach',
                'cluster_player',
                'age',
                'minutes',
                'FGA','TOV','PF','DRtg',
                'Prod_mean_opp'
                ]]
        
        AST = df1[['full_name',
                'Tm',
                'GS',
                'Domicile',
                'month',
                'cluster_coach',
                'cluster_player',
                'age',
                'minutes',
                'FGA','TOV','PF','DRtg',
                'Prod_mean_opp'
                ]]
        
        FGA = df1[['full_name',
                'GS',
                'minutes',
                'count'
                ]]
        
        df1['FGA_pred'] = MLP.predict(FGA)
        df1['AST_pred'] = Assists.predict(AST)
        df1['AST_pred'] = np.exp(df1['AST_pred'])
        df1['TRB_pred'] = Rebounds.predict(TRB)
        df1['TRB_pred'] = np.exp(df1['TRB_pred'])
        df1['PTS_pred'] = Points.predict(PTS)
        df1['PTS_pred'] = np.exp(df1['PTS_pred'])
        
        pred_point = df1['PTS_pred'].values
        pred_point = pred_point.round(2)
        predp = str(*pred_point)
        
        pred_fga = df1['FGA_pred'].values
        pred_fga = pred_fga.round(2)
        predf = str(*pred_fga)
        
        pred_ast = df1['AST_pred'].values
        pred_ast = pred_ast.round(2)
        preda = str(*pred_ast)
        
        pred_reb = df1['TRB_pred'].values
        pred_reb = pred_reb.round(2)
        predr = str(*pred_reb)
        
        text = tk.Label(root5, text="Predictions for "+str(full_name)+" against "+str(Opp)+" and "+str(Opp_player))
        text.grid(row=0, column=0)
        text_1 = tk.Label(root5, text='Points prediction')
        text_1.grid(row = 1, column = 0)
        aff_pred = tk.Label(root5, text=(predp))
        aff_pred.grid(row = 2, column = 0)
        
        text_2 = tk.Label(root5, text='Field goal attempts prediction')
        text_2.grid(row = 3, column = 0)
        aff_predf = tk.Label(root5, text=str(predf))
        aff_predf.grid(row = 4, column = 0)
        
        text_3 = tk.Label(root5, text='Assists prediction')
        text_3.grid(row = 5, column = 0)
        aff_preda = tk.Label(root5, text=str(preda))
        aff_preda.grid(row = 6, column = 0)
        
        text_4 = tk.Label(root5, text='Rebonds prediction')
        text_4.grid(row = 7, column = 0)
        aff_predr = tk.Label(root5, text=str(predr))
        aff_predr.grid(row = 8, column = 0)
    except ValueError:
        label = tk.Label(root5, text= "La saisie effectuée est incomplète",
                         relief ="groove")
        label.pack()
    except Exception: 
        label = tk.Label(root5, text= "La saisie effectuée est incorrecte",
                         relief ="groove")
        label.pack()
    
    root5.mainloop()

def absence(data,player_list):
    for player in player_list:
        data = data.drop(data.loc[data['full_name']==player].index)
    return(data)
    
def afficher_team(donnees):
    tableau = tk.Tk()
    tableau.iconbitmap('config/icone.ico')
    tableau.title("Roster")
    
    frame = tk.Frame(tableau)
    frame.pack()
    
    pt = Table(frame,dataframe = donnees)
    pt.show()
    
    tableau.mainloop()
    
def create_df(data,month):
    data["Opp_code"]=data['POS'].map(str) + data['Opp'].map(str) + data['GS'].map(str)
    
    liste_code = data['Opp_code']
    Opp=(data['Opp'])
    Opp=pd.DataFrame(Opp)
    Opp=Opp.drop_duplicates(["Opp"])
    Opp=str(*Opp["Opp"])
    
    codes=[]
    for code in liste_code:
        df_code=proj_game.loc[proj_game['code']==code]
        df_code=df_code.drop_duplicates(['code'])
        codes.append(df_code)
    X = pd.concat(codes)
    X = X[["code","cluster_def"]]
    X= X.rename(columns={"code":"Opp_code","cluster_def":"cluster_player"})
    Y = proj_game.loc[proj_game['Tm']==Opp]
    Y=Y[["Tm","cluster_c"]]
    Y = Y.drop_duplicates(["cluster_c"])
    Y = Y.rename(columns={"Tm":"Opp","cluster_c":"cluster_coach"})

    data=pd.merge(data,X,on="Opp_code",how="left")
    data=pd.merge(data,Y,on="Opp",how="left")
    data = data.drop_duplicates(['full_name','Tm'],keep= 'last')
    data['cluster_player']=data['cluster_player'].fillna(0)
    
    data['month']=month
    data['bonus_malus']=0
    data['absence']=0
    return(data)
    
def simulation_match(data):

    model=load("models/Ridge_PTS_simu.joblib")
    
    data['bonus_malus']=np.random.normal(1, 5.2, len(data))
    data['minutes_var']=np.random.normal(0,3,len(data))
    data['minutes']=data['minutes']+data['minutes_var']
    
    data['score']=model.predict(data)
    data['ptspred']=np.exp(data['score'])
    data['pts_pred']=data['ptspred']+data['bonus_malus']
    data["score_tot"]=sum(data["pts_pred"])
    data["score_fin"]=(data['score_tot']/sum(data["minutes"]))*240
    return(data)


def modif_roster(equipe,Opp,month):

    fenet = tk.Tk()
    fenet.geometry('450x300')
    fenet.iconbitmap('config/icone.ico')
    fenet.title("Selection des absents")
    
    txt1=tk.Label(fenet,text="Choisir les joueurs absents")

    lbox=tk.Listbox(fenet,selectmode="multiple")
    lbox.delete('0', 'end')
    
    scrollbar = tk.Scrollbar(fenet)
    scrollbar.grid(column=3,row=1)
    
    lbox.config(yscrollcommand = scrollbar.set, width=50)
    scrollbar.config(command = lbox.yview)
    
    progress_simul=ttk.Progressbar(fenet,orient="horizontal",length=100,mode='determinate')
    
    def simulation(df_team,df_Opp, month, player_list):
        
        finish=tk.Tk()
        finish.geometry('500x75')
        finish.iconbitmap('config/icone.ico')
        finish.title("Pourcentage de victoire")
        
        score=tk.Label(finish,text="")
        
        df_team=df_team
        df_Opp=df_Opp
        month=month
        player_list=player_list
        
        def game(df_team,df_Opp,month):
            bilan=pd.DataFrame(columns={"Team","Opp","Victoire","Défaite","score_team",
                     "score_opp"})
            
            try:
                month=month
                
                df_team=absence(df_team,player_list)
                df_Opp=absence(df_Opp,player_list)
                df_team=simulation_match(df_team)
                df_Opp=simulation_match(df_Opp) 
                    
                score_t = df_team.drop_duplicates(['score_fin'],keep="last")
                score_O = df_Opp.drop_duplicates(['score_fin'],keep="last")
                
                ind_team=indice.loc[indice["Tm"]==equipe]
                ind_opp=indice.loc[indice["Tm"]==Opp]
           
                score_team=float(score_t['score_fin'])*float(ind_team['indice'])
                score_Opp=float(score_O['score_fin'])*float(ind_opp['indice'])
                
                if score_team>score_Opp:
                    Victoire=1
                    Defaite=0
                else:
                    Defaite=1
                    Victoire=0
                bilan=bilan.append({"Team":equipe,"Opp":Opp,"score_team":score_team,
                                    "score_opp":score_Opp,"Victoire":Victoire,"Défaite":Defaite},ignore_index=True)
                return(bilan)
    
            except:
                    pass
        final=[]
        
        for i in range (100):
            progress_simul['value']+=1
            bilan=game(df_team,df_Opp,month)  
            final.append(bilan)
            finish.update_idletasks()
            
        df_fin=pd.concat(final)
        df_fin['victoire']=df_fin.Victoire.astype(float)
        mean= df_fin.groupby(df_fin['Team']).sum().reset_index()
        loss = 100-mean['victoire']
        
        score.config(text="Pour 100 simulations"+"\n"+
                     "Nombre de victoires de "+str(equipe)+" "+ str(*mean['victoire'].values)+"\n"+
                     "Nombre de victoires de "+str(Opp)+" "+str(*loss))
        
        score.pack()
        finish.mainloop()
                
    month=month
    
    equipe=equipe
    
    Opp=Opp
    
    df_team=proj_game.loc[(proj_game['Tm']==equipe)]
    df_team['Opp']=str(Opp)
    df_team=create_df(df_team,month)
    
    df_Opp=proj_game.loc[(proj_game['Tm']==Opp)]
    df_Opp['Opp']=str(equipe)
    df_Opp=create_df(df_Opp,month)
 
    frames = [df_team, df_Opp,]

    result = pd.concat(frames)
    
    nom = result['full_name']    
    
    for x in nom:
            lbox.insert("end",x)
    
    player_list=[]
    for i in lbox.curselection():
        result = lbox.get(i)
        player_list.append(result)
        return(player_list)
    
    bpred=tk.Button(fenet,text="Lancer la prediction", command=lambda:[simulation(df_team,df_Opp,month,player_list)])
    
    txt1.grid(column=0,row=0)
    lbox.grid(column=0,row=1)
    bpred.grid(column=0,row=2)
    progress_simul.grid(column=0,row=3)
    
    
    fenet.mainloop()
    