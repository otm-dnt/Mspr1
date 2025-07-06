# 📄 dashboard/pages/1_vue_globale.py

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# ✅ Connexion PostgreSQL
@st.cache_resource
def connecter_db():
    return psycopg2.connect(
        host="localhost",
        database="pandemie_mspr",
        user="postgres",
        password="admin"
    )

# ✅ Charger les données
@st.cache_data
def charger_donnees():
    conn = connecter_db()
    query = """
        SELECT s.date, p.nom_pays, m.nom_maladie,
               s.cas_totaux, s.décès_totaux
        FROM STATISTIQUE s
        JOIN PAYS p ON s.id_pays = p.id_pays
        JOIN MALADIE m ON s.id_maladie = m.id_maladie
    """
    df = pd.read_sql(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    return df

# 🖥️ Titre de la page
st.title("📊 Vue Globale des Pandémies")

df = charger_donnees()

# 🔍 Filtres (pays + maladie)
col1, col2 = st.columns(2)
with col1:
    pays_selectionne = st.selectbox("🌍 Choisir un pays", sorted(df["nom_pays"].unique()))

with col2:
    maladie_selectionnee = st.selectbox("🦠 Choisir une maladie", sorted(df["nom_maladie"].unique()))

# 🧼 Filtrage
df_filtré = df[(df["nom_pays"] == pays_selectionne) & (df["nom_maladie"] == maladie_selectionnee)]

# 📈 Graphique des cas
fig1 = px.line(
    df_filtré,
    x="date",
    y="cas_totaux",
    title=f"📈 Évolution des cas totaux en {pays_selectionne}",
    labels={"cas_totaux": "Nombre de cas", "date": "Date"}
)
st.plotly_chart(fig1, use_container_width=True)

# 📉 Graphique des décès
fig2 = px.line(
    df_filtré,
    x="date",
    y="décès_totaux",
    title=f"📉 Évolution des décès totaux en {pays_selectionne}",
    labels={"décès_totaux": "Nombre de décès", "date": "Date"}
)
st.plotly_chart(fig2, use_container_width=True)

# ✅ Confirmation
st.success("✅ Graphiques mis à jour sans les nouveaux cas/décès.")
