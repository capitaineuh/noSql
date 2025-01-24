from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Configuration de la connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client['bruxelles_db']

# Fonctions d'harmonisation pour chaque dataset
def harmonize_arbres(arbres):
    # Harmonisation spécifique pour les arbres
    return arbres

def harmonize_musees(musees):
    # Harmonisation spécifique pour les musées
    return musees

def harmonize_urinoirs(urinoirs):
    # Harmonisation spécifique pour les urinoirs publics
    return urinoirs

def harmonize_streetart(streetart):
    # Harmonisation spécifique pour le streetart
    return streetart

# Route pour les arbres remarquables
@app.route('/api/arbres', methods=['GET'])
def get_arbres():
    collection = db['arbres_remarquables']
    arbres = list(collection.find({}, {'_id': 0}))
    arbres = harmonize_arbres(arbres)
    return jsonify(arbres)

# Route pour les musées
@app.route('/api/musees', methods=['GET'])
def get_musees():
    collection = db['musees_a_bruxelles']
    musees = list(collection.find({}, {'_id': 0}))
    musees = harmonize_musees(musees)
    return jsonify(musees)

# Route pour les urinoirs publics
@app.route('/api/urinoirs', methods=['GET'])
def get_urinoirs():
    collection = db['urinoirs_publics']
    urinoirs = list(collection.find({}, {'_id': 0}))
    urinoirs = harmonize_urinoirs(urinoirs)
    return jsonify(urinoirs)

# Route pour le streetart
@app.route('/api/streetart', methods=['GET'])
def get_streetart():
    collection = db['streetart']
    streetart = list(collection.find({}, {'_id': 0}))
    streetart = harmonize_streetart(streetart)
    return jsonify(streetart)

# Route de recherche pour les arbres
@app.route('/api/arbres/search', methods=['GET'])
def search_arbres():
    collection = db['arbres_remarquables']
    name = request.args.get('nom_francais')
    if not name:
        return jsonify({"error": "Missing search parameter 'nom_francais'"}), 400
    arbres = list(collection.find({"nom_harmonisé_1": {"$regex": name, "$options": "i"}}, {'_id': 0}))
    arbres = harmonize_arbres(arbres)
    return jsonify(arbres)

if __name__ == '__main__':
    app.run(debug=True)