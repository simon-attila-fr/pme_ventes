import sqlite3
import os
import requests
import pandas
import io
import datetime

def bdd_maj():
    try:
        print(f"[{datetime.datetime.now()}] Recherche de nouvelles ventes...")
        # Lire la table ventes --> la date de la dernière vente.
        bdd_path = os.getenv('SQLITE_BDD_PATH', '/bdd/bdd.sqlite3') # Bdd path

        with sqlite3.connect(bdd_path) as bdd_connexion:
            cursor = bdd_connexion.cursor()
            dernier_vente = cursor.execute("SELECT date FROM ventes ORDER BY date DESC LIMIT 1").fetchone()
            dernier_vente_date = pandas.to_datetime(dernier_vente[0]) if dernier_vente else None

        # HTTP GET ventes csv

        ventes_lien = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
        print("Récupération des données depuis une source extérieure...")
        ventes_response = requests.get(ventes_lien)
        if ventes_response.status_code == 200:
            print("OK")
            ventes_response.encoding = 'utf-8'

        # Couper la partie où la date est supérieure à la date du dernier élément dans la table ventes
            ventes_response_dataframe = pandas.read_csv(io.StringIO(ventes_response.text))
            ventes_response_dataframe["Date"] = pandas.to_datetime(ventes_response_dataframe["Date"])
            nouvelles_ventes = ventes_response_dataframe[ventes_response_dataframe["Date"] > dernier_vente_date]
            if not nouvelles_ventes.empty:
                print("Rajoute de nouvelles données...")
                nouvelles_ventes.to_sql("ventes", bdd_connexion, if_exists="append", index=False)
                print("OK")
            else:
                print("Il n'y a pas de nouvelles ventes.")

        bdd_connexion.close()
    except Exception as error:
        print("Erreur lors de la mise à jour de la base de données : ", error)