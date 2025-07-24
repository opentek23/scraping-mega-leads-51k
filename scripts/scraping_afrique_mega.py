#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE MEGA - VERSION SANS PANDAS
Script ultra-léger pour éviter les conflits de dépendances
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
import os
from datetime import datetime, timezone
import urllib.parse

class AfriqueScrapingMega:
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        
        # Headers réalistes
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        
        # Configuration
        self.target_leads = int(os.environ.get('TARGET_LEADS', '100'))
        self.test_mode = os.environ.get('TEST_MODE', 'true').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        
        print(f"🎯 Target leads: {self.target_leads}")
        print(f"🧪 Test mode: {self.test_mode}")
        print(f"🔢 Run number: {self.run_number}")
        
        # Requêtes optimisées Afrique
        self.search_queries = [
            'CEO startup Nigeria site:linkedin.com',
            'founder Kenya business site:linkedin.com',
            'entrepreneur Ghana tech site:linkedin.com',
            'consultant strategy "South Africa" site:linkedin.com',
            'business advisor Nigeria site:linkedin.com',
            'afrobeats artist Nigeria site:instagram.com',
            'musician Ghana site:twitter.com',
            'content creator "South Africa" site:instagram.com',
            'influencer Lagos Nigeria site:instagram.com',
            'tech entrepreneur Kenya site:linkedin.com',
            'startup CEO Morocco site:linkedin.com',
            'business owner Egypt site:linkedin.com'
        ]
    
    def scrape_google_search(self, query, max_results=30):
        """Scrape Google simplifié"""
        results = []
        
        try:
            print(f"  🔍 {query[:60]}...")
            
            # URL de recherche
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
            
            # Requête
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 429:
                print(f"    ⚠️ Rate limit, pause...")
                time.sleep(30)
                return results
            
            if response.status_code != 200:
                print(f"    ⚠️ Status {response.status_code}")
                return results
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction des liens
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                # Nettoyer URL Google
                if href.startswith('/url?q='):
                    href = href.split('/url?q=')[1].split('&')[0]
                    href = urllib.parse.unquote(href)
                
                # Filtrer les plateformes pertinentes
                relevant_platforms = [
                    'linkedin.com/in/', 'instagram.com/', 'twitter.com/',
                    'crunchbase.com/', 'angel.co/'
                ]
                
                if any(platform in href for platform in relevant_platforms):
                    link_text = link.get_text(strip=True)
                    
                    # Éviter les liens trop courts ou vides
                    if len(link_text) > 5:
                        result = {
                            'url': href,
                            'text': link_text[:300],
                            'query': query,
                            'found_at': datetime.now(timezone.utc).isoformat()
                        }
                        results.append(result)
                        
                        if len(results) >= max_results:
                            break
            
            print(f"    ✅ {len(results)} liens trouvés")
            
            # Délai anti-détection
            time.sleep(random.uniform(4, 8))
            
        except Exception as e:
            print(f"    ❌ Erreur: {str(e)[:100]}")
        
        return results
    
    def classify_prospect(self, query, url, text):
        """Classification automatique des prospects"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Déterminer la plateforme
        if 'linkedin.com' in url:
            platform = 'linkedin'
        elif 'instagram.com' in url:
            platform = 'instagram'
        elif 'twitter.com' in url:
            platform = 'twitter'
        elif 'crunchbase.com' in url:
            platform = 'crunchbase'
        else:
            platform = 'other'
        
        # Déterminer le type de cible
        if any(word in query_lower for word in ['ceo', 'founder', 'entrepreneur']):
            target_type = 'entrepreneur'
        elif any(word in query_lower for word in ['consultant', 'advisor']):
            target_type = 'consultant'
        elif any(word in query_lower for word in ['musician', 'artist', 'afrobeats']):
            target_type = 'musicien'
        elif any(word in query_lower for word in ['creator', 'influencer']):
            target_type = 'createur'
        else:
            target_type = 'other'
        
        # Déterminer le pays
        if any(word in query_lower for word in ['nigeria', 'lagos']):
            country = 'nigeria'
        elif 'kenya' in query_lower:
            country = 'kenya'
        elif 'ghana' in query_lower:
            country = 'ghana'
        elif 'south africa' in query_lower:
            country = 'south_africa'
        elif 'morocco' in query_lower:
            country = 'morocco'
        elif 'egypt' in query_lower:
            country = 'egypt'
        else:
            country = 'africa_other'
        
        return platform, target_type, country
    
    def scrape_all_queries(self):
        """Scraping complet"""
        print("\n🌍 DÉMARRAGE SCRAPING AFRIQUE")
        print("=" * 50)
        
        all_prospects = []
        
        # Limiter en mode test
        queries_to_use = self.search_queries[:4] if self.test_mode else self.search_queries
        
        for i, query in enumerate(queries_to_use):
            print(f"\n🎯 Query {i+1}/{len(queries_to_use)}")
            
            # Scraping
            results = self.scrape_google_search(query, max_results=25 if self.test_mode else 40)
            
            # Traitement
            for result in results:
                platform, target_type, country = self.classify_prospect(
                    query, result['url'], result['text']
                )
                
                prospect = {
                    'url': result['url'],
                    'text': result['text'],
                    'platform': platform,
                    'target_type': target_type,
                    'country': country,
                    'source_query': query,
                    'found_at': result['found_at'],
                    'region': 'afrique',
                    'run_number': self.run_number
                }
                all_prospects.append(prospect)
            
            # Vérifier objectif
            if len(all_prospects) >= self.target_leads:
                print(f"🎯 Objectif {self.target_leads} atteint!")
                break
            
            # Délai entre requêtes
            time.sleep(random.uniform(8, 15))
        
        # Suppression des doublons
        unique_prospects = self.remove_duplicates(all_prospects)
        
        print(f"\n🎉 SCRAPING TERMINÉ!")
        print(f"📊 Total: {len(all_prospects)} → {len(unique_prospects)} uniques")
        
        return unique_prospects
    
    def remove_duplicates(self, prospects):
        """Supprime les doublons par URL"""
        seen_urls = set()
        unique = []
        
        for prospect in prospects:
            url = prospect['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique.append(prospect)
        
        removed = len(prospects) - len(unique)
        if removed > 0:
            print(f"🧹 {removed} doublons supprimés")
        
        return unique
    
    def calculate_stats(self, prospects):
        """Calcule les statistiques"""
        stats = {
            'total': len(prospects),
            'by_platform': {},
            'by_target_type': {},
            'by_country': {}
        }
        
        for prospect in prospects:
            # Stats par plateforme
            platform = prospect['platform']
            stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
            
            # Stats par type
            target_type = prospect['target_type']
            stats['by_target_type'][target_type] = stats['by_target_type'].get(target_type, 0) + 1
            
            # Stats par pays
            country = prospect['country']
            stats['by_country'][country] = stats['by_country'].get(country, 0) + 1
        
        return stats
    
    def save_results(self, prospects):
        """Sauvegarde en CSV et JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Créer dossier
        os.makedirs('data', exist_ok=True)
        
        # Noms de fichiers
        csv_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.csv"
        json_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.json"
        stats_file = f"data/stats_afrique_run{self.run_number}_{timestamp}.json"
        
        try:
            if prospects:
                # Sauvegarde CSV
                with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'url', 'text', 'platform', 'target_type', 'country',
                        'source_query', 'found_at', 'region', 'run_number'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(prospects)
                
                print(f"💾 CSV sauvé: {csv_file}")
                
                # Sauvegarde JSON
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(prospects, f, indent=2, ensure_ascii=False)
                
                print(f"💾 JSON sauvé: {json_file}")
                
                # Statistiques
                stats = self.calculate_stats(prospects)
                stats.update({
                    'run_number': self.run_number,
                    'timestamp': timestamp,
                    'test_mode': self.test_mode,
                    'target_leads': self.target_leads
                })
                
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
                
                print(f"📊 Stats sauvées: {stats_file}")
                
                # Affichage résultats
                print(f"\n📈 RÉSULTATS DÉTAILLÉS:")
                print(f"  📊 Total prospects: {stats['total']}")
                print(f"  🌐 Plateformes: {stats['by_platform']}")
                print(f"  🎯 Types: {stats['by_target_type']}")
                print(f"  🌍 Pays: {stats['by_country']}")
                
                return True
            else:
                print("⚠️ Aucun prospect trouvé")
                return False
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False

def main():
    """Fonction principale pour GitHub Actions"""
    print("🚀 SCRAPING AFRIQUE - VERSION OPTIMISÉE")
    print("=" * 60)
    
    try:
        # Initialiser
        scraper = AfriqueScrapingMega()
        
        # Scraper
        prospects = scraper.scrape_all_queries()
        
        # Sauvegarder
        success = scraper.save_results(prospects)
        
        if success and prospects:
            print(f"\n🎉 SUCCÈS TOTAL!")
            print(f"📊 {len(prospects)} prospects africains collectés")
            print(f"📁 Fichiers CSV et JSON prêts à télécharger")
        else:
            print(f"\n⚠️ Terminé avec peu ou pas de résultats")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR FATALE: {e}")
        return False

if __name__ == "__main__":
    main()
