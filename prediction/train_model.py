# prediction/train_model.py

import pandas as pd               # Pour manipuler les données
import psycopg2                   # Pour se connecter à PostgreSQL
from sklearn.linear_model import LinearRegression  # Pour la prédiction simple
import matplotlib.pyplot as plt   # Pour visualiser la courbe

# 1️⃣ Connexion à PostgreSQL
def connecter_db():
    return psycopg2.connect(
        host="localhost",
        database="pandemie_mspr",
        user="postgres",
        password="admin"
    )

# 2️⃣ Charger les données (exemple : nouveaux cas COVID)
def charger_donnees():
    conn = connecter_db()
    query = """
        SELECT date, nouveaux_cas
        FROM STATISTIQUE s
        JOIN MALADIE m ON s.id_maladie = m.id_maladie
        WHERE m.nom_maladie = 'COVID-19'
        ORDER BY date
    """
    df = pd.read_sql(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    conn.close()
    return df

# 3️⃣ Exemple d'affichage
if __name__ == "__main__":
    df = charger_donnees()
    print(df.head())

    # Visualiser rapidement
    plt.plot(df["date"], df["nouveaux_cas"])
    plt.title("Historique des nouveaux cas COVID-19")
    plt.xlabel("Date")
    plt.ylabel("Nouveaux cas")
    plt.show()
