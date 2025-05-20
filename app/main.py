import requests
import io
import pandas
import os
import sqlite3
import gradio
import threading
import time
from src import fonctions_aidants
from src import bdd_maj

# ---------- PARAMETERS ----------

# Base de données
bdd_path = os.getenv('SQLITE_BDD_PATH', '/bdd/bdd.sqlite3') # Bdd path
table_noms = ("magasins", "produits", "ventes")
init_tables_path = os.path.join(os.path.dirname(__file__), 'sql', 'init_tables.sql') # SQL script pour initialiser la bdd

# Source de données : Liens pour envoyer des requêtes HTTP pour récupérer les données nécessaires.
ventes_lien = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
produits_lien = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
magasins_lien = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
# --------------------

# EXECUTION
try:
    # Initialisation de la base de données
    with sqlite3.connect(bdd_path) as bdd_connexion:
        cursor = bdd_connexion.cursor()

    # Charger et executer un script SQL pour initialiser les tables de la base de données si les tables n'existent pas.
    with open(init_tables_path, 'r', encoding='utf-8') as initbdd:
        sql_script = initbdd.read()
        cursor.executescript(sql_script)
    
    bdd_connexion.commit()

    # Conditions
    # Tables vides ?    
    magasins_is_empty = fonctions_aidants.check_si_table_est_vide("magasins", cursor)
    produits_is_empty = fonctions_aidants.check_si_table_est_vide("produits", cursor)
    ventes_is_empty = fonctions_aidants.check_si_table_est_vide("ventes", cursor)

    if (not magasins_is_empty) or (not produits_is_empty) or (not ventes_is_empty):
        # ---------- Récupérer les données CSV ----------
        ventes_response = requests.get(ventes_lien)
        print(f"Ventes status : {ventes_response.status_code}")
        produits_response = requests.get(produits_lien)
        print(f"Produits status : {produits_response.status_code}")
        magasins_response = requests.get(magasins_lien)
        print(f"Magasins status : {magasins_response.status_code}")

        if ventes_response.status_code == 200 and produits_response.status_code == 200 and magasins_response.status_code == 200:
            ventes_response.encoding = 'utf-8' # Forcer utf-8 encoding
            produits_response.encoding = 'utf-8'
            magasins_response.encoding  = 'utf-8'

            bdd_connexion = sqlite3.connect(bdd_path)
            cursor = bdd_connexion.cursor()

            # ---------- Ajoute à la base de données ----------

            # Magasins
            fonctions_aidants.bdd_ajoute_csv("magasins", magasins_response.text, bdd_connexion)

            # Produits
            fonctions_aidants.bdd_ajoute_csv("produits", produits_response.text, bdd_connexion)

            # Ventes
            fonctions_aidants.bdd_ajoute_csv("ventes", ventes_response.text, bdd_connexion)

            bdd_connexion.close()
            print("Les données initiales on bien été récupérées.")
        else:
            bdd_connexion.close()
            raise Exception("Les données initiales ne peuvent pas être récupérées.")
    else: # La base de données n'est pas vide
        print("La base de données n'est pas vide.")

    # ---------- Interface ----------

    def function_pme_interface(option):
        if option == "magasins" or option == "produits" or option == "ventes":
            return fonctions_aidants.bdd_lire_tout(option, sqlite3.connect, bdd_path)
        elif option == "magasins description":
            bdd_connexion = sqlite3.connect(bdd_path)
            cursor = bdd_connexion.cursor()
            result = bdd_connexion.execute("PRAGMA table_info(magasins);").fetchall()
            cursor.close()
            return result

    pme_app_interface = gradio.Interface(
        fn = function_pme_interface,
        inputs = [gradio.Dropdown(choices=["magasins", "magasins description", "produits", "ventes"], label="Sélectionner une expression SQL")],
        # outputs = [gradio.Textbox(label="Résultat", lines=10, max_lines=100, interactive=False)],
        outputs = [gradio.Dataframe(label="Résultat")],
        title = "PME ventes"
    )

    pme_app_interface.launch(server_name="0.0.0.0", server_port=6789)

    def bdd_ventes_maj_reguliere():
        bdd_maj.bdd_maj()
        while True:
            time.sleep(120)
            bdd_maj.bdd_maj()
    thread = threading.Thread(target=bdd_ventes_maj_reguliere, daemon=True)
    thread.start()

except Exception as error:
    print("Erreur lors de traitement des données : ", error)
