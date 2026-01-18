from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Connexion MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['audit_db']
users = db['users']

print(f"MONGO_URI chargée : {MONGO_URI}")
print("Tentative de connexion à MongoDB...")

try:
    client.admin.command('ping')
    print("Connexion MongoDB OK !")
except Exception as e:
    print(f"ERREUR CONNEXION MONGO : {e}")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Recherche utilisateur
    user = users.find_one({'username': username, 'password': password})

    if user:
        return jsonify({
            'message': 'Connexion réussie !',
            'success': True,
            'username': username
        })
    else:
        return jsonify({
            'message': 'Identifiants invalides',
            'success': False
        }), 401

@app.route('/data', methods=['GET'])
def get_data():
    """Récupère toutes les données de toutes les collections"""
    try:
        all_data = {}
        
        # Récupérer toutes les collections
        collections = db.list_collection_names()
        
        for collection_name in collections:
            collection = db[collection_name]
            # Convertir ObjectId en string pour JSON
            documents = []
            for doc in collection.find().limit(100):  # Limite à 100 docs par collection
                doc['_id'] = str(doc['_id'])
                documents.append(doc)
            
            all_data[collection_name] = {
                'count': collection.count_documents({}),
                'documents': documents
            }
        
        return jsonify({
            'success': True,
            'database': 'audit_db',
            'collections': all_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/collection/<collection_name>', methods=['GET'])
def get_collection(collection_name):
    """Récupère les données d'une collection spécifique"""
    try:
        collection = db[collection_name]
        documents = []
        
        for doc in collection.find():
            doc['_id'] = str(doc['_id'])
            documents.append(doc)
        
        return jsonify({
            'success': True,
            'collection': collection_name,
            'count': len(documents),
            'documents': documents
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)