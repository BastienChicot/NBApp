# NBApp
Application pour projections NBA
Repertoire Old

Ce répertoire comprends l'intégralité des anciennes versions et des anciens codes utilisés pour créer l'application en python

Repertoire prévisions saison

Ce répertoire comprends des codes et des bases permettant de simuler des matchs et/ou des saisons NBA complètes grâce à un modèle de prédiction des points créé avec sklearn. 
Le programme simulation_test dans code_config est celui qui permet de lancer une simulation. Les réglages se situent après les fonctions avec une boucle pour simuler les saisons
et les lignes nécessaires pour simuler des matchs à l'unité.
La mise à jour des data se fait grâce aux fichiers .py situés dans bases_config. Le dossier scoring team permet de traiter des datas par équipes pour introduire des notions d'entente
d'équipe dans les simulations.
Les calendriers par équipes sont enregistrés dans le dossier calendriers.

Repertoire Stat joueurs

Ce dossier comprends l'ensemble des données scrapées pour la création des dataframes permettant d'entraîner les modèles de prédiction. Cependant, ceux qui sont utilisés par l'application
se situent dans le dossier version 3.0.
Ici vous pouvez trouver les statistiques depuis 2006 de l'ensemble des joueurs en activité. 

Repertoire Version 3.0
Cette application permet de récupérer toutes les données par joueur et pas match depuis basketball-reference.com. 
Elle construit un fichier exploitable pour faire du machine-learning et entraîne des modèles.
Le dossier config comprends les codes de fonctions utilisées par l'application.
Le dossier data comprends les bases utiles pour l'application.
Le dossier models comprends les modèles de machine-learning.

Pour faire fonctionner l'application depuis ce dossier, il suffit de lancer le script App_V3.0 sur un interprêteur Python.
