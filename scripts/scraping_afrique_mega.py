#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE MEGA - VERSION CORRIGÉE
Script simplifié et fonctionnel pour GitHub Actions
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
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
        
        # Configuration simplifiée
        self.target_leads = int(os.environ.get('TARGET_LEADS', '100'))
        self.test_mode = os.environ.get('TEST_MODE', 'true').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        
        print(f"🎯 Target leads: {self.target_leads}")
        print(f"🧪 Test mode: {self.test_mode}")
        print(f"🔢 Run number: {self.run_number}")
        
        # Requêtes de recherche prêtes
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
            'tech entrepreneur Kenya site:linkedin.com'
        ]
    
    def scrape_google_search(self, query, max_results=50):
        """Scrape Google avec gestion d'erreur simple"""
        results = []
        
        try:
            print(f"  🔍 Recherche: {query[:50]}...")
            
            # Construction URL
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
            
            # Requête
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                print(f"    ⚠️ Status {response.status_code}")
                return results
            
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
                if any(site in href for site in ['linkedin.com/in/', 'instagram.com/', 'twitter.com/']):
                    link_text = link.get_text(strip=True)
                    
                    result = {
                        'url': href,
                        'text': link_text[:200],
                        'query': query,
                        'found_at': datetime.now(timezone.utc).isoformat()
                    }
                    results.append(result)
                    
                    if len(results) >= max_results:
                        break
            
            print(f"    ✅ Trouvé {len(results)} liens")
            
            # Délai anti-détection
            time.sleep(random.uniform(3, 7))
            
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
        
        return results
    
    def determine_platform(self, url):
        """Détermine la plateforme"""
        if 'linkedin.com' in url:
            return 'linkedin'
        elif 'instagram.com' in url:
            return 'instagram'
        elif 'twitter.com' in url:
            return 'twitter'
        else:
            return 'other'
    
    def determine_target_type(self, query, text):
        """Détermine le type de cible"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        if any(word in query_lower for word in ['ceo', 'founder', 'entrepreneur']):
            return 'entrepreneur'
        elif any(word in query_lower for word in ['consultant', 'advisor']):
            return 'consultant'
        elif any(word in query_lower for word in ['musician', 'artist', 'afrobeats']):
            return 'musicien'
        elif any(word in query_lower for word in ['creator', 'influencer']):
            return 'createur'
        else:
            return 'other'
    
    def determine_country(self, query, text):
        """Détermine le pays"""
        query_lower = query.lower()
        text_lower = text.lower()
        
        if any(word in query_lower for word in ['nigeria', 'lagos']):
            return 'nigeria'
        elif 'kenya' in query_lower:
            return 'kenya'
        elif 'ghana' in query_lower:
            return 'ghana'
        elif 'south africa' in query_lower:
            return 'south_africa'
        else:
            return 'africa_other'
    
    def scrape_all_queries(self):
        """Scrape toutes les requêtes"""
        print("🌍 DÉMARRAGE SCRAPING AFRIQUE")
        print("=" * 50)
        
        all_prospects = []
        
        # Limiter les requêtes en mode test
        queries_to_use = self.search_queries[:3] if self.test_mode else self.search_queries
        
        for i, query in enumerate(queries_to_use):
            print(f"\n🎯 Query {i+1}/{len(queries_to_use)}")
            
            # Scraping
            results = self.scrape_google_search(query, max_results=20 if self.test_mode else 50)
            
            # Traitement des résultats
            for result in results:
                prospect = {
                    'url': result['url'],
                    'text': result['text'],
                    'platform': self.determine_platform(result['url']),
                    'target_type': self.determine_target_type(query, result['text']),
                    'country': self.determine_country(query, result['text']),
                    'source_query': query,
                    'found_at': result['found_at'],
                    'region': 'afrique',
                    'run_number': self.run_number
                }
                all_prospects.append(prospect)
            
            # Arrêter si objectif atteint
            if len(all_prospects) >= self.target_leads:
                print(f"🎯 Objectif {self.target_leads} atteint!")
                break
            
            # Délai entre requêtes
            time.sleep(random.uniform(5, 10))
        
        # Suppression des doublons
        unique_prospects = []
        seen_urls = set()
        
        for prospect in all_prospects:
            if prospect['url'] not in seen_urls:
                seen_urls.add(prospect['url'])
                unique_prospects.append(prospect)
        
        removed = len(all_prospects) - len(unique_prospects)
        if removed > 0:
            print(f"🧹 Supprimé {removed} doublons")
        
        print(f"\n🎉 SCRAPING TERMINÉ!")
        print(f"📊 Total prospects uniques: {len(unique_prospects)}")
        
        return unique_prospects
    
    def save_results(self, prospects):
        """Sauvegarde simplifiée"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Créer dossier
        os.makedirs('data', exist_ok=True)
        
        # Noms de fichiers
        csv_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.csv"
        json_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.json"
        summary_file = f"data/summary_afrique_run{self.run_number}_{timestamp}.json"
        
        try:
            if prospects:
                # DataFrame
                df = pd.DataFrame(prospects)
                
                # CSV
                df.to_csv(csv_file, index=False, encoding='utf-8')
                print(f"💾 CSV sauvé: {csv_file}")
                
                # JSON
                df.to_json(json_file, orient='records', indent=2)
                print(f"💾 JSON sauvé: {json_file}")
                
                # Statistiques
                stats = {
                    'total_prospects': len(prospects),
                    'by_platform': df['platform'].value_counts().to_dict(),
                    'by_target_type': df['target_type'].value_counts().to_dict(),
                    'by_country': df['country'].value_counts().to_dict(),
                    'run_number': self.run_number,
                    'timestamp': timestamp,
                    'test_mode': self.test_mode
                }
                
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
                
                print(f"📊 Stats sauvées: {summary_file}")
                print(f"\n📈 RÉSULTATS:")
                print(f"  - Total: {len(prospects)} prospects")
                print(f"  - Platforms: {stats['by_platform']}")
                print(f"  - Types: {stats['by_target_type']}")
                print(f"  - Pays: {stats['by_country']}")
                
                return True
            else:
                print("⚠️ Aucun prospect trouvé")
                return False
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False

def main():
    """Fonction principale"""
    print("🚀 GITHUB ACTIONS - SCRAPING AFRIQUE MEGA")
    print("=" * 60)
    
    try:
        # Initialiser
        scraper = AfriqueScrapingMega()
        
        # Scraper
        prospects = scraper.scrape_all_queries()
        
        # Sauvegarder
        success = scraper.save_results(prospects)
        
        if success:
            print(f"\n🎉 SUCCÈS! {len(prospects)} prospects trouvés")
        else:
            print(f"\n⚠️ ÉCHEC ou aucun résultat")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR FATALE: {e}")
        return False

if __name__ == "__main__":
    main()
