import pandas
import io
import re
import unicodedata

# PARAMETRES
table_noms = ("magasins", "produits", "ventes")

# Cette fonction permet de vérifier si la table X est vide ou pas.
# nom_table   string
# cursor      cursor object
# returns     Bool
def check_si_table_est_vide(nom_table, cursor):
        try:
            if nom_table in table_noms:
                cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {nom_table} LIMIT 1);")
                return cursor.fetchone()[0] == 1  # 1 si la table contient des données, 0 si elle est vide.
            else:
                raise ValueError
        except Exception as error:
            print(error)
            return False

# Cette fonction permet d'ajouter des données sous format CSV à une table dans la base de données.
# table                    string
# table_response_text      text attribut d'un objet Response de la librairie requests
# bdd_conn                 objet de connexion d'une base de données
# returns                  -        
def bdd_ajoute_csv(table, table_response_text, bdd_conn, if_exists="append"):
    table_read_csv = pandas.read_csv(io.StringIO(table_response_text))
    print("table read csv\n", table_read_csv)
    table_read_csv.columns = table_read_csv.columns.str.strip()
    def to_snake_case(str):
        str = unicodedata.normalize('NFKD', str).encode('ASCII', 'ignore').decode()
        str = re.sub(r'[\s\-]+', '_', str)
        str = re.sub(r'([a-z])([A-Z])', r'\1_\2', str)
        return str.lower()
    table_read_csv.columns = [to_snake_case(col) for col in table_read_csv.columns]
    table_read_csv.to_sql(table, bdd_conn, if_exists=if_exists, index=False)

# Cette fonction permet de récupérer toutes les enregisrements d'une table.
# La fonction d'abord crée une couvelle connexion à la base de données, ensuite elle récupère les données demandées, clotûre
# le connexion et rend le résultat de la requête sql.
# table_name        string
# connect_fonction  fonction
# bdd_path          string
def bdd_lire_tout(table_name, connect_fonction, bdd_path):
    if table_name in table_noms:
        bdd_connexion = connect_fonction(bdd_path)
        cursor = bdd_connexion.cursor()
        query = f"SELECT * FROM {table_name}"
        result = cursor.execute(query).fetchall()
        header = cursor.description
        cleaned_header = []
        for header_element in header:
            cleaned_header.append(header_element[0])
        print("cleaned_header\n", cleaned_header)
        cursor.close()
        return { "result": result, "header":cleaned_header }
    else:
        raise ValueError