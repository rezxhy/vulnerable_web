#!/usr/bin/env python3
"""
Scan Nmap automatisé sur URL ngrok - version corrigée 2025/2026
Nettoie correctement l'URL avant de la passer à nmap
"""

import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

CONFIG_FILE = "target_config.json"


def load_ngrok_url():
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        print(f"Erreur : {CONFIG_FILE} introuvable")
        print("Exécute d'abord ton script config.py")
        sys.exit(1)

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        url = config.get("target_url", "").strip()
        if not url:
            print("Aucune URL trouvée dans la configuration")
            sys.exit(1)
        return url
    except Exception as e:
        print(f"Erreur lecture config : {e}")
        sys.exit(1)


def clean_target_for_nmap(target: str) -> str:
    """
    Transforme https://xxx.ngrok-free.app → xxx.ngrok-free.app
    Gère http, https, port optionnel, chemin éventuel
    """
    if target.startswith(('http://', 'https://')):
        parsed = urlparse(target)
        hostname = parsed.hostname
        if hostname:
            return hostname
        # fallback si urlparse échoue bizarrement
        target = target.split('://', 1)[-1]

    # enlève chemin et port s'il reste
    target = target.split('/', 1)[0].split(':', 1)[0]
    return target.strip()


def run_nmap_scan(target: str):
    clean_target = clean_target_for_nmap(target)
    print(f"URL originale  : {target}")
    print(f"Cible pour Nmap : {clean_target}\n")

    # Commande Nmap - adaptée pour ngrok http(s)
    cmd = [
        "nmap",
        "-Pn",                # pas de ping (ngrok bloque souvent)
        "-sV",                # détection de version/service
        "--version-light",    # plus rapide
        "-p", "80,443,8080,8443",  # ports les plus probables
        "--script", "http-title,http-server-header",
        clean_target
    ]

    print("Commande :", " ".join(cmd))
    print("-" * 70)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        print(result.stdout.strip())

        if result.stderr:
            print("\n--- STDERR ---")
            print(result.stderr.strip())

        print(f"\nRetour code : {result.returncode}")

    except FileNotFoundError:
        print("ERREUR : nmap n'est pas installé ou pas dans le PATH")
        print("→ sudo apt update && sudo apt install nmap")
        sys.exit(1)
    except PermissionError:
        print("ERREUR : Permission denied sur nmap")
        print("Essaie avec : sudo python3 ton_script.py")
        print("Ou ajoute --unprivileged à la commande nmap")
        sys.exit(1)


def main():
    print("=" * 70)
    print("   Nmap Ngrok Scanner - version corrigée")
    print("=" * 70)

    target_url = load_ngrok_url()

    print(f"\nDate : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_nmap_scan(target_url)

    print("\nNote importante :")
    print("→ Avec ngrok http/https → tu verras presque toujours seulement 443 (ou 80)")
    print("→ Pour scanner d'autres ports → utilise ngrok tcp xxxx")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrompu (Ctrl+C)")