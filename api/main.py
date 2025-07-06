# 📁 api/main.py

from fastapi import FastAPI
import psycopg2
import pandas as pd
from fastapi.responses import JSONResponse

# 🚀 On lance notre application FastAPI
app = FastAPI(title="API Pandémie", version="1.0")

# 🔗 Connexion à la base de données PostgreSQL
def connecter_db():
    try:
        connexion = psycopg2.connect(
            host="localhost",
            database="pandemie_mspr",
            user="postgres",
            password="admin"
        )
        return connexion
    except Exception as e:
        print("❌ Erreur de connexion à PostgreSQL :", e)
        return None

# 🔍 Exemple de route simple pour tester
@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API des pandémies !"}


# 🔎 Route pour récupérer la liste des pays
@app.get("/pays")
def get_pays():
    conn = connecter_db()
    if not conn:
        return JSONResponse(content={"error": "Connexion impossible"}, status_code=500)

    try:
        df = pd.read_sql("SELECT * FROM PAYS ORDER BY nom_pays ASC;", conn)
        return df.to_dict(orient="records")  # Convertit en JSON lisible
    finally:
        conn.close()


# 🔎 Route pour les maladies
@app.get("/maladies")
def get_maladies():
    conn = connecter_db()
    if not conn:
        return JSONResponse(content={"error": "Connexion impossible"}, status_code=500)

    try:
        df = pd.read_sql("SELECT * FROM MALADIE;", conn)
        return df.to_dict(orient="records")
    finally:
        conn.close()


# 🔎 Route pour récupérer toutes les statistiques
@app.get("/statistiques")
def get_statistiques():
    conn = connecter_db()
    if not conn:
        return JSONResponse(content={"error": "Connexion impossible"}, status_code=500)

    try:
        df = pd.read_sql("""
            SELECT s.*, p.nom_pays, m.nom_maladie
            FROM STATISTIQUE s
            JOIN PAYS p ON s.id_pays = p.id_pays
            JOIN MALADIE m ON s.id_maladie = m.id_maladie
            LIMIT 100;
        """, conn)
        return df.to_dict(orient="records")
    finally:
        conn.close()
