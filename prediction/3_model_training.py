# ---------------------------------------------
# 📁 prediction/3_model_training.py
# 👉 Objectif : entraîner un modèle de Machine Learning
# pour prédire le taux de transmission
# ---------------------------------------------

# ---------------------------------------------
# 📌 1️⃣ Importer les bibliothèques
# ---------------------------------------------
import pandas as pd
# ✅ pandas : pour charger et manipuler les données tabulaires (DataFrame)

from sklearn.model_selection import train_test_split
# ✅ train_test_split : pour diviser le jeu de données en partie entraînement et test

from sklearn.linear_model import LinearRegression
# ✅ LinearRegression : le modèle de régression linéaire de scikit-learn

from sklearn.metrics import r2_score, mean_squared_error
# ✅ r2_score : mesure la qualité de la régression (1 = parfait)
# ✅ mean_squared_error : permet de calculer l'erreur moyenne au carré

import numpy as np
# ✅ numpy : pour les calculs numériques, notamment racine carrée

import joblib
# ✅ joblib : pour sauvegarder et recharger le modèle entraîné facilement

# ---------------------------------------------
# 📌 2️⃣ Charger les données préparées
# 👉 issues de 2_features_engineering.py
# ---------------------------------------------
df = pd.read_csv("features_data.csv")
print("✅ Données chargées :")
print(df.head())

# ---------------------------------------------
# 📌 3️⃣ Définir la cible (y) et les variables explicatives (X)
# ---------------------------------------------
# 🎯 y = ce qu'on veut prédire : le taux de transmission
y = df['taux_transmission']

# 🎯 X = les variables utilisées pour prédire y
# On enlève ce qui n'aide pas à la prédiction directe
X = df.drop(columns=['date', 'nom_pays', 'taux_transmission'])

print("\n✅ Features utilisées pour l'entraînement :")
print(X.columns)

# ---------------------------------------------
# 📌 4️⃣ Diviser le dataset en entraînement et test
# ---------------------------------------------
# 👉 Pour vérifier si le modèle est capable de généraliser
# - 80% pour entraîner
# - 20% pour tester
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n✅ Jeu d'entraînement : {X_train.shape}")
print(f"✅ Jeu de test : {X_test.shape}")

# ---------------------------------------------
# 📌 5️⃣ Créer et entraîner le modèle
# ---------------------------------------------
# ✅ On choisit la régression linéaire car c'est simple et interprétable
model = LinearRegression()
model.fit(X_train, y_train)

print("\n✅ Modèle entraîné avec succès.")

# ---------------------------------------------
# 📌 6️⃣ Faire des prédictions sur le test
# ---------------------------------------------
# ✅ On vérifie ce que prédit le modèle sur des données jamais vues
y_pred = model.predict(X_test)

# ---------------------------------------------
# 📌 7️⃣ Évaluer la qualité du modèle
# ---------------------------------------------
# ✅ Score R² : 1 = prédictions parfaites
r2 = r2_score(y_test, y_pred)

# ✅ RMSE : racine de l'erreur quadratique moyenne
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n✅ Évaluation du modèle :")
print(f"R² (score de détermination) : {r2:.3f}")
print(f"RMSE (Root Mean Squared Error) : {rmse:.6f}")

# ---------------------------------------------
# ✅ Explication des métriques
# - R² mesure la proportion de variance expliquée par le modèle
#   (1 = parfait, 0 = modèle nul)
# - RMSE donne une idée de l'erreur moyenne en unités du taux de transmission
# ---------------------------------------------

# ---------------------------------------------
# 📌 8️⃣ Sauvegarder le modèle entraîné
# ---------------------------------------------
# ✅ On sauvegarde le modèle pour pouvoir le réutiliser plus tard
joblib.dump(model, "model_taux_transmission.pkl")
print("\n✅ Modèle sauvegardé sous prediction/model_taux_transmission.pkl ✅")
