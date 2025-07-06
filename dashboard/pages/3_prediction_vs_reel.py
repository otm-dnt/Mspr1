# 📁 dashboard/pages/3_prediction_vs_reel.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# ✅ Titre et introduction
# ------------------------------------------------------
st.title("📈 Comparaison Taux de Transmission : Réel vs Prédit")

st.markdown("""
Cette page compare le **taux de transmission réel** observé dans les données
avec le **taux prédit** par le modèle de Machine Learning.

✔ Tu peux choisir un pays pour visualiser la qualité des prédictions.
""")

# ------------------------------------------------------
# ✅ 1️⃣ Charger les résultats de prédiction
# ------------------------------------------------------
@st.cache_data
def charger_donnees():
    return pd.read_csv("prediction/predictions_resultats.csv", parse_dates=['date'])

df = charger_donnees()

# ------------------------------------------------------
# ✅ 2️⃣ Sélection du pays
# ------------------------------------------------------
pays_disponibles = sorted(df['nom_pays'].dropna().unique())
pays_selectionne = st.selectbox("🌍 Choisir un pays :", pays_disponibles)

# ------------------------------------------------------
# ✅ 3️⃣ Filtrage des données pour ce pays
# ------------------------------------------------------
df_pays = df[df['nom_pays'] == pays_selectionne].sort_values('date')

if df_pays.empty:
    st.warning("Aucune donnée disponible pour ce pays.")
    st.stop()

# ------------------------------------------------------
# ✅ 4️⃣ Graphique avec Plotly
# ------------------------------------------------------
fig = px.line(
    df_pays,
    x="date",
    y=["taux_transmission", "taux_transmission_prédit"],
    labels={"value": "Taux de Transmission", "variable": "Type"},
    title=f"Taux de Transmission : Réel vs Prédit ({pays_selectionne})",
)

fig.update_traces(mode='lines+markers')
fig.update_layout(
    legend_title_text='Type de courbe',
    legend=dict(
        itemsizing='constant'
    )
)

# ✅ 5️⃣ Affichage du graphique
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# ✅ 6️⃣ Explications supplémentaires
# ------------------------------------------------------
st.markdown("""
**ℹ️ Interprétation :**  
- La courbe bleue correspond au **taux réel** observé dans l'historique.
- La courbe rouge pointillée correspond au **taux prédit** par le modèle.
- Plus les deux courbes se ressemblent, plus le modèle est fiable pour ce pays.

En cas de fortes différences, cela montre qu'il reste des marges d'amélioration.
""")
