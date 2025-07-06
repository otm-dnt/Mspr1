# etl/verifier_qualite_donnees.py

import pandas as pd

# ------------------------
# 1. Lire les fichiers CSV
# ------------------------

# ⚠️ Remplace ces chemins si nécessaire
chemin_monkeypox = "data/owid-monkeypox-data.csv"
chemin_covid = "data/worldometer_coronavirus_daily_data.csv"

# ------------------------
# 2. Vérification Monkeypox
# ------------------------

print("🦠 Vérification des données Monkeypox :")
df_monkey = pd.read_csv(chemin_monkeypox)
print(f"📦 Lignes AVANT nettoyage : {len(df_monkey)}")

# Sélection des colonnes utiles (mêmes que dans etl_monkey.py)
colonnes_utiles = [
    'date', 'location', 'total_cases', 'new_cases', 'total_deaths',
    'new_deaths', 'new_cases_smoothed', 'new_cases_smoothed_per_million'
]
df_monkey = df_monkey[colonnes_utiles].copy()

# Suppression des lignes nulles sur les colonnes critiques
df_monkey_clean = df_monkey.dropna(subset=['date', 'location', 'total_cases'])

# Suppression des doublons
df_monkey_clean = df_monkey_clean.drop_duplicates()

# Normalisation des pays
df_monkey_clean['location'] = df_monkey_clean['location'].str.strip().str.title()

# Filtrage continents
continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'World']
df_monkey_clean = df_monkey_clean[~df_monkey_clean['location'].isin(continents)]

print(f"✅ Lignes APRÈS nettoyage : {len(df_monkey_clean)}")
print("❌ Lignes supprimées (Nettoyage) :", len(df_monkey) - len(df_monkey_clean))
print()

# ------------------------
# 3. Vérification COVID
# ------------------------

print("🦠 Vérification des données COVID-19 :")
df_covid = pd.read_csv(chemin_covid)
print(f"📦 Lignes AVANT nettoyage : {len(df_covid)}")

# Colonnes utiles (comme dans etl_covid.py)
colonnes_utiles_covid = [
    'date', 'country', 'cumulative_total_cases', 'daily_new_cases',
    'active_cases', 'cumulative_total_deaths', 'daily_new_deaths'
]
df_covid = df_covid[colonnes_utiles_covid].copy()

# Filtrage continents
df_covid = df_covid[~df_covid['country'].isin(continents)]

# Nettoyage
df_covid_clean = df_covid.dropna(subset=['date', 'country', 'cumulative_total_cases'])
df_covid_clean['country'] = df_covid_clean['country'].str.strip().str.title()
df_covid_clean = df_covid_clean.drop_duplicates()

print(f"✅ Lignes APRÈS nettoyage : {len(df_covid_clean)}")
print("❌ Lignes supprimées (Nettoyage) :", len(df_covid) - len(df_covid_clean))
