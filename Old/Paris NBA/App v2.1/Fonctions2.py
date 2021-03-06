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

full_name="Damian Lillard"
code="lillada"
annee='2021'
Opp = "LAL"
player_team="POR"
Opp_player="Dennis Schroder"

df=pd.read_csv("data/data_ML.csv", sep=";")

def prp_en_carriere(full_name):
    data = pd.read_csv("data/evo_carriere.csv", sep =";")
    players_base = pd.read_csv('nba_players.csv', sep=";")

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
    url = 'https://www.basketball-reference.com/players/a/'+str(code)+'01/gamelog/'+str(annee)
    
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
            
    if annee<'2022' :
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
    
    url3 = 'https://www.basketball-reference.com/players/a/'+str(code)+'01/splits/'
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
    root3.geometry('1250x600')
    canvas2 = tk.Canvas(root3)
    
    scrollbar=tk.Scrollbar(canvas2,orient="vertical",command=canvas2.yview)
    scrollbarix=tk.Scrollbar(canvas2,orient="horizontal",command=canvas2.xview)
    
    #Création des cadres
    cadre = tk.LabelFrame(canvas2, text="Stat contre " + str(Opp))
    cadre.grid(row=0,column=0)
    cadre2 = tk.LabelFrame(canvas2, text="Stat contre les joueurs de " + str(Opp))
    cadre2.grid(row=0,column=0)
    
    canvas2.create_window(0,250,window=cadre, anchor='w')
    canvas2.create_window(0,550,window=cadre2, anchor='w')

    A = A.loc[(A["full_name"] == full_name) & (A["Opp"] == Opp)]
    A = A[['Opp',"Opp_name","Opp_Coach","minutes","Domicile","PTS","AST","TRB","FGA",'annee','PTS_diff','AST_diff','TRB_diff']]
    
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
    scrollbarix.pack(fill='both', side="right")
    
    root3.mainloop()

def stat_teams (player_team,Opp):
    root4 = tk.Tk()
    root4.geometry('1750x200')
    
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

    team_code=pd.read_csv('code_team.csv', sep=';')
    
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
    
def afficher_predictions(full_name, Opp, Opp_player):

    root5= tk.Tk()
    
    df = pd.read_csv('data.csv', sep=";")
    coach_df = pd.read_csv("coach_cluster.csv",sep=";")
    player_df = pd.read_csv("player_cluster.csv",sep=";")
    team_df = pd.read_csv("team_cluster.csv",sep=";")
    MLP = load('MLP_FGA_pred.joblib')
    SGD = load('SGD_PTS_pred.joblib')
    Lin_ridge = load('Ridge_TRB_pred.joblib')
    Lin_Reg=load('Reg_AST_pred.joblib')

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

    team_df = team_df.loc[team_df['Opp']==Opp]
    team_df=team_df.nlargest(1, columns=['annee'])
    coach_df = coach_df.loc[coach_df['Opp']==Opp]
    coach_df=coach_df.nlargest(1, columns=['annee'])
    player_df = player_df.loc[player_df['Opp_name']==Opp_player]
    player_df=player_df.nlargest(1, columns=['annee'])
        
    df1['cluster_team']=team_df[['cluster_team']].values
    df1['cluster_coach']=coach_df[['cluster_coach']].values
    df1['cluster_player']=player_df[['cluster_player']].values
    
    PTS = df1[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'cluster_team',
            'age',
            'minutes',
            'FGA','TOV','PF','annee'
            ]]
    
    TRB = df1[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_team',
            'cluster_player',
            'age',
            'minutes',
            'FGA','TOV_moy','PF','annee'
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
            'FGA','TOV_moy','PF','annee'
            ]]
    
    FGA = df1[['full_name',
            'GS',
            'minutes',
            'count'
            ]]
    
    df1['FGA_pred'] = MLP.predict(FGA)
    df1['AST_pred'] = Lin_Reg.predict(AST)
    df1['TRB_pred'] = Lin_ridge.predict(TRB)
    df1['PTS_pred'] = SGD.predict(PTS)
    
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
    
    root5.mainloop()