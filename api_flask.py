from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Configuration de la connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['bruxelles_db']
collection = db['arbres_remarquables']

@app.route('/api/arbres', methods=['GET'])
def get_arbres():
    # Récupérer tous les documents de la collection
    arbres = list(collection.find({}, {'_id': 0}))  # Exclure le champ _id pour simplifier la réponse
    return jsonify(arbres)

@app.route('/api/arbres/search', methods=['GET'])
def search_arbres():
    # Récupérer les paramètres de recherche depuis l'URL
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing search parameter 'name'"}), 400
    
    # Effectuer une recherche par nom
    arbres = list(collection.find({"nom_harmonisé_1": {"$regex": name, "$options": "i"}}, {'_id': 0}))
    return jsonify(arbres)

if __name__ == '__main__':
    app.run(debug=True)