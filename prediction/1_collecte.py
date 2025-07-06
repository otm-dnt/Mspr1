# ----------------------------------------
# 📁 prediction/1_collecte.py
# 👉 Objectif : collecter les données propres depuis PostgreSQL
# pour entraîner un modèle prédictif sur le taux de transmission
# ----------------------------------------

import pandas as pd
import psycopg2

# ----------------------------------------
# 1️⃣ Connexion à la base PostgreSQL
# ----------------------------------------
try:
    connexion = psycopg2.connect(
        host="localhost",
        database="pandemie_mspr",
        user="postgres",
        password="admin"
    )
    print("✅ Connexion à la base réussie.")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# ----------------------------------------
# 2️⃣ Chargement des données brutes
# ----------------------------------------
try:
    query = """
        SELECT s.date, p.nom_pays, p.population, s.nouveaux_cas
        FROM STATISTIQUE s
        JOIN PAYS p ON s.id_pays = p.id_pays
        WHERE s.id_maladie = (
            SELECT id_maladie FROM MALADIE WHERE nom_maladie = 'COVID-19'
        )
    """
    df = pd.read_sql(query, connexion)
    print("✅ Données chargées.")
except Exception as e:
    print("❌ Erreur lors du chargement des données :", e)
    connexion.close()
    exit()

# ----------------------------------------
# 3️⃣ Nettoyage des données
# ----------------------------------------

# ✅ Conversion de la colonne date
df['date'] = pd.to_datetime(df['date'])

# ✅ Suppression des valeurs manquantes
df = df.dropna(subset=['nouveaux_cas', 'population'])

# ✅ Population > 0 uniquement
df = df[df['population'] > 0]

# ✅ Supprimer les nouveaux cas négatifs
df = df[df['nouveaux_cas'] >= 0]

# ✅ Vérification
print("✅ Données prêtes pour le Machine Learning :")
print(df.head())
print(df.info())

# ----------------------------------------
# 4️⃣ Sauvegarde éventuelle en CSV pour inspection
# ----------------------------------------

# ✅ Sauvegarde directement dans le dossier actuel
df.to_csv("clean_data.csv", index=False)
print("✅ Fichier clean_data.csv généré avec succès.")


# 5️⃣ Fermeture de la connexion
# ----------------------------------------
connexion.close()
print("🔒 Connexion fermée.")
