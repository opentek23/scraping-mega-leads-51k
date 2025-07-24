#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE MEGA - 17,800 LEADS AUTOMATIQUE
Scrape 8 types de cibles dans 6 pays africains
Optimisé pour GitHub Actions avec anti-détection
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os
import urllib.parse
from datetime import datetime, timezone
import logging

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AfriqueScrapingMega:
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        
        # Headers rotatifs réalistes
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0'
        ]
        
        # Configuration détaillée Afrique
        self.config = {
            "pays": {
                "nigeria": {
                    "villes": ["Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan"],
                    "codes": ["Nigeria", "NG", "Nigerian"],
                    "multiplicateur": 1.8,  # Plus gros marché
                    "priorite": 1
                },
                "south_africa": {
                    "villes": ["Cape Town", "Johannesburg", "Durban", "Pretoria"],
                    "codes": ["South Africa", "ZA", "South African"],
                    "multiplicateur": 1.5,
                    "priorite": 2
                },
                "kenya": {
                    "villes": ["Nairobi", "Mombasa", "Kisumu", "Nakuru"],
                    "codes": ["Kenya", "KE", "Kenyan"],
                    "multiplicateur": 1.3,
                    "priorite": 3
                },
                "ghana": {
                    "villes": ["Accra", "Kumasi", "Tamale", "Cape Coast"],
                    "codes": ["Ghana", "GH", "Ghanaian"],
                    "multiplicateur": 1.2,
                    "priorite": 4
                },
                "morocco": {
                    "villes": ["Casablanca", "Rabat", "Marrakech", "Fes"],
                    "codes": ["Morocco", "MA", "Moroccan"],
                    "multiplicateur": 1.1,
                    "priorite": 5
                },
                "egypt": {
                    "villes": ["Cairo", "Alexandria", "Giza", "Luxor"],
                    "codes": ["Egypt", "EG", "Egyptian"],
                    "multiplicateur": 1.1,
                    "priorite": 6
                }
            },
            
            "cibles": {
                "entrepreneurs": {
                    "titres": [
                        "CEO", "Founder", "Co-founder", "Managing Director",
                        "Entrepreneur", "Business Owner", "Startup Founder",
                        "Executive Director", "President"
                    ],
                    "keywords": [
                        "startup founder", "entrepreneur", "business owner",
                        "tech entrepreneur", "social entrepreneur", "innovation",
                        "venture", "startup CEO"
                    ],
                    "sites": ["linkedin.com", "crunchbase.com", "angel.co"],
                    "objectif": 2700,
                    "priorite": 1
                },
                
                "consultants": {
                    "titres": [
                        "Management Consultant", "Business Consultant", "Strategy Advisor",
                        "Digital Consultant", "Financial Advisor", "HR Consultant",
                        "Consulting Director", "Senior Consultant"
                    ],
                    "keywords": [
                        "consulting", "strategy", "advisory", "transformation",
                        "business consultant", "management consultant",
                        "digital transformation"
                    ],
                    "sites": ["linkedin.com"],
                    "objectif": 2200,
                    "priorite": 2
                },
                
                "managers": {
                    "titres": [
                        "Country Manager", "Regional Manager", "Operations Manager",
                        "General Manager", "Investment Manager", "Portfolio Manager",
                        "Business Development Manager", "Sales Manager"
                    ],
                    "keywords": [
                        "manager", "director", "investment", "operations",
                        "country manager", "regional director", "business development"
                    ],
                    "sites": ["linkedin.com"],
                    "objectif": 2500,
                    "priorite": 3
                },
                
                "createurs": {
                    "titres": [
                        "Content Creator", "Influencer", "Digital Creator",
                        "Brand Ambassador", "Social Media Manager", "Creator"
                    ],
                    "keywords": [
                        "influencer", "creator", "content", "digital creator",
                        "social media", "brand ambassador", "content marketing"
                    ],
                    "sites": ["instagram.com", "twitter.com", "tiktok.com", "youtube.com"],
                    "objectif": 3500,
                    "priorite": 4
                },
                
                "personnalites": {
                    "titres": [
                        "Public Figure", "Celebrity", "Author", "Speaker",
                        "Activist", "Leader", "Thought Leader", "Expert"
                    ],
                    "keywords": [
                        "public figure", "celebrity", "author", "speaker",
                        "leader", "activist", "thought leader", "expert"
                    ],
                    "sites": ["twitter.com", "linkedin.com", "instagram.com"],
                    "objectif": 1200,
                    "priorite": 5
                },
                
                "entreprises": {
                    "types": [
                        "Technology Company", "Fintech", "E-commerce",
                        "Manufacturing", "Agriculture", "Healthcare",
                        "Education", "Energy", "Consulting Firm"
                    ],
                    "keywords": [
                        "company", "corporation", "enterprise", "business",
                        "tech company", "fintech", "startup", "firm"
                    ],
                    "sites": ["linkedin.com", "crunchbase.com"],
                    "objectif": 2000,
                    "priorite": 6
                },
                
                "artistes": {
                    "types": [
                        "Visual Artist", "Digital Artist", "Painter",
                        "Sculptor", "Designer", "Creative Director", "Artist"
                    ],
                    "keywords": [
                        "artist", "art", "creative", "design", "painter",
                        "visual artist", "digital artist", "creative director"
                    ],
                    "sites": ["instagram.com", "behance.net", "twitter.com"],
                    "objectif": 1500,
                    "priorite": 7
                },
                
                "musiciens": {
                    "genres": [
                        "Afrobeats", "Highlife", "Amapiano", "Bongo Flava",
                        "Hip Hop", "R&B", "Gospel", "Traditional", "Afropop"
                    ],
                    "keywords": [
                        "musician", "singer", "producer", "DJ", "artist",
                        "afrobeats", "music producer", "recording artist",
                        "afropop", "amapiano"
                    ],
                    "sites": ["instagram.com", "twitter.com", "soundcloud.com", "spotify.com"],
                    "objectif": 2200,
                    "priorite": 8
                }
            }
        }
        
        # Variables d'environnement
        self.target_leads = int(os.environ.get('TARGET_LEADS', '1500'))
        self.test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        
        logger.info(f"🎯 Target leads: {self.target_leads}")
        logger.info(f"🧪 Test mode: {self.test_mode}")
        logger.info(f"🔢 Run number: {self.run_number}")
    
    def get_random_headers(self):
        """Headers rotatifs pour éviter détection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def generate_search_queries(self, cible, pays):
        """Génère requêtes optimisées par cible et pays"""
        queries = []
        
        cible_config = self.config["cibles"][cible]
        pays_config = self.config["pays"][pays]
        
        # Requêtes titre + lieu + site
        for titre in cible_config["titres"][:4]:  # Top 4 titres
            for ville in pays_config["villes"][:3]:  # Top 3 villes
                for site in cible_config["sites"][:2]:  # Top 2 sites
                    query = f'"{titre}" "{ville}" site:{site}'
                    queries.append(query)
        
        # Requêtes keyword + pays + site
        for keyword in cible_config["keywords"][:4]:
            for code in pays_config["codes"][:2]:
                for site in cible_config["sites"][:2]:
                    query = f'{keyword} "{code}" site:{site}'
                    queries.append(query)
        
        # Requêtes spécialisées par cible
        if cible == "musiciens":
            for genre in cible_config["genres"][:3]:
                for code in pays_config["codes"][:2]:
                    query = f'"{genre}" artist "{code}" site:instagram.com'
                    queries.append(query)
        
        elif cible == "createurs":
            social_terms = ["influencer", "content creator", "digital creator"]
            for term in social_terms:
                for code in pays_config["codes"][:2]:
                    query = f'"{term}" "{code}" site:instagram.com'
                    queries.append(query)
        
        # Limiter nombre de requêtes en mode test
        max_queries = 3 if self.test_mode else 20
        return queries[:max_queries]
    
    def scrape_google_search(self, query, max_results=100):
        """Scrape Google avec anti-détection avancée"""
        results = []
        
        try:
            # Headers rotatifs
            self.session.headers.update(self.get_random_headers())
            
            # Délai initial
            time.sleep(random.uniform(1, 3))
            
            # Pagination Google (maximum 5 pages)
            max_pages = 2 if self.test_mode else 5
            
            for page in range(max_pages):
                start = page * 10
                
                # Construction URL Google
                params = {
                    'q': query,
                    'start': start,
                    'num': 10,
                    'hl': 'en',
                    'gl': 'us'
                }
                
                search_url = "https://www.google.com/search?" + urllib.parse.urlencode(params)
                
                # Requête avec timeout
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 429:
                    logger.warning("⚠️ Rate limit détecté, pause longue...")
                    time.sleep(random.uniform(60, 120))
                    continue
                
                if response.status_code != 200:
                    logger.warning(f"⚠️ Status {response.status_code} pour: {query}")
                    continue
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraction liens
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    
                    # Nettoyer URL Google
                    if href.startswith('/url?q='):
                        href = href.split('/url?q=')[1].split('&')[0]
                        href = urllib.parse.unquote(href)
                    
                    # Filtrer liens pertinents
                    relevant_sites = [
                        'linkedin.com/in/', 'instagram.com/', 'twitter.com/',
                        'crunchbase.com/', 'angel.co/', 'behance.net/',
                        'soundcloud.com/', 'spotify.com/', 'tiktok.com/'
                    ]
                    
                    if any(site in href for site in relevant_sites):
                        # Extraire texte du lien
                        link_text = link.get_text(strip=True)
                        
                        result = {
                            'url': href,
                            'text': link_text[:300],  # Limiter texte
                            'query': query,
                            'found_at': datetime.now(timezone.utc).isoformat(),
                            'page': page + 1,
                            'search_engine': 'google'
                        }
                        results.append(result)
                        
                        if len(results) >= max_results:
                            break
                
                # Délai entre pages
                time.sleep(random.uniform(3, 8))
                
                if len(results) >= max_results:
                    break
        
        except Exception as e:
            logger.error(f"❌ Erreur scraping '{query}': {e}")
        
        return results[:max_results]
    
    def scrape_cible_pays(self, cible, pays):
        """Scrape une cible spécifique dans un pays"""
        logger.info(f"🎯 Scraping {cible} - {pays}")
        
        queries = self.generate_search_queries(cible, pays)
        cible_prospects = []
        
        # Calcul objectif ajusté
        objectif_base = self.config["cibles"][cible]["objectif"] // 6  # Répartir sur 6 pays
        multiplicateur = self.config["pays"][pays]["multiplicateur"]
        objectif_ajuste = int(objectif_base * multiplicateur)
        
        # Mode test = objectif réduit
        if self.test_mode:
            objectif_ajuste = min(objectif_ajuste, 20)
        
        logger.info(f"  🎯 Objectif ajusté: {objectif_ajuste} prospects")
        
        for i, query in enumerate(queries):
            if len(cible_prospects) >= objectif_ajuste:
                break
                
            logger.info(f"  🔍 Query {i+1}/{len(queries)}: {query[:60]}...")
            
            # Scraping avec gestion d'erreur
            try:
                results = self.scrape_google_search(query, max_results=50)
                
                for result in results:
                    prospect = {
                        'url': result['url'],
                        'text': result['text'],
                        'cible': cible,
                        'pays': pays,
                        'source_query': query,
                        'platform': self.extract_platform(result['url']),
                        'found_at': result['found_at'],
                        'region': 'afrique',
                        'page': result.get('page', 1),
                        'run_number': self.run_number
                    }
                    cible_prospects.append(prospect)
                
                logger.info(f"📋 Summary sauvé: {summary_file}")
                
                # Affichage résultats
                print(f"\n💾 RÉSULTATS SAUVEGARDÉS")
                print(f"📊 Total prospects: {len(prospects):,}")
                print(f"🎯 Objectif 17,800: {summary['progress_percent']:.1f}%")
                print(f"📁 Fichier principal: {csv_file}")
                
                # GitHub Actions outputs
                print(f"::set-output name=prospects_count::{len(prospects)}")
                print(f"::set-output name=csv_file::{csv_file}")
                print(f"::set-output name=progress::{summary['progress_percent']}")
                print(f"::set-output name=success::true")
                
                return summary
                
            else:
                # Aucun prospect trouvé
                summary = {
                    'run_number': self.run_number,
                    'timestamp': timestamp,
                    'total_prospects': 0,
                    'error': 'Aucun prospect trouvé',
                    'success': False
                }
                
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2)
                
                logger.warning("⚠️ Aucun prospect trouvé")
                print("::set-output name=prospects_count::0")
                print("::set-output name=success::false")
                
                return summary
                
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            
            error_summary = {
                'run_number': self.run_number,
                'timestamp': timestamp,
                'error': str(e),
                'success': False
            }
            
            try:
                with open(f"data/error_run{self.run_number}_{timestamp}.json", 'w') as f:
                    json.dump(error_summary, f, indent=2)
            except:
                pass
            
            print("::set-output name=success::false")
            return error_summary

def main():
    """Fonction principale pour GitHub Actions"""
    print("🚀 GITHUB ACTIONS - SCRAPING AFRIQUE MEGA")
    print("🎯 Objectif: Jusqu'à 1,500 prospects par run")
    print("🌍 Cibles: 8 types dans 6 pays africains")
    print("=" * 70)
    
    try:
        # Initialiser scraper
        scraper = AfriqueScrapingMega()
        
        # Information de démarrage
        logger.info(f"🚀 Démarrage run #{scraper.run_number}")
        logger.info(f"🎯 Target leads: {scraper.target_leads}")
        logger.info(f"🧪 Test mode: {scraper.test_mode}")
        
        # Scraping complet
        prospects, stats = scraper.scrape_all_afrique()
        
        # Sauvegarde
        summary = scraper.save_results(prospects, stats)
        
        # Résultat final
        if summary.get('success', False):
            print(f"\n🎉 SCRAPING AFRIQUE TERMINÉ AVEC SUCCÈS !")
            print(f"📊 {summary['total_prospects']} prospects trouvés")
            print(f"📈 Progression: {summary.get('progress_percent', 0):.1f}% vers 17,800")
        else:
            print(f"\n⚠️ SCRAPING TERMINÉ AVEC ERREURS")
            print(f"❌ Erreur: {summary.get('error', 'Inconnue')}")
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        print(f"❌ ERREUR FATALE: {e}")
        print("::set-output name=success::false")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    main()"    ✅ +{len(results)} prospects (Total: {len(cible_prospects)})")
                
            except Exception as e:
                logger.error(f"    ❌ Erreur query: {e}")
            
            # Délai entre queries
            time.sleep(random.uniform(4, 10))
        
        logger.info(f"  🎉 {cible} {pays}: {len(cible_prospects)} prospects trouvés")
        return cible_prospects
    
    def extract_platform(self, url):
        """Extrait la plateforme de l'URL"""
        platforms = {
            'linkedin.com': 'linkedin',
            'instagram.com': 'instagram',
            'twitter.com': 'twitter',
            'crunchbase.com': 'crunchbase',
            'angel.co': 'angellist',
            'behance.net': 'behance',
            'soundcloud.com': 'soundcloud',
            'spotify.com': 'spotify',
            'tiktok.com': 'tiktok',
            'youtube.com': 'youtube'
        }
        
        for domain, platform in platforms.items():
            if domain in url:
                return platform
        
        return 'other'
    
    def remove_duplicates(self, prospects):
        """Supprime les doublons basés sur l'URL"""
        seen_urls = set()
        unique_prospects = []
        
        for prospect in prospects:
            url = prospect['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_prospects.append(prospect)
        
        removed = len(prospects) - len(unique_prospects)
        if removed > 0:
            logger.info(f"🧹 Supprimé {removed} doublons")
        
        return unique_prospects
    
    def scrape_all_afrique(self):
        """Scrape complet Afrique - Optimisé pour GitHub Actions"""
        logger.info("🌍 DÉMARRAGE SCRAPING AFRIQUE COMPLET")
        logger.info("=" * 60)
        
        all_prospects = []
        stats = {
            'start_time': datetime.now(timezone.utc).isoformat(),
            'run_number': self.run_number,
            'target_leads': self.target_leads,
            'test_mode': self.test_mode,
            'by_cible': {},
            'by_pays': {},
            'by_platform': {},
            'queries_executed': 0
        }
        
        # Ordre prioritaire des cibles (entrepreneurs en premier)
        cibles_ordered = sorted(
            self.config["cibles"].keys(),
            key=lambda x: self.config["cibles"][x]["priorite"]
        )
        
        # Ordre prioritaire des pays (Nigeria en premier)
        pays_ordered = sorted(
            self.config["pays"].keys(),
            key=lambda x: self.config["pays"][x]["priorite"]
        )
        
        total_processed = 0
        
        for cible in cibles_ordered:
            stats['by_cible'][cible] = 0
            
            for pays in pays_ordered:
                if pays not in stats['by_pays']:
                    stats['by_pays'][pays] = 0
                
                # Vérifier si on a atteint l'objectif
                if total_processed >= self.target_leads:
                    logger.info(f"🎯 Objectif {self.target_leads} atteint, arrêt du scraping")
                    break
                
                # Scrape cible + pays
                try:
                    prospects = self.scrape_cible_pays(cible, pays)
                    all_prospects.extend(prospects)
                    
                    # Update stats
                    stats['by_cible'][cible] += len(prospects)
                    stats['by_pays'][pays] += len(prospects)
                    total_processed += len(prospects)
                    
                    for prospect in prospects:
                        platform = prospect['platform']
                        stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
                    
                except Exception as e:
                    logger.error(f"❌ Erreur {cible} {pays}: {e}")
                
                # Délai entre pays
                time.sleep(random.uniform(10, 20))
            
            logger.info(f"✅ {cible}: {stats['by_cible'][cible]} prospects")
            
            # Arrêter si objectif atteint
            if total_processed >= self.target_leads:
                break
            
            # Délai entre cibles
            time.sleep(random.uniform(15, 30))
        
        # Suppression des doublons
        all_prospects = self.remove_duplicates(all_prospects)
        
        stats['end_time'] = datetime.now(timezone.utc).isoformat()
        stats['total_prospects'] = len(all_prospects)
        stats['total_unique'] = len(all_prospects)
        
        logger.info(f"\n🎉 SCRAPING TERMINÉ!")
        logger.info(f"📊 Total prospects uniques: {len(all_prospects):,}")
        
        return all_prospects, stats
    
    def save_results(self, prospects, stats):
        """Sauvegarde optimisée pour GitHub Actions"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Créer dossier data
        os.makedirs('data', exist_ok=True)
        
        # Noms de fichiers avec run number
        csv_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.csv"
        json_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.json"
        stats_file = f"data/stats_afrique_run{self.run_number}_{timestamp}.json"
        summary_file = f"data/summary_afrique_run{self.run_number}_{timestamp}.json"
        
        try:
            # DataFrame avec gestion d'erreur
            if prospects:
                df = pd.DataFrame(prospects)
                
                # Sauvegarde CSV
                df.to_csv(csv_file, index=False, encoding='utf-8')
                logger.info(f"💾 CSV sauvé: {csv_file}")
                
                # Sauvegarde JSON
                df.to_json(json_file, orient='records', indent=2)
                logger.info(f"💾 JSON sauvé: {json_file}")
                
                # Statistiques détaillées
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
                logger.info(f"📊 Stats sauvées: {stats_file}")
                
                # Summary pour GitHub
                summary = {
                    'run_number': self.run_number,
                    'timestamp': timestamp,
                    'total_prospects': len(prospects),
                    'target_17800': 17800,
                    'progress_percent': round((len(prospects) / 17800) * 100, 2),
                    'test_mode': self.test_mode,
                    'files': {
                        'csv': csv_file,
                        'json': json_file,
                        'stats': stats_file
                    },
                    'top_stats': {
                        'top_cible': max(stats['by_cible'].items(), key=lambda x: x[1]) if stats['by_cible'] else ('none', 0),
                        'top_pays': max(stats['by_pays'].items(), key=lambda x: x[1]) if stats['by_pays'] else ('none', 0),
                        'top_platform': max(stats['by_platform'].items(), key=lambda x: x[1]) if stats['by_platform'] else ('none', 0)
                    },
                    'success': True
                }
                
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2, ensure_ascii=False)
                
                # Fichier latest pour monitoring
                with open('data/summary_latest.json', 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2, ensure_ascii=False)
                
                logger.info(f
