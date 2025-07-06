# 📁 etl/enrichissement_covid.py

import pandas as pd
import psycopg2

# -------------------------------------------------
# 1. Connexion sécurisée à PostgreSQL
# -------------------------------------------------
try:
    connexion = psycopg2.connect(
        host="localhost",
        database="pandemie_mspr",
        user="postgres",
        password="admin"
    )
    print("✅ Connexion PostgreSQL réussie.")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# -------------------------------------------------
# 2. Chargement du fichier CSV résumé
# -------------------------------------------------
try:
    df = pd.read_csv("data/worldometer_coronavirus_summary_data.csv")
    print("📄 Fichier résumé chargé avec succès.")
except Exception as e:
    print("❌ Erreur chargement CSV résumé :", e)
    exit()

# -------------------------------------------------
# 3. Nettoyage du fichier résumé
# -------------------------------------------------

# On garde uniquement les colonnes pertinentes
colonnes = ['country', 'continent', 'population', 'total_recovered', 'serious_or_critical']
df = df[colonnes].copy()

# Supprimer les doublons exacts
df.drop_duplicates(inplace=True)

# Supprimer les lignes sans pays ou sans données essentielles
df.dropna(subset=['country', 'continent', 'population'], inplace=True)

# Standardiser les noms de pays
df['country'] = df['country'].str.strip().str.title()

# Supprimer les lignes qui ne concernent pas des pays (ex : continents globaux)
continents_invalides = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
df = df[~df['country'].isin(continents_invalides)]

# ✅ Résumé après nettoyage
print(f"📊 Données propres : {len(df)} lignes prêtes à l’insertion.")
print(df.head())

# -------------------------------------------------
# 4. Mise à jour de la table PAYS (continent + population)
# -------------------------------------------------
try:
    curseur = connexion.cursor()
    pays_mis_a_jour = 0

    for index, ligne in df.iterrows():
        try:
            curseur.execute("""
                UPDATE PAYS
                SET continent = %s, population = %s
                WHERE nom_pays = %s;
            """, (
                ligne['continent'],
                ligne['population'],
                ligne['country']
            ))
            pays_mis_a_jour += 1
        except Exception as e:
            print(f"⚠️ Erreur pays ligne {index}: {e}")
            continue

    connexion.commit()
    print(f"✅ Table PAYS mise à jour : {pays_mis_a_jour} pays modifiés.")

except Exception as e:
    print("❌ Erreur globale update PAYS :", e)
    connexion.rollback()

# -------------------------------------------------
# 5. Mise à jour des champs STATISTIQUE (guéris + cas graves)
# -------------------------------------------------
try:
    stats_modifiées = 0

    for index, ligne in df.iterrows():
        try:
            # Récupérer l’ID du pays
            curseur.execute("SELECT id_pays FROM PAYS WHERE nom_pays = %s;", (ligne['country'],))
            resultat = curseur.fetchone()
            if resultat is None:
                continue
            id_pays = resultat[0]

            # Récupérer l’ID de la maladie (COVID-19)
            curseur.execute("SELECT id_maladie FROM MALADIE WHERE nom_maladie = 'COVID-19';")
            id_maladie = curseur.fetchone()[0]

            # Mettre à jour les statistiques (si maladie = COVID-19)
            curseur.execute("""
                UPDATE STATISTIQUE
                SET total_guéris = %s, cas_graves = %s
                WHERE id_pays = %s AND id_maladie = %s;
            """, (
                ligne['total_recovered'],
                ligne['serious_or_critical'],
                id_pays,
                id_maladie
            ))

            stats_modifiées += 1
        except Exception as e:
            print(f"⚠️ Erreur ligne {index}: {e}")
            continue

    connexion.commit()
    print(f"✅ STATISTIQUE enrichie avec succès : {stats_modifiées} lignes modifiées.")

except Exception as e:
    print("❌ Erreur globale update STATISTIQUE :", e)
    connexion.rollback()

finally:
    curseur.close()
    connexion.close()
    print("🔒 Connexion fermée proprement.")
