# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:21:32 2021

@author: basti
"""
import tkinter as tk
from config.Fonctions import prp_en_carriere, stat_20matchs_splits, stat_Opp_team, stat_teams,afficher_predictions
from config.Fonctions import modif_roster, create_df, afficher_team
from config.Entrainement_modèles import train_model_pts, train_model_ast,train_model_trb,train_model_fga
from config.maj_data_fun import miseajour
import pandas as pd
import numpy as np
from tkinter import ttk
import datetime
import os
import time

players_base = pd.read_csv('data/nba_players.csv', sep=";")

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")

liste_equipe=['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET',
       'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
       'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
       'TOR', 'UTA', 'WAS']
mois=list(range(1,13))

root = tk.Tk()
root.iconbitmap('config/icone.ico')
root.title("NBApp pour parieur avertis")

def afficher_aide():
    os.startfile("Aide.txt")

def train_models():
    window = tk.Tk()
    window.iconbitmap('config/icone.ico')
    window.title("Mettez à jour les modèles de prédictions")
    liste_models={
    train_model_pts,
    train_model_ast,
    train_model_trb,
    train_model_fga
    }
    
    pb = ttk.Progressbar(window, orient='horizontal', length = 300)
    lab = tk.Label(window, text="")
    lab2 = tk.Label(window, text="")
    
    def lancement():
        lab2.config(text="Lancement du traitement")
        for model in liste_models :
            pb['value']+=25
            lab.config(text=model)
            model()
            window.update_idletasks()
            time.sleep(0.5)
        lab2.config(text="Traitement terminé")    
    bt = tk.Button(window, text="Lancer le programme", command=lancement)
    pb.pack()
    lab.pack()
    lab2.pack()
    bt.pack()
    window.mainloop()
    
menubar = tk.Menu(root)

menu1 = tk.Menu(menubar, tearoff=0)
menu1.add_command(label="Mise à jour des données", command=miseajour)
menu1.add_command(label="Entrainer les modèles de machines learning", command=train_models)
menu1.add_command(label="Aide", command=afficher_aide)
menu1.add_separator()
menubar.add_cascade(label="Options", menu=menu1)

n = ttk.Notebook(root)   # Création du système d'onglets
n.pack()

#s = ttk.Style()
#s.configure('TFrame', background='#99CCFF')

o1 = ttk.Frame(n)#, style='new.TFrame')       # Ajout de l'onglet 1
o1.pack()
o2 = ttk.Frame(n)       # Ajout de l'onglet 2
o2.pack()
o3 = ttk.Frame(n)       # Ajout de l'onglet 3
o3.pack()
n.add(o1, text='Statistiques')      # Nom de l'onglet 1
n.add(o2, text='Projections')      # Nom de l'onglet 2
n.add(o3, text='Simulation de match')      # Nom de l'onglet 3
    
def afficher_prp():
    full_name=str(e11.get())
    prp_en_carriere(full_name)

def afficher_20last():
    try :
        full_name=str(e11.get())
        code_base = players_base.loc[players_base['full_name'] == full_name].values[0]
        y = code_base[2:3]
        code = ''.join(y)
        annee = '2021'
        stat_20matchs_splits(code,annee)
    except IndexError:
        label = tk.Label(root, text= "La saisie effectuée est incorrecte",
                         relief ="groove")
        label.pack() 

def afficher_stats_team():
    player_team = str(combo_equipe.get())
    Opp = str(combo_equipe2.get())
    stat_teams(player_team,Opp)

def afficher_stats_Oppteam():
    full_name=str(e11.get())
    Opp = str(combo_equipe2.get())
    stat_Opp_team(full_name,Opp)
    
l11 = tk.Label(o1, text="Saisir le nom du joueur")
e11 = tk.Entry(o1)
l21 = tk.Label(o1, text="Choisir le nom de l'équipe du joueur")
combo_equipe = ttk.Combobox(o1, values=liste_equipe)
l31 = tk.Label(o1, text="Choisir le nom de l'équipe adverse")
combo_equipe2 = ttk.Combobox(o1, values=liste_equipe)

l11.pack()
e11.pack()
l21.pack()
combo_equipe.pack()
l31.pack()
combo_equipe2.pack()

b1 = tk.Button(o1, text='Afficher les prp moyens en carrière', command=afficher_prp)
b1.pack()
b2 = tk.Button(o1, text='Afficher les statistiques sur les 20 derniers matchs et les stats splits en carrière', command=afficher_20last)
b2.pack()
b3 = tk.Button(o1, text='Afficher les ranking des équipes', command=afficher_stats_team)
b3.pack()
b4 = tk.Button(o1, text="Afficher les statistiques face à l'adversaire", command=afficher_stats_Oppteam)
b4.pack()

lbl1 = tk.Label(o1)
lbl1.pack()

def prepa_pred():
    full_name=str(e1.get())
    Opp=str(combo_equipe3.get())
    Opp_player=str(e2.get())
    game_start = int(e3.get())
    domicile = int(e4.get())
    month = int(choix_mois.get())
    minutes = int(e6.get())
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    annee=date.strftime("%Y")
    annee =int(annee)
           
    afficher_predictions(full_name, Opp, Opp_player,game_start,domicile,month,
                         minutes)
    
def show_pred(event):
    full_name=str(e1.get())
    Opp=str(combo_equipe3.get())
    Opp_player=str(e2.get())
    game_start = int(e3.get())
    domicile = int(e4.get())
    month = int(choix_mois.get())
    minutes = int(e6.get())
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    annee=date.strftime("%Y")
    annee =int(annee)
           
    afficher_predictions(full_name, Opp, Opp_player,game_start,domicile,month,
                         minutes)

l1 = tk.Label(o2, text="Saisir le nom du joueur")
e1 = tk.Entry(o2)
l15 = tk.Label(o2, text="Choisir le nom de l'équipe adverse")
combo_equipe3 = ttk.Combobox(o2, values=liste_equipe)
l2 = tk.Label(o2, text="Saisir le nom de l'adversaire direct")
e2 = tk.Entry(o2)
l3 = tk.Label(o2, text="Game starter (1 pour oui, 0 sinon)")
e3 = tk.Entry(o2)
l4 = tk.Label(o2, text="Match à domicile (1 pour oui, 0 sinon)")
e4 = tk.Entry(o2)
l5 = tk.Label(o2, text="Choisir le mois de l'annee")
choix_mois=ttk.Combobox(o2, values=mois)
l6 = tk.Label(o2, text="Nombre de minutes du joueur")
e6 = tk.Entry(o2)

l1.pack()
e1.pack()
l15.pack()
combo_equipe3.pack()
l2.pack()
e2.pack()
l3.pack()
e3.pack()
l4.pack()
e4.pack()
l5.pack()
choix_mois.pack()
l6.pack()
e6.pack()

b5 = tk.Button(o2, text='Afficher les projections', command=prepa_pred)
b5.pack()

lbl2 = tk.Label(o2)
lbl2.pack()

def creation_df_team ():
    month=int(combo_month.get())
    
    equipe=str(combo_team.get())
    
    Opp=str(combo_Opp.get())
    
    df_team=proj_game.loc[(proj_game['Tm']==equipe)]
    df_team['Opp']=Opp
    df_team=create_df(df_team,month)
    
    df_roster=df_team[['full_name',"minutes"]]
    afficher_team(df_roster)
    return(df_team)

def creation_df_Opp ():
    month=int(combo_month.get())
    
    equipe=str(combo_team.get())
    
    Opp=str(combo_Opp.get())
    
    df_Opp=proj_game.loc[(proj_game['Tm']==Opp)]
    df_Opp['Opp']=str(equipe)
    df_Opp=create_df(df_Opp,month)
    
    df_roster=df_Opp[['full_name',"minutes"]]
    afficher_team(df_roster)
    return(df_Opp)    
    
choix=list(np.unique(proj_game['Tm']))

moi=tk.Label(o3,text="Choisir le mois de la rencontre")
moi.grid(column=0,row=0)

combo_month = ttk.Combobox(o3, values=mois)
combo_month.grid(column=1,row=0)

choixtm=tk.Label(o3,text="Choisir l'équipe 1")
choixtm.grid(column=0,row=1)

combo_team = ttk.Combobox(o3, values=choix)
combo_team.grid(column=1,row=1)

choixopp=tk.Label(o3,text="Choisir l'équipe 2")
choixopp.grid(column=0,row=2)

combo_Opp = ttk.Combobox(o3, values=choix)
combo_Opp.grid(column=1,row=2)

b6 = tk.Button(o3, text="Roster équipe 1", command=creation_df_team)
b6.grid(column=0,row=3)
b7 = tk.Button(o3, text="Roster équipe 2", command=creation_df_Opp)
b7.grid(column=1,row=3)

bval = tk.Button(o3, text="Valider la selection", command=lambda:[creation_df_team, creation_df_Opp, 
                                                                  modif_roster(str(combo_team.get()),str(combo_Opp.get()),int(combo_month.get()))])
bval.grid(row=5,column=1)

root.bind('<Return>', show_pred)
root.config(menu=menubar)

root.mainloop()