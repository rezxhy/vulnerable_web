#!/usr/bin/env python3
"""
Gestionnaire de configuration centralisé
Permet de définir l'URL cible (localhost ou ngrok) au démarrage
"""

import os
import json
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_FILE = "target_config.json"


def save_config(url):
    """Sauvegarde la configuration"""
    config = {
        "target_url": url,
        "login_endpoint": f"{url}/login",
        "data_endpoint": f"{url}/data",
        "base_url": url
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config


def load_config():
    """Charge la configuration existante"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None


def get_target_url():
    """Demande et configure l'URL cible"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║         🎯 CONFIGURATION DE LA CIBLE             ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    # Vérifier si une config existe
    existing_config = load_config()
    
    if existing_config:
        print(f"{Fore.YELLOW}[*] Configuration existante détectée:{Style.RESET_ALL}")
        print(f"    URL: {existing_config['target_url']}")
        
        use_existing = input(f"\n{Fore.CYAN}Utiliser cette configuration ? (o/n): {Style.RESET_ALL}")
        
        if use_existing.lower() in ['o', 'oui', 'y', 'yes']:
            print(f"{Fore.GREEN}[✓] Configuration chargée{Style.RESET_ALL}")
            return existing_config
    
    # Demander le type d'URL
    print(f"\n{Fore.WHITE}Sélectionnez le type de cible:")
    print("1. Localhost (http://localhost)")
    print("2. Ngrok (URL personnalisée)")
    print("3. Autre URL{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-3): {Style.RESET_ALL}")
    
    if choice == "1":
        url = "http://localhost"
    elif choice == "2":
        print(f"\n{Fore.YELLOW}[!] Entrez l'URL Ngrok complète{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Exemple: https://1234-5678-abcd.ngrok-free.app{Style.RESET_ALL}")
        url = input(f"\n{Fore.CYAN}URL Ngrok: {Style.RESET_ALL}").strip()
        
        # Retirer le / final si présent
        url = url.rstrip('/')
        
        # Vérifier le format
        if not url.startswith('http'):
            print(f"{Fore.RED}[✗] URL invalide, ajout de https://{Style.RESET_ALL}")
            url = f"https://{url}"
    else:
        url = input(f"\n{Fore.CYAN}URL cible: {Style.RESET_ALL}").strip().rstrip('/')
        
        if not url.startswith('http'):
            url = f"https://{url}"
    
    # Tester la connexion
    print(f"\n{Fore.CYAN}[*] Test de connexion à {url}...{Style.RESET_ALL}")
    
    import requests
    try:
        response = requests.get(url, timeout=10)
        print(f"{Fore.GREEN}[✓] Connexion réussie ! (Status: {response.status_code}){Style.RESET_ALL}")
        
        # Sauvegarder la config
        config = save_config(url)
        print(f"{Fore.GREEN}[✓] Configuration sauvegardée dans {CONFIG_FILE}{Style.RESET_ALL}")
        
        return config
        
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[✗] Impossible de se connecter à {url}")
        print(f"[✗] Vérifiez que le serveur est en ligne{Style.RESET_ALL}")
        
        retry = input(f"\n{Fore.YELLOW}Utiliser quand même cette URL ? (o/n): {Style.RESET_ALL}")
        if retry.lower() in ['o', 'oui', 'y', 'yes']:
            return save_config(url)
        else:
            return get_target_url()  # Recommencer
    
    except Exception as e:
        print(f"{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")
        return get_target_url()


def display_config():
    """Affiche la configuration actuelle"""
    config = load_config()
    
    if not config:
        print(f"{Fore.YELLOW}[!] Aucune configuration trouvée{Style.RESET_ALL}")
        return
    
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║         📋 CONFIGURATION ACTUELLE                ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}URL Cible: {Fore.GREEN}{config['target_url']}{Style.RESET_ALL}
{Fore.WHITE}Endpoint Login: {Fore.GREEN}{config['login_endpoint']}{Style.RESET_ALL}
{Fore.WHITE}Endpoint Data: {Fore.GREEN}{config['data_endpoint']}{Style.RESET_ALL}
""")


def reset_config():
    """Supprime la configuration"""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"{Fore.GREEN}[✓] Configuration supprimée{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Aucune configuration à supprimer{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        config = get_target_url()
        display_config()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Configuration annulée{Style.RESET_ALL}")