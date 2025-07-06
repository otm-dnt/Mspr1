# 📁 dashboard/pages/2_evolution_temporelle.py

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# -------------------------------------
# 1. Fonction pour se connecter à la base PostgreSQL
# -------------------------------------
@st.cache_resource
def connecter_db():
    try:
        return psycopg2.connect(
            host="localhost",
            database="pandemie_mspr",
            user="postgres",
            password="admin"
        )
    except Exception as e:
        st.error(f"❌ Erreur de connexion à la base : {e}")
        return None

# -------------------------------------
# 2. Fonction pour charger les données
# -------------------------------------
@st.cache_data
def charger_donnees():
    conn = connecter_db()
    requete = """
        SELECT s.*, p.nom_pays, m.nom_maladie
        FROM STATISTIQUE s
        JOIN PAYS p ON s.id_pays = p.id_pays
        JOIN MALADIE m ON s.id_maladie = m.id_maladie
    """
    df = pd.read_sql(requete, conn)
    df['date'] = pd.to_datetime(df['date'])  # On s'assure que la colonne date est bien au bon format
    conn.close()
    return df

# -------------------------------------
# 3. Titre de la page
# -------------------------------------
st.title("📈 Évolution Temporelle des Statistiques Pandémiques")

# -------------------------------------
# 4. Chargement des données
# -------------------------------------
df = charger_donnees()

# -------------------------------------
# 5. Filtres utilisateur
# -------------------------------------
pays_disponibles = sorted(df['nom_pays'].dropna().unique())
maladies_disponibles = sorted(df['nom_maladie'].dropna().unique())

# Sélection multiple de pays
pays_selectionnes = st.multiselect("🌍 Sélectionner un ou plusieurs pays :", pays_disponibles, default=["France", "Germany"])

# Sélection d'une seule maladie
maladie_selectionnee = st.selectbox("🦠 Choisir une maladie :", maladies_disponibles)

# -------------------------------------
# 6. Filtrage du DataFrame selon les choix utilisateur
# -------------------------------------
df_filtre = df[(df['nom_pays'].isin(pays_selectionnes)) & (df['nom_maladie'] == maladie_selectionnee)]

# -------------------------------------
# 7. Liste des statistiques à visualiser
# -------------------------------------
statistiques = {
    'cas_totaux': "🟦 Cas Totaux",
    'nouveaux_cas': "🟨 Nouveaux Cas",
    'décès_totaux': "🟥 Décès Totaux",
    'nouveaux_décès': "🟧 Nouveaux Décès",
    'cas_actifs': "🟩 Cas Actifs",
    'total_guéris': "🟪 Total Guéris",
    'cas_graves': "🟫 Cas Graves",
    'nouveaux_cas_lisses': "🟦 Nouveaux Cas Lissés",
    'nouveaux_cas_lisses_par_million': "🔵 Cas Lissés par Million"
}

# -------------------------------------
# 8. Affichage des graphiques
# -------------------------------------
st.markdown("## 📊 Graphiques d'évolution par statistique")

for colonne, titre in statistiques.items():
    if colonne not in df_filtre.columns:
        continue  # On saute si la colonne n’existe pas

    fig = px.line(
        df_filtre,
        x="date",
        y=colonne,
        color="nom_pays",
        title=f"{titre} - {maladie_selectionnee}",
        labels={"date": "Date", colonne: titre}
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------
# 9. Message si pas de données
# -------------------------------------
if df_filtre.empty:
    st.warning("Aucune donnée disponible pour la sélection choisie.")
