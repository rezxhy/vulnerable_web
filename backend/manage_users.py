from pymongo import MongoClient
import os

MONGO_URI = "mongodb+srv://admin:caca@cluster0.7xkbg3y.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['audit_db']
users = db['users']

def list_users():
    print("\n📋 Utilisateurs actuels :")
    for user in users.find():
        print(f"  • {user['username']} : {user['password']}")
    print(f"\nTotal : {users.count_documents({})} utilisateurs\n")

def add_user():
    username = input("Nouveau username : ")
    password = input("Nouveau password : ")
    users.insert_one({'username': username, 'password': password})
    print(f"✅ Utilisateur '{username}' ajouté !")

def delete_user():
    username = input("Username à supprimer : ")
    result = users.delete_one({'username': username})
    if result.deleted_count > 0:
        print(f"✅ Utilisateur '{username}' supprimé !")
    else:
        print(f"❌ Utilisateur '{username}' introuvable")

def main():
    while True:
        print("\n=== GESTION DES UTILISATEURS ===")
        print("1. Lister les utilisateurs")
        print("2. Ajouter un utilisateur")
        print("3. Supprimer un utilisateur")
        print("4. Quitter")
        
        choice = input("\nChoix : ")
        
        if choice == '1':
            list_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            print("Au revoir !")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    try:
        client.admin.command('ping')
        print("✅ Connexion MongoDB OK\n")
        main()
    except Exception as e:
        print(f"❌ Erreur MongoDB : {e}")
    finally:
        client.close()