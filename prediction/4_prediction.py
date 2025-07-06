# ---------------------------------------------
# 📁 prediction/4_prediction.py
# 👉 Objectif : utiliser le modèle entraîné
# pour prédire le taux de transmission sur des données
# ---------------------------------------------

# 📌 1️⃣ Importer les bibliothèques
import pandas as pd
# ✅ pandas : manipulation des DataFrames

import joblib
# ✅ joblib : pour charger le modèle entraîné

# ---------------------------------------------
# 📌 2️⃣ Charger les données à prédire
# ---------------------------------------------
# 👉 On utilise ici features_data.csv car il est déjà formaté
# exactement comme attendu par le modèle.
try:
    df = pd.read_csv("features_data.csv")
    print("✅ Données chargées pour prédiction :")
    print(df.head())
except Exception as e:
    print(f"❌ Erreur lors du chargement des données : {e}")
    exit()

# ---------------------------------------------
# 📌 3️⃣ Charger le modèle sauvegardé
# ---------------------------------------------
try:
    model = joblib.load("model_taux_transmission.pkl")
    print("✅ Modèle chargé avec succès.")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    exit()

# ---------------------------------------------
# 📌 4️⃣ Préparer les features pour prédiction
# ---------------------------------------------
# ✅ On enlève les colonnes inutiles pour la prédiction
X = df.drop(columns=['date', 'nom_pays', 'taux_transmission'])
print("\n✅ Colonnes utilisées pour prédiction :")
print(X.columns)

# ---------------------------------------------
# 📌 5️⃣ Faire les prédictions
# ---------------------------------------------
df['taux_transmission_prédit'] = model.predict(X)

# ✅ Nouvelle étape : suppression des valeurs négatives
# 👉 On s'assure qu'aucun taux de transmission prédit ne soit négatif
df['taux_transmission_prédit'] = df['taux_transmission_prédit'].clip(lower=0)

print("\n✅ Prédictions ajoutées au DataFrame (corrigées) :")
print(df[['date', 'nom_pays', 'taux_transmission_prédit']].head())

# ---------------------------------------------
# 📌 6️⃣ Sauvegarder le résultat dans un fichier CSV
# ---------------------------------------------
try:
    df.to_csv("predictions_resultats.csv", index=False)
    print("\n✅ Fichier predictions_resultats.csv créé avec succès ✅")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde du fichier : {e}")
