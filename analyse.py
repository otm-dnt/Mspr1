# On importe la bibliothèque pandas, qui permet de manipuler les données tabulaires
import pandas as pd

# On importe le module 'os' pour accéder aux fichiers et dossiers du système
import os

# On définit le chemin vers le dossier où tu as placé tes fichiers de données CSV
data_dir = "data"  # dossier 'data' situé dans le dossier de ton projet

# On parcourt tous les fichiers dans le dossier 'data'
for fichier in os.listdir(data_dir):
    # On vérifie que le fichier se termine bien par .csv (juste les fichiers CSV)
    if fichier.endswith(".csv"):
        # On affiche un titre pour ce fichier
        print(f"\n--- {fichier} ---")

        # On lit le fichier CSV avec pandas et on le stocke dans une variable 'df' (dataframe)
        df = pd.read_csv(os.path.join(data_dir, fichier))

        # On affiche les 5 premières lignes du fichier pour avoir un aperçu rapide du contenu
        print(df.head())

        # On affiche des infos techniques : noms de colonnes, type de données, valeurs manquantes, etc.
        print(df.info())

        # On affiche des statistiques générales sur les colonnes numériques (moyenne, min, max…)
        print(df.describe())