# 📁 etl/etl_monkey.py

import pandas as pd
import psycopg2

# ----------------------------
# 1. Connexion à PostgreSQL
# ----------------------------
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

# ----------------------------
# 2. Lecture du fichier CSV
# ----------------------------
try:
    df = pd.read_csv("data/owid-monkeypox-data.csv")
    print("📄 Fichier Monkeypox chargé avec succès.")
except Exception as e:
    print("❌ Erreur chargement CSV :", e)
    exit()

# ----------------------------
# 3. Sélection des colonnes utiles
# ----------------------------
colonnes_utiles = [
    'date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
    'new_cases_smoothed', 'new_cases_smoothed_per_million'
]
df = df[colonnes_utiles].copy()

# ----------------------------
# 4. Nettoyage des données
# ----------------------------

# 4.1 Supprimer les doublons exacts
df.drop_duplicates(inplace=True)

# 4.2 Supprimer les lignes avec champs critiques manquants
df.dropna(subset=['date', 'location', 'total_cases'], inplace=True)

# 4.3 Supprimer les continents comme "World", "Africa", etc.
continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'World']
df = df[~df['location'].isin(continents)]

# 4.4 Nettoyer les noms de pays (ex: "  france " → "France")
df['location'] = df['location'].str.strip().str.title()

# 4.5 Supprimer les lignes où toutes les stats sont nulles
df = df[~(
    (df['total_cases'].isna() | (df['total_cases'] == 0)) &
    (df['new_cases'].isna() | (df['new_cases'] == 0)) &
    (df['total_deaths'].isna() | (df['total_deaths'] == 0)) &
    (df['new_deaths'].isna() | (df['new_deaths'] == 0))
)]

print(f"✅ Données nettoyées. {len(df)} lignes prêtes à être insérées.")

# ----------------------------
# 5. Insertion dans la base
# ----------------------------

try:
    curseur = connexion.cursor()

    # 5.1 Insérer la maladie Monkeypox (si pas déjà là)
    curseur.execute("""
        INSERT INTO MALADIE (nom_maladie)
        VALUES (%s)
        ON CONFLICT (nom_maladie) DO NOTHING;
    """, ('Monkeypox',))

    # 5.2 Récupérer l'id de la maladie Monkeypox
    curseur.execute("SELECT id_maladie FROM MALADIE WHERE nom_maladie = 'Monkeypox';")
    id_maladie = curseur.fetchone()[0]

    # 5.3 Insérer tous les pays (si pas déjà en base)
    for pays in df['location'].unique():
        curseur.execute("""
            INSERT INTO PAYS (nom_pays)
            VALUES (%s)
            ON CONFLICT (nom_pays) DO NOTHING;
        """, (pays,))

    # 5.4 Insérer les lignes de STATISTIQUE
    compteur = 0
    for index, ligne in df.iterrows():
        pays = ligne['location']

        # Vérifie si le pays est bien en base
        curseur.execute("SELECT id_pays FROM PAYS WHERE nom_pays = %s;", (pays,))
        result = curseur.fetchone()
        if not result:
            print(f"⚠️ Pays introuvable en base : {pays}")
            continue

        id_pays = result[0]

        try:
            curseur.execute("""
                INSERT INTO STATISTIQUE (
                    date, id_pays, id_maladie,
                    cas_totaux, nouveaux_cas, décès_totaux, nouveaux_décès,
                    nouveaux_cas_lisses, nouveaux_cas_lisses_par_million
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                ligne['date'],
                id_pays,
                id_maladie,
                ligne['total_cases'],
                ligne['new_cases'],
                ligne['total_deaths'],
                ligne['new_deaths'],
                ligne['new_cases_smoothed'],
                ligne['new_cases_smoothed_per_million']
            ))
            compteur += 1
        except Exception as e:
            print(f"❌ Erreur ligne {index} : {e}")
            continue

    connexion.commit()
    print(f"✅ {compteur} lignes insérées dans la table STATISTIQUE.")

except Exception as e:
    print("❌ Erreur globale d'insertion :", e)
    connexion.rollback()

finally:
    curseur.close()
    connexion.close()
    print("🔒 Connexion fermée.")
