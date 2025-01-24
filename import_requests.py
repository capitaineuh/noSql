import requests
import pandas as pd

# URL de l'API (remplacez par l'URL réelle de votre API)
api_url = "https://opendata.brussels.be/api/records/1.0/search/?dataset=bruxelles_arbres_remarquables"
params = {
    "rows": 10,  # Nombre d'enregistrements par page
    "start": 0,  # Indice de départ
    "format": "json"
}

all_records = []

try:
    while True:
        # Appel à l'API avec pagination
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        # Extraire les données JSON de la réponse
        data = response.json()

        # Extraire et ajouter les enregistrements
        records = data['records']
        all_records.extend([record['fields'] for record in records])

        # Mettre à jour l'indice de départ pour la prochaine page
        params['start'] += params['rows']

        # Arrêter si tous les enregistrements ont été récupérés
        if params['start'] >= data['nhits']:
            break

    # Convertir en DataFrame
    df = pd.DataFrame(all_records)

    # Nettoyage des Données
    # Exemple : Remplacer les valeurs manquantes par NaN
    df.fillna(value=pd.NA, inplace=True)

    # Harmonisation des Données
    # Exemple : Uniformiser les noms de colonnes
    df.rename(columns={
        'nom_fr': 'nom_francais',
        'nom_nl': 'nom_neerlandais',
        'nom_la': 'nom_latin',
        'circonference': 'circonference_m'
    }, inplace=True)

    # Sauvegarder le DataFrame nettoyé et harmonisé dans un fichier CSV
    df.to_csv('arbres_remarquables_cleaned.csv', index=False)

    print("Données enregistrées dans le fichier CSV 'arbres_remarquables_cleaned.csv'.")
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de l'appel à l'API : {e}")