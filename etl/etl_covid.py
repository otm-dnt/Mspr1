# 📁 etl/etl_covid.py

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
    print("✅ Connexion à PostgreSQL réussie.")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# ----------------------------
# 2. Lecture du fichier CSV
# ----------------------------
try:
    df = pd.read_csv("data/worldometer_coronavirus_daily_data.csv")
    print("📄 Fichier COVID chargé avec succès.")
except Exception as e:
    print("❌ Erreur chargement CSV :", e)
    exit()

# ----------------------------
# 3. Nettoyage des données
# ----------------------------

# 🔹 Colonnes utiles uniquement
colonnes = ['date', 'country', 'cumulative_total_cases', 'daily_new_cases',
            'active_cases', 'cumulative_total_deaths', 'daily_new_deaths']
df = df[colonnes].copy()

# 🔹 Renomme les colonnes pour correspondre au MPD
df.columns = ['date', 'nom_pays', 'cas_totaux', 'nouveaux_cas',
              'cas_actifs', 'décès_totaux', 'nouveaux_décès']

# ✅ Supprimer les doublons
df.drop_duplicates(inplace=True)

# ✅ Supprimer les lignes incomplètes (date, pays, cas)
df.dropna(subset=['date', 'nom_pays', 'cas_totaux'], inplace=True)

# ✅ Supprimer les continents ou régions invalides
continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'World']
df = df[~df['nom_pays'].isin(continents)]

# ✅ Nettoyer les noms de pays
df['nom_pays'] = df['nom_pays'].str.strip().str.title()

# ✅ Supprimer les lignes où toutes les statistiques sont nulles ou 0
df = df[~(
    (df['cas_totaux'].isna() | (df['cas_totaux'] == 0)) &
    (df['nouveaux_cas'].isna() | (df['nouveaux_cas'] == 0)) &
    (df['cas_actifs'].isna() | (df['cas_actifs'] == 0)) &
    (df['décès_totaux'].isna() | (df['décès_totaux'] == 0)) &
    (df['nouveaux_décès'].isna() | (df['nouveaux_décès'] == 0))
)]

# ✅ Résumé nettoyage
print(f"✅ Données prêtes : {len(df)} lignes nettoyées.")
print(df.head())

# ----------------------------
# 4. Insertion dans PostgreSQL
# ----------------------------

try:
    curseur = connexion.cursor()

    # 🔹 Insertion des pays
    for pays in df['nom_pays'].unique():
        curseur.execute("""
            INSERT INTO PAYS (nom_pays)
            VALUES (%s)
            ON CONFLICT (nom_pays) DO NOTHING;
        """, (pays,))
    print("✅ Insertion des pays terminée.")

    # 🔹 Insertion de la maladie COVID-19
    curseur.execute("""
        INSERT INTO MALADIE (nom_maladie)
        VALUES (%s)
        ON CONFLICT (nom_maladie) DO NOTHING;
    """, ('COVID-19',))
    print("✅ Maladie COVID-19 insérée.")

    # 🔹 Récupérer son ID
    curseur.execute("SELECT id_maladie FROM MALADIE WHERE nom_maladie = 'COVID-19';")
    id_maladie = curseur.fetchone()[0]

    lignes_insérées = 0

    # 🔹 Insertion des statistiques
    for index, ligne in df.iterrows():
        try:
            curseur.execute("SELECT id_pays FROM PAYS WHERE nom_pays = %s;", (ligne['nom_pays'],))
            resultat = curseur.fetchone()
            if not resultat:
                continue
            id_pays = resultat[0]

            curseur.execute("""
                INSERT INTO STATISTIQUE (
                    date, id_pays, id_maladie,
                    cas_totaux, nouveaux_cas, décès_totaux, nouveaux_décès, cas_actifs
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                ligne['date'],
                id_pays,
                id_maladie,
                ligne['cas_totaux'],
                ligne['nouveaux_cas'],
                ligne['décès_totaux'],
                ligne['nouveaux_décès'],
                ligne['cas_actifs']
            ))

            lignes_insérées += 1

        except Exception as e:
            print(f"⚠️ Erreur ligne {index}: {e}")
            connexion.rollback()
            continue

    connexion.commit()
    print(f"✅ Insertion terminée. {lignes_insérées} lignes ajoutées.")

except Exception as e:
    print("❌ Erreur globale d'insertion :", e)
    connexion.rollback()

finally:
    curseur.close()
    connexion.close()
    print("🔒 Connexion fermée proprement.")
