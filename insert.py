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
harmonized_df = pd.read_csv('bruxelles_parcours_bd.csv')

# Insérer les données dans MongoDB
insert_into_mongodb(harmonized_df, 'bruxelles_db', 'parcours_DB')