import requests
import pandas as pd
from pymongo import MongoClient

# Liste des URLs des bases de données à récupérer
api_urls = [
    "https://opendata.brussels.be/api/records/1.0/search/?dataset=bruxelles_parcours_bd",
    "https://opendata.brussels.be/api/records/1.0/search/?dataset=bruxelles_arbres_remarquables",
    "https://opendata.brussels.be/api/records/1.0/search/?dataset=musees-a-bruxelles",
    "https://opendata.brussels.be/api/records/1.0/search/?dataset=bruxelles_urinoirs_publics",
    "https://opendata.brussels.be/api/records/1.0/search/?dataset=streetart"
]

# Fonction pour harmoniser les champs pour chaque URL
def harmonize_fields_url1(df):
    df.rename(columns={
        'surface_m2': 'surface_metres_carre',
        'lien_site_parcours_bd': 'lien_site_francais',
        'adres': 'adresse_nl',
        'dessinateur': 'auteur',
        'commune_gemeente': 'commune',
        'adresse': 'adresse_fr',
        'naam_fresco_nl': 'nom_fresque_nl',
        'date': 'annee_creation',
        'nom_de_la_fresque': 'nom_fresque_fr',
        'realisateur': 'realisateur',
        'link_site_striproute': 'lien_site_neerlandais',
        'image': 'url_image',
        'maison_d_edition': 'maison_edition',
        'coordonnees_geographiques': 'coordonnees_geo'
    }, inplace=True)

def harmonize_fields_url2(df):
    df.rename(columns={
        'geo_point_2d': 'coordonnees_geo',
        'circonference': 'circonference_m',
        'rarete': 'niveau_rarete',
        'statuts_fr': 'statut_fr',
        'nom_fr': 'nom_francais',
        'url_fr': 'lien_francais',
        'firstimage': 'image_url',
        'nom_nl': 'nom_neerlandais',
        'nom_la': 'nom_latin',
        'statuts_nl': 'statut_neerlandais',
        'id_arbres_cms': 'id_arbre',
        'diametre_cime': 'diametre_cime_m',
        'url_nl': 'lien_neerlandais'
    }, inplace=True)
    # Convertir les colonnes si nécessaire, par exemple, convertir 'circonference' en float
    df['circonference_m'] = df['circonference_m'].astype(float)
    df['diametre_cime_m'] = df['diametre_cime_m'].astype(float)
    df['niveau_rarete'] = df['niveau_rarete'].astype(float)

def harmonize_fields_url3(df):
    df.rename(columns={
        'commune_gemeente': 'commune',
        'latitude_breedtegraad': 'latitude',
        'telephone_telefoon': 'telephone',
        'adresse': 'adresse',
        'code_postal_postcode': 'code_postal',
        'coordonnees_geographiques': 'coordonnees_geo',
        'e_mail': 'email',
        'site_web_website': 'site_web',
        'nom_du_musee': 'nom_musee',
        'longitude_lengtegraad': 'longitude',
        'facebook': 'lien_facebook'
    }, inplace=True)

    # Convertir les colonnes latitude et longitude en float
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    
def harmonize_fields_url4(df):
    df.rename(columns={
        'typeeng': 'type_anglais',
        'wgs84_long': 'longitude',
        'wgs84_lat': 'latitude',
        'z_pcdd_nl': 'commune_nl',
        'adrvoisfr': 'adresse_fr',
        'wgs84_lalo': 'coordonnees_geo',
        'typefr': 'type_francais',
        'z_pcdd_fr': 'commune_fr',
        'typedut': 'type_neerlandais',
        'statuut': 'statut',
        'adrvoisnl': 'adresse_nl'
    }, inplace=True)

    # Convertir les colonnes latitude et longitude en float (même si c'est déjà fait en amont, mieux vaut 2x qu'une!)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    
def harmonize_fields_url5(df):
    df.rename(columns={
        'nom_de_l_artiste': 'nom_artiste',
        'annee': 'annee_creation',
        'lieu': 'lieu_fr',
        'geocoordinates': 'coordonnees_geo',
        'adres': 'adresse_nl',
        'plaats': 'lieu_nl',
        'adresse': 'adresse_fr',
        'location': 'location_fr',
        'photo': 'photo_info'
    }, inplace=True)

    # Convertir les coordonnées géographiques en colonnes latitude et longitude séparées
    df['latitude'] = df['coordonnees_geo'].apply(lambda x: x[0])
    df['longitude'] = df['coordonnees_geo'].apply(lambda x: x[1])

    # Si vous avez besoin de traitements supplémentaires, tels que la conversion de types ou l'ajout de nouvelles colonnes, vous pouvez les ajouter ici

# Fonction pour récupérer et traiter les données
def fetch_and_process_data(api_url):
    params = {"rows": 10, "start": 0, "format": "json"}
    all_records = []

    try:
        while True:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            records = data.get('records', [])
            all_records.extend([record['fields'] for record in records])

            params['start'] += params['rows']
            if params['start'] >= data['nhits']:
                break

        df = pd.DataFrame(all_records)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API {api_url}: {e}")
        return pd.DataFrame()

# Fonction pour insérer les données dans MongoDB
def insert_into_mongodb(dataframe, db_name, collection_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[collection_name]
    if not dataframe.empty:
        data_dict = dataframe.to_dict("records")
        collection.insert_many(data_dict)
        print(f"Données insérées avec succès dans {collection_name} de la base {db_name}.")

# Automatisation du processus pour toutes les URLs
for i, url in enumerate(api_urls):
    df = fetch_and_process_data(url)
    
    # Appliquer l'harmonisation spécifique à chaque URL
    if i == 0:
        harmonize_fields_url1(df)
    elif i == 1:
        harmonize_fields_url2(df)
    elif i == 2:
        harmonize_fields_url3(df)
    elif i == 3:
        harmonize_fields_url4(df)
    elif i == 4:
        harmonize_fields_url5(df)
    
    # Ajoutez d'autres conditions pour chaque URL

    collection_name = f"collection_{i+1}"  # Nom de collection unique pour chaque URL
    insert_into_mongodb(df, 'votre_db', collection_name)