#from pymongo import MongoClient
#import pandas as pd
#
## Connexion à MongoDB
#client = MongoClient('mongodb://localhost:27017')
#db = client['brussels_data']
#collection = db['remarkable_trees']
#
## Chargement des données nettoyées
#df = pd.read_csv('arbres_remarquables_cleaned.csv')
#
## Conversion du DataFrame en dictionnaires pour l'insertion
#records = df.to_dict(orient='records')
#
## Insertion des données dans la collection
#collection.insert_many(records)
#
#print("Données insérées avec succès dans MongoDB.")

from pymongo import MongoClient
import pandas as pd

def insert_into_mongodb(dataframe, db_name, collection_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[collection_name]
    
    # Convertir le DataFrame en dictionnaire et insérer les données
    data_dict = dataframe.to_dict("records")
    collection.insert_many(data_dict)

    print(f"Données insérées avec succès dans {collection_name} de la base {db_name}.")

# Assurez-vous d'avoir le DataFrame harmonized_df prêt
harmonized_df = pd.read_csv('arbres_remarquables_cleaned.csv')

# Insérer les données dans MongoDB
insert_into_mongodb(harmonized_df, 'bruxelles_db', 'arbres_remarquables')