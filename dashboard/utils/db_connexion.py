# dashboard/utils/db_connexion.py

import psycopg2

def connecter_db():
    return psycopg2.connect(
        host="localhost",
        database="pandemie_mspr",
        user="postgres",
        password="admin"
    )
