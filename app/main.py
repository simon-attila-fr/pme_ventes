import requests
import io
import pandas

# PARAMETERS

# ---------- Récupérer les données ----------
protocol = "https"
host = "docs.google.com/spreadsheets"

# Liens pour envoyer des requêtes HTTP pour récupérer les données nécessaires.
ventes_lien = f"{protocol}://{host}/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
produits_lien = f"{protocol}://{host}/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
magasins_lien = f"{protocol}://{host}/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
# --------------------

# EXECUTION
try:
    # ---------- Récupérer les données ----------
    ventes_response = requests.get(ventes_lien)
    print(f"Ventes: {ventes_response.status_code}")
    produits_response = requests.get(produits_lien)
    print(f"Produits: {produits_response.status_code}")
    magasins_response = requests.get(magasins_lien)
    print(f"Magasins: {magasins_response.status_code}")

    if ventes_response.status_code == 200 and produits_response.status_code == 200 and magasins_response.status_code == 200:
        ventes_response.encoding = 'utf-8' # Forcer utf-8 encoding
        produits_response.encoding = 'utf-8'
        magasins_response.encoding  = 'utf-8'

        print(pandas.read_csv(io.StringIO(ventes_response.text)))
        print(pandas.read_csv(io.StringIO(produits_response.text)))
        print(pandas.read_csv(io.StringIO(magasins_response.text)))
        print("Les données initiales on bien été récupérées.")
    else:
        raise Exception("Les données initiales ne peuvent pas être récupérées.")
    
    # ---------- Remplir la base de données ----------
    
except Exception as error:
    print("Erreur lors de la récupération des données initiales: ", error)
