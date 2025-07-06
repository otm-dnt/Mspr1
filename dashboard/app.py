# dashboard/app.py

import streamlit as st

# 🔧 Configure la page principale
st.set_page_config(
    page_title="Tableau de bord des Pandémies",  # Titre de l'onglet
    layout="wide"                                # Affichage large (pleine page)
)

# 🧠 C'est la page d'accueil, pas de graphique ici
st.title("🌍 Tableau de bord des Pandémies")

# 👉 Menu à gauche (sidebar)
st.sidebar.title("Navigation")
st.sidebar.info("Choisis une page dans le menu ci-dessus 👆")

# ✨ Message principal
st.markdown("""
Bienvenue sur le tableau de bord interactif !  
Utilise les menus à gauche pour explorer les cas, décès, guérisons et autres statistiques liées à **COVID-19** et **Monkeypox**.
""")
