# ---------------------------------------------
# 📁 prediction/2_features_engineering.py
# ---------------------------------------------
# 📌 Objectif : transformer les données brutes
# en variables (features) adaptées au Machine Learning
#
# On va calculer :
# - taux_transmission (nouveaux cas / population)
# - décalages temporels (lag)
# - moyennes mobiles
#
# Résultat : un CSV prêt pour l'entraînement
# ---------------------------------------------

import pandas as pd

# ---------------------------------------------
# 1️⃣ Charger les données nettoyées
# ---------------------------------------------
# 👉 On récupère le CSV généré par 1_collecte.py
df = pd.read_csv("clean_data.csv", parse_dates=['date'])
print("✅ Données chargées :")
print(df.head())

# ---------------------------------------------
# 2️⃣ Calculer le taux de transmission
# ---------------------------------------------
# 👉 nouveaux cas / population
# ✅ Normalisation pour comparer les pays
df['taux_transmission'] = df['nouveaux_cas'] / df['population']

# ✅ Exemple :
# - 500 cas sur 60 millions ≠ 500 cas sur 1 million
# - Le taux permet au modèle de raisonner proportionnellement

# ---------------------------------------------
# 3️⃣ Créer des variables lag (retard)
# ---------------------------------------------
# 👉 Pour que le modèle "se souvienne" du passé
df = df.sort_values(['nom_pays', 'date'])

# ✅ Lag sur 1 jour
df['nouveaux_cas_j-1'] = df.groupby('nom_pays')['nouveaux_cas'].shift(1)
df['taux_transmission_j-1'] = df.groupby('nom_pays')['taux_transmission'].shift(1)

# ✅ Explication :
# - Ces colonnes disent au modèle la situation la veille.
# - C'est très utile pour prévoir la suite de l'épidémie.

# ---------------------------------------------
# 4️⃣ Créer des moyennes mobiles (exemple sur 7 jours)
# ---------------------------------------------
# 👉 Pour lisser les fluctuations quotidiennes
df['moyenne_7j_nouveaux_cas'] = df.groupby('nom_pays')['nouveaux_cas'].transform(lambda x: x.rolling(7).mean())
df['moyenne_7j_taux'] = df.groupby('nom_pays')['taux_transmission'].transform(lambda x: x.rolling(7).mean())

# ✅ Explication :
# - Les données brutes sont très bruyantes (exemple : gros pic un jour).
# - La moyenne mobile aide le modèle à capter la tendance générale.

# ---------------------------------------------
# 5️⃣ Nettoyer : supprimer les lignes avec NaN
# ---------------------------------------------
# 👉 Les lags et les rolling créent des valeurs manquantes
df = df.dropna()

# ✅ Pourquoi ?
# - Après shift ou rolling, les premières lignes n'ont pas assez d'historique.
# - Il faut les retirer pour éviter des erreurs à l'entraînement.

# ---------------------------------------------
# 6️⃣ Aperçu final
# ---------------------------------------------
print("\n✅ Données finales prêtes pour le ML :")
print(df.head())
print(df.info())

# ---------------------------------------------
# 7️⃣ Sauvegarder le jeu de données préparé
# ---------------------------------------------
# ✅ ATTENTION : chemin corrigé pour que le CSV soit dans prediction/
df.to_csv("features_data.csv", index=False)
print("\n✅ Fichier features_data.csv créé avec succès ✅")
