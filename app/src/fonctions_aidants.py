import pandas
import io

# Cette fonction permet de vérifier si la table X est vide ou pas.
# nom_table   string
# cursor      cursor object
# returns     Bool
def check_si_table_est_vide(nom_table, cursor):
        try:
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM {nom_table} LIMIT 1);")
            return cursor.fetchone()[0] == 1  # 1 if table has data, 0 if empty
        except Exception as error:
            print(error)
            return False

# Cette fonction permet d'ajouter des données sous format CSV à une table dans la base de données.
# table                    string
# table_response_text      text attribut d'un objet Response de la librairie requests
# bdd_conn                 objet de connexion d'une base de données
# returns                  -        
def bdd_ajoute_csv(table, table_response_text, bdd_conn):
    table_read_csv = pandas.read_csv(io.StringIO(table_response_text))
    table_read_csv.columns = table_read_csv.columns.str.strip()
    table_read_csv.to_sql(table, bdd_conn, if_exists='replace', index=False)

def bdd_lire_tout(table_name, connect_fonction, bdd_path):
    bdd_connexion = connect_fonction(bdd_path)
    cursor = bdd_connexion.cursor()
    result = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
    cursor.close()
    return result