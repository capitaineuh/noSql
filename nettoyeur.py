import pandas as pd

def clean_data(filename):
    # Charger les données depuis le fichier CSV
    df = pd.read_csv(filename)

    # Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # Remplacer les valeurs manquantes par NaN (ou une autre valeur par défaut)
    df.fillna(value=pd.NA, inplace=True)

    # Convertir les formats si nécessaire (exemple : convertir les dates)
    # df['date_colonne'] = pd.to_datetime(df['date_colonne'], errors='coerce')

    return df

# Nettoyer les données
cleaned_df = clean_data('bruxelles_parcours_bd.csv')

def harmonize_fields(df):
    # Renommer les colonnes pour assurer une harmonisation
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

    return df

# Harmoniser les champs
harmonized_df = harmonize_fields(cleaned_df)

# Afficher un aperçu des données harmonisées
print(harmonized_df.head())

# Afficher un aperçu des données nettoyées
print(cleaned_df.head())