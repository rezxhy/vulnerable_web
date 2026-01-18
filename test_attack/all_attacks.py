#!/usr/bin/env python3
"""
Menu principal pour toutes les attaques
Permet de lancer n'importe quelle attaque depuis un seul point
"""

import subprocess
import sys
from colorama import Fore, Style, init

TARGET = "http://localhost"

init(autoreset=True)

def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ⚠️  SIMULATEUR D'ATTAQUES - CYBERSÉCURITÉ PÉDAGOGIQUE      ║
║                                                               ║
║          UTILISEZ UNIQUEMENT SUR VOS PROPRES SYSTÈMES         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.CYAN}📚 Objectif pédagogique:{Style.RESET_ALL}
{Fore.WHITE}Ce simulateur permet de comprendre et démontrer différentes
vulnérabilités de sécurité web courantes.{Style.RESET_ALL}

{Fore.YELLOW}⚠️  Avertissement:{Style.RESET_ALL}
{Fore.RED}L'utilisation de ces outils sur des systèmes dont vous n'êtes
pas propriétaire est ILLÉGALE et peut entraîner des poursuites.{Style.RESET_ALL}
""")


def show_vulnerabilities():
    """Affiche les vulnérabilités de l'application"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║            🔍 VULNÉRABILITÉS DE L'APPLICATION                ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}Votre application vulnérable contient:{Style.RESET_ALL}

{Fore.RED}1. 🔨 Brute Force{Style.RESET_ALL}
   {Fore.YELLOW}• Pas de rate limiting
   • Pas de CAPTCHA
   • Pas de blocage après X tentatives
   • Permet tests illimités de mots de passe{Style.RESET_ALL}

{Fore.RED}2. 💉 NoSQL Injection{Style.RESET_ALL}
   {Fore.YELLOW}• Requêtes MongoDB non sanitizées
   • Accepte des objets JSON malveillants
   • Permet bypass de l'authentification
   • Énumération de données possible{Style.RESET_ALL}

{Fore.RED}3. 💥 DDoS / DoS{Style.RESET_ALL}
   {Fore.YELLOW}• Serveur single-threaded
   • Pas de protection contre flood
   • Pas de load balancing
   • Facile à surcharger{Style.RESET_ALL}

{Fore.RED}4. 🕷️  XSS (Cross-Site Scripting){Style.RESET_ALL}
   {Fore.YELLOW}• Pas de sanitisation des inputs
   • Stockage direct dans MongoDB
   • Affichage sans échappement
   • XSS stocké et reflété possibles{Style.RESET_ALL}

{Fore.RED}5. 🔓 Credentials exposés{Style.RESET_ALL}
   {Fore.YELLOW}• MONGO_URI en clair dans docker-compose.yml
   • Mots de passe hardcodés
   • Accès direct à MongoDB possible
   • Pas de chiffrement{Style.RESET_ALL}

{Fore.WHITE}Impact global: {Fore.RED}CRITIQUE{Style.RESET_ALL}
""")


def run_attack(script_name):
    """Lance un script d'attaque"""
    try:
        subprocess.run([sys.executable, script_name])
    except FileNotFoundError:
        print(f"{Fore.RED}[✗] Script {script_name} introuvable{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attaque interrompue{Style.RESET_ALL}")


def quick_pentest():
    """Pentest rapide - teste toutes les vulnérabilités"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║              🎯 PENTEST RAPIDE AUTOMATIQUE                   ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    import requests
    import json
    
    results = []
    
    print(f"{Fore.WHITE}Test 1/5: Vérification de la disponibilité...{Style.RESET_ALL}")
    try:
        r = requests.get(TARGET, timeout=5)
        print(f"{Fore.GREEN}[✓] Application accessible{Style.RESET_ALL}")
        results.append(("Disponibilité", "OK", "green"))
    except:
        print(f"{Fore.RED}[✗] Application inaccessible{Style.RESET_ALL}")
        results.append(("Disponibilité", "ERREUR", "red"))
        return
    
    print(f"\n{Fore.WHITE}Test 2/5: Test NoSQL Injection...{Style.RESET_ALL}")
    try:
        payload = {"username": {"$ne": None}, "password": {"$ne": None}}
        r = requests.post(f"{TARGET}/login", json=payload, timeout=5)
        if r.status_code == 200 and r.json().get('success'):
            print(f"{Fore.RED}[!] VULNÉRABLE à NoSQL Injection{Style.RESET_ALL}")
            results.append(("NoSQL Injection", "VULNÉRABLE", "red"))
        else:
            print(f"{Fore.GREEN}[✓] Protégé contre NoSQL Injection{Style.RESET_ALL}")
            results.append(("NoSQL Injection", "SÉCURISÉ", "green"))
    except:
        print(f"{Fore.YELLOW}[!] Test échoué{Style.RESET_ALL}")
        results.append(("NoSQL Injection", "ERREUR", "yellow"))
    
    print(f"\n{Fore.WHITE}Test 3/5: Test Brute Force (10 tentatives)...{Style.RESET_ALL}")
    import time
    start = time.time()
    attempts = 0
    for i in range(10):
        try:
            r = requests.post(f"{TARGET}/login", 
                            json={"username": "admin", "password": f"test{i}"}, 
                            timeout=2)
            attempts += 1
        except:
            break
    elapsed = time.time() - start
    
    if attempts == 10:
        print(f"{Fore.RED}[!] VULNÉRABLE - Aucun rate limiting ({attempts} tentatives en {elapsed:.2f}s){Style.RESET_ALL}")
        results.append(("Rate Limiting", "ABSENT", "red"))
    else:
        print(f"{Fore.GREEN}[✓] Protection détectée{Style.RESET_ALL}")
        results.append(("Rate Limiting", "PRÉSENT", "green"))
    
    print(f"\n{Fore.WHITE}Test 4/5: Test XSS Reflété...{Style.RESET_ALL}")
    xss_payload = "<script>alert('XSS')</script>"
    try:
        r = requests.post(f"{TARGET}/login", 
                         json={"username": xss_payload, "password": "test"}, 
                         timeout=5)
        if xss_payload in r.text:
            print(f"{Fore.RED}[!] VULNÉRABLE à XSS Reflété{Style.RESET_ALL}")
            results.append(("XSS Reflété", "VULNÉRABLE", "red"))
        else:
            print(f"{Fore.GREEN}[✓] XSS filtré{Style.RESET_ALL}")
            results.append(("XSS Reflété", "SÉCURISÉ", "green"))
    except:
        print(f"{Fore.YELLOW}[!] Test échoué{Style.RESET_ALL}")
        results.append(("XSS Reflété", "ERREUR", "yellow"))
    
    print(f"\n{Fore.WHITE}Test 5/5: Vérification credentials exposés...{Style.RESET_ALL}")
    try:
        with open('../docker-compose.yml', 'r') as f:
            content = f.read()
            if 'MONGO_URI' in content and 'mongodb' in content:
                print(f"{Fore.RED}[!] Credentials MongoDB trouvés dans docker-compose.yml{Style.RESET_ALL}")
                results.append(("Credentials exposés", "TROUVÉS", "red"))
            else:
                print(f"{Fore.GREEN}[✓] Pas de credentials en clair{Style.RESET_ALL}")
                results.append(("Credentials exposés", "SÉCURISÉS", "green"))
    except:
        print(f"{Fore.YELLOW}[!] Fichier non accessible{Style.RESET_ALL}")
        results.append(("Credentials exposés", "INCONNU", "yellow"))
    
    # Rapport final
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                   📊 RAPPORT DE PENTEST                      ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    for test, status, color in results:
        color_code = {"red": Fore.RED, "yellow": Fore.YELLOW, "green": Fore.GREEN}[color]
        print(f"{Fore.WHITE}{test:<25} {color_code}{status:>15}{Style.RESET_ALL}")
    
    vuln_count = sum(1 for _, status, _ in results if status in ["VULNÉRABLE", "ABSENT", "TROUVÉS"])
    
    print(f"\n{Fore.WHITE}Vulnérabilités détectées: {Fore.RED}{vuln_count}/5{Style.RESET_ALL}")
    
    if vuln_count >= 4:
        print(f"{Fore.RED}\n⚠️  NIVEAU DE SÉCURITÉ: CRITIQUE")
        print(f"L'application présente de nombreuses vulnérabilités majeures{Style.RESET_ALL}")
    elif vuln_count >= 2:
        print(f"{Fore.YELLOW}\n⚠️  NIVEAU DE SÉCURITÉ: MOYEN")
        print(f"Plusieurs vulnérabilités nécessitent une correction{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}\n✓ NIVEAU DE SÉCURITÉ: BON")
        print(f"L'application est relativement bien protégée{Style.RESET_ALL}")


def generate_report():
    """Génère un rapport de sécurité"""
    print(f"{Fore.CYAN}[*] Génération du rapport de sécurité...{Style.RESET_ALL}")
    
    report = f"""
╔═══════════════════════════════════════════════════════════════╗
║              RAPPORT DE SÉCURITÉ - APPLICATION WEB           ║
╚═══════════════════════════════════════════════════════════════╝

Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Application: Vulnerable Web App
URL: {TARGET}

══════════════════════════════════════════════════════════════
1. VULNÉRABILITÉS IDENTIFIÉES
══════════════════════════════════════════════════════════════

🔴 CRITIQUE - Brute Force
   • Description: Aucune protection contre les attaques par force brute
   • Impact: Compromission de comptes utilisateurs
   • Recommandation: Implémenter rate limiting (Flask-Limiter)
   
🔴 CRITIQUE - NoSQL Injection
   • Description: Requêtes MongoDB non sanitizées
   • Impact: Bypass authentification, accès non autorisé
   • Recommandation: Valider types des inputs, utiliser ORM

🔴 CRITIQUE - Credentials exposés
   • Description: MONGO_URI en clair dans docker-compose.yml
   • Impact: Accès direct à la base de données
   • Recommandation: Utiliser .env + Docker Secrets

🟠 ÉLEVÉE - XSS (Cross-Site Scripting)
   • Description: Pas de sanitisation des entrées utilisateur
   • Impact: Vol de session, phishing, malware
   • Recommandation: Sanitiser inputs, CSP headers

🟠 ÉLEVÉE - Denial of Service
   • Description: Pas de protection contre flood
   • Impact: Indisponibilité du service
   • Recommandation: Rate limiting, WAF, Load balancing

══════════════════════════════════════════════════════════════
2. SCORE DE SÉCURITÉ
══════════════════════════════════════════════════════════════

Vulnérabilités critiques: 3
Vulnérabilités élevées:   2
Vulnérabilités moyennes:  0
Vulnérabilités faibles:   0

SCORE GLOBAL: 15/100 (CRITIQUE)

══════════════════════════════════════════════════════════════
3. PLAN D'ACTION PRIORITAIRE
══════════════════════════════════════════════════════════════

PRIORITÉ 1 (Urgent):
  ✓ Déplacer MONGO_URI vers .env
  ✓ Valider types des inputs (str uniquement)
  ✓ Implémenter rate limiting

PRIORITÉ 2 (Important):
  ✓ Sanitiser toutes les entrées utilisateur
  ✓ Ajouter CSP headers
  ✓ Hasher les mots de passe (bcrypt)

PRIORITÉ 3 (Recommandé):
  ✓ Implémenter WAF
  ✓ Load balancing
  ✓ Monitoring et alertes

══════════════════════════════════════════════════════════════
4. EXEMPLES DE CODE CORRIGÉ
══════════════════════════════════════════════════════════════

# Rate Limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    ...

# Validation des inputs
if not isinstance(username, str) or not isinstance(password, str):
    return jsonify({{'error': 'Invalid input'}}), 400

# Hachage des mots de passe
from bcrypt import hashpw, gensalt, checkpw
hashed = hashpw(password.encode(), gensalt())

══════════════════════════════════════════════════════════════
Fin du rapport
══════════════════════════════════════════════════════════════
"""
    
    # Sauvegarder le rapport
    filename = f"security_report_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n{Fore.GREEN}[✓] Rapport sauvegardé: {filename}{Style.RESET_ALL}")


def main():
    banner()
    
    while True:
        print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                      MENU PRINCIPAL                          ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}ATTAQUES INDIVIDUELLES:{Style.RESET_ALL}
  1. 🔨 Brute Force Attack
  2. 💉 NoSQL Injection
  3. 💥 DDoS Simulation
  4. 🕷️  XSS Attack
  5. 🔓 Credential Exploitation

{Fore.WHITE}OUTILS:{Style.RESET_ALL}
  6. 🔍 Voir les vulnérabilités
  7. 🎯 Pentest rapide automatique
  8. 📊 Générer rapport de sécurité

  9. ❌ Quitter
""")
        
        choice = input(f"{Fore.CYAN}Votre choix (1-9): {Style.RESET_ALL}")
        
        if choice == "1":
            run_attack("1_brute_force.py")
        elif choice == "2":
            run_attack("2_nosql_injection.py")
        elif choice == "3":
            run_attack("3_ddos_simulation.py")
        elif choice == "4":
            run_attack("4_xss_attack.py")
        elif choice == "5":
            run_attack("5_credential_exploit.py")
        elif choice == "6":
            show_vulnerabilities()
        elif choice == "7":
            quick_pentest()
        elif choice == "8":
            generate_report()
        elif choice == "9":
            print(f"\n{Fore.CYAN}Merci d'avoir utilisé le simulateur d'attaques !{Style.RESET_ALL}")
            print(f"{Fore.WHITE}N'oubliez pas: utilisez ces connaissances de manière éthique.{Style.RESET_ALL}\n")
            break
        else:
            print(f"{Fore.RED}[✗] Choix invalide{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Programme interrompu{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")