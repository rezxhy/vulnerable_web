#!/usr/bin/env python3
"""
Script de gestion des utilisateurs avec support des rôles
Permet d'ajouter, lister, modifier et supprimer des utilisateurs
"""

from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = "mongodb+srv://admin:caca@cluster0.7xkbg3y.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['audit_db']
users = db['users']


def list_users():
    """Liste tous les utilisateurs"""
    print("\n📋 Utilisateurs actuels :")
    print("=" * 80)
    
    all_users = list(users.find())
    
    if not all_users:
        print("Aucun utilisateur trouvé.")
        return
    
    print(f"{'Username':<20} {'Role':<15} {'Created At':<20}")
    print("-" * 80)
    
    for user in all_users:
        username = user.get('username', 'N/A')
        role = user.get('role', 'user')
        created_at = user.get('created_at', 'N/A')
        print(f"{username:<20} {role:<15} {created_at:<20}")
    
    print(f"\nTotal : {len(all_users)} utilisateurs\n")


def add_user():
    """Ajoute un nouvel utilisateur"""
    print("\n➕ Ajouter un utilisateur")
    print("=" * 80)
    
    username = input("Username : ").strip()
    
    # Vérifier si l'utilisateur existe déjà
    if users.find_one({'username': username}):
        print(f"❌ L'utilisateur '{username}' existe déjà !")
        return
    
    password = input("Password : ").strip()
    
    print("\nRôle :")
    print("  1. administrator (accès complet)")
    print("  2. user (accès limité)")
    role_choice = input("Choix (1/2) [défaut: 2] : ").strip() or "2"
    
    role = "administrator" if role_choice == "1" else "user"
    
    # Créer l'utilisateur
    new_user = {
        'username': username,
        'password': password,  # ⚠️ En clair pour le projet pédagogique
        'role': role,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    users.insert_one(new_user)
    print(f"\n✅ Utilisateur '{username}' ajouté avec succès !")
    print(f"   Rôle : {role}")
    print(f"   Créé le : {new_user['created_at']}")


def modify_user():
    """Modifie un utilisateur existant"""
    print("\n✏️  Modifier un utilisateur")
    print("=" * 80)
    
    username = input("Username à modifier : ").strip()
    
    user = users.find_one({'username': username})
    
    if not user:
        print(f"❌ Utilisateur '{username}' introuvable !")
        return
    
    print(f"\nUtilisateur trouvé :")
    print(f"  Username : {user.get('username')}")
    print(f"  Role : {user.get('role', 'user')}")
    print(f"  Créé le : {user.get('created_at', 'N/A')}")
    
    print("\nQue voulez-vous modifier ?")
    print("  1. Mot de passe")
    print("  2. Rôle")
    print("  3. Les deux")
    choice = input("Choix (1/2/3) : ").strip()
    
    update_data = {}
    
    if choice in ['1', '3']:
        new_password = input("Nouveau mot de passe : ").strip()
        if new_password:
            update_data['password'] = new_password
    
    if choice in ['2', '3']:
        print("\nNouveau rôle :")
        print("  1. administrator")
        print("  2. user")
        role_choice = input("Choix (1/2) : ").strip()
        new_role = "administrator" if role_choice == "1" else "user"
        update_data['role'] = new_role
    
    if update_data:
        users.update_one({'username': username}, {'$set': update_data})
        print(f"\n✅ Utilisateur '{username}' modifié avec succès !")
    else:
        print("\n⚠️  Aucune modification effectuée")


def delete_user():
    """Supprime un utilisateur"""
    print("\n🗑️  Supprimer un utilisateur")
    print("=" * 80)
    
    username = input("Username à supprimer : ").strip()
    
    user = users.find_one({'username': username})
    
    if not user:
        print(f"❌ Utilisateur '{username}' introuvable !")
        return
    
    print(f"\n⚠️  Êtes-vous sûr de vouloir supprimer '{username}' ?")
    print(f"   Rôle : {user.get('role', 'user')}")
    confirm = input("Confirmer (oui/non) : ").strip().lower()
    
    if confirm in ['oui', 'o', 'yes', 'y']:
        users.delete_one({'username': username})
        print(f"\n✅ Utilisateur '{username}' supprimé !")
    else:
        print("\n⚠️  Suppression annulée")


def main():
    """Menu principal"""
    try:
        client.admin.command('ping')
        print("✅ Connexion MongoDB OK")
    except Exception as e:
        print(f"❌ Erreur MongoDB : {e}")
        return
    
    while True:
        print("\n" + "=" * 80)
        print("🔐 GESTION DES UTILISATEURS - CyberTrust")
        print("=" * 80)
        print("1. 📋 Lister les utilisateurs")
        print("2. ➕ Ajouter un utilisateur")
        print("3. ✏️  Modifier un utilisateur")
        print("4. 🗑️  Supprimer un utilisateur")
        print("5. ❌ Quitter")
        print("=" * 80)
        
        choice = input("\nVotre choix : ").strip()
        
        if choice == '1':
            list_users()
        elif choice == '2':
            add_user()
        elif choice == '3':
            modify_user()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide")
        
        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
    finally:
        client.close()