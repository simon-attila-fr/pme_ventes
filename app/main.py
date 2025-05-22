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

ui_server_name = "0.0.0.0"
server_port = 6789
montrer_table_menu = ("magasins", "produits", "ventes")
analyse_menu = (
    "magasins_classement_par_quantite_vendue",
    "magasins_classement_par_revenu",
    "produits_classement_par_quantite_vendu",
    "produits_classement_par_revenue",
    "ventes_classement_de_jours_par_revenue",
    "ventes_classement_jours_totale_revenue"
    "ventes_moyenne_revenue_par_produit_par_ventes",
    "ventes_totale_de_periode"
)
ui_menu = montrer_table_menu + analyse_menu
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
    print("magasins_is_empty", magasins_is_empty)
    produits_is_empty = fonctions_aidants.check_si_table_est_vide("produits", cursor)
    print("produits_is_empty", produits_is_empty)
    ventes_is_empty = fonctions_aidants.check_si_table_est_vide("ventes", cursor)
    print("ventes_is_empty", ventes_is_empty)

    def csv_to_sql(lien, nom_table, bdd_connexion):
        # ---------- Récupérer les données CSV ----------
        response = requests.get(lien)
        print(f"{nom_table} status : {response.status_code}")
        # ---------- Si réussite, sauvegarder dans la base de données ----------
        if response.status_code == 200:
            print("csv_to_sql...")
            response.encoding  = 'utf-8'
            fonctions_aidants.bdd_ajoute_csv(nom_table, response.text, bdd_connexion)
        else:
            raise Exception("Les données initiales ne peuvent pas être récupérées.")

    # ---------- AJOUTE à la BASE DE DONNÉES si besoin ----------

    if magasins_is_empty:
        csv_to_sql(magasins_lien, "magasins", bdd_connexion)
    
    if produits_is_empty:
        csv_to_sql(produits_lien, "produits", bdd_connexion)
        
    if ventes_is_empty:
        csv_to_sql(ventes_lien, "ventes", bdd_connexion)

    # ---------- INTERFACE ----------
    sys_message= ''

    def function_pme_interface(option):
        global sys_message
        if option in montrer_table_menu: # Lire une table en entier
            data = fonctions_aidants.bdd_lire_tout(option, sqlite3.connect, bdd_path)
            df = pandas.DataFrame(data["result"], columns=data["header"])
            sys_message = f"Requête réussie sur la table '{option}'."
            return df, sys_message
        elif option in analyse_menu: # Lire une requête d'analyse
            analyse_scripts_path = os.path.join(os.path.dirname(__file__), 'sql', f'{option}.sql')
            print("analyse_scripts_path: ", analyse_scripts_path)
            result = fonctions_aidants.executer_analyse_script(sqlite3.connect, bdd_path, analyse_scripts_path)
            sys_message = f"Requête réussie : '{option}'."
            return result, sys_message
        else:
            sys_message = "Option invalide."
            return pandas.DataFrame(), sys_message

    pme_ventes_interface = gradio.Interface(
        fn = function_pme_interface,
        inputs = [gradio.Dropdown(choices=ui_menu,
                                  label="Sélectionner une expression SQL")],
        outputs = [gradio.Dataframe(label="Résultat"),
                   gradio.Textbox(label="Message Système", interactive=False)],
        title = "PME ventes"
    )

    pme_ventes_interface.launch(server_name=ui_server_name, server_port=server_port)

    def bdd_ventes_maj_reguliere():
        bdd_maj.bdd_maj()
        while True:
            time.sleep(120)
            bdd_maj.bdd_maj()
    thread = threading.Thread(target=bdd_ventes_maj_reguliere, daemon=True)
    thread.start()

except Exception as error:
    print("Erreur lors de traitement des données : ", error)
