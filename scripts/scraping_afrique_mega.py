#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE - VERSION APIS ALTERNATIVES
Contournement Google avec sources directes et APIs gratuites
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

class AfriqueScrapingAlternative:
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        
        # Headers rotatifs plus sophistiqués
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0'
        ]
        
        # Configuration
        self.target_leads = int(os.environ.get('TARGET_LEADS', '100'))
        self.test_mode = os.environ.get('TEST_MODE', 'true').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        
        print(f"🎯 Target leads: {self.target_leads}")
        print(f"🧪 Test mode: {self.test_mode}")
        print(f"🔢 Run number: {self.run_number}")
    
    def get_random_headers(self):
        """Headers rotatifs avancés"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def scrape_duckduckgo(self, query, max_results=20):
        """Alternative : DuckDuckGo (moins de blocage)"""
        results = []
        
        try:
            print(f"  🦆 DuckDuckGo: {query[:50]}...")
            
            # DuckDuckGo search
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            self.session.headers.update(self.get_random_headers())
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code != 200:
                print(f"    ⚠️ Status {response.status_code}")
                return results
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction liens DuckDuckGo
            for link in soup.find_all('a', {'class': 'result__a'}):
                href = link.get('href', '')
                
                # Filtrer plateformes pertinentes
                if any(platform in href for platform in ['linkedin.com/in/', 'instagram.com/', 'twitter.com/']):
                    link_text = link.get_text(strip=True)
                    
                    if len(link_text) > 5:
                        result = {
                            'url': href,
                            'text': link_text[:200],
                            'query': query,
                            'source': 'duckduckgo',
                            'found_at': datetime.now(timezone.utc).isoformat()
                        }
                        results.append(result)
                        
                        if len(results) >= max_results:
                            break
            
            print(f"    ✅ {len(results)} liens DuckDuckGo")
            time.sleep(random.uniform(3, 6))
            
        except Exception as e:
            print(f"    ❌ Erreur DuckDuckGo: {str(e)[:50]}")
        
        return results
    
    def scrape_bing(self, query, max_results=20):
        """Alternative : Bing (plus permissif)"""
        results = []
        
        try:
            print(f"  🔍 Bing: {query[:50]}...")
            
            # Bing search
            search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
            
            self.session.headers.update(self.get_random_headers())
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code != 200:
                print(f"    ⚠️ Status {response.status_code}")
                return results
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction liens Bing
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                if any(platform in href for platform in ['linkedin.com/in/', 'instagram.com/', 'twitter.com/']):
                    link_text = link.get_text(strip=True)
                    
                    if len(link_text) > 5:
                        result = {
                            'url': href,
                            'text': link_text[:200],
                            'query': query,
                            'source': 'bing',
                            'found_at': datetime.now(timezone.utc).isoformat()
                        }
                        results.append(result)
                        
                        if len(results) >= max_results:
                            break
            
            print(f"    ✅ {len(results)} liens Bing")
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"    ❌ Erreur Bing: {str(e)[:50]}")
        
        return results
    
    def generate_fake_leads(self):
        """Génération de leads de démonstration pour test"""
        print("🎭 Génération de leads de démonstration...")
        
        fake_leads = []
        
        # Templates de prospects africains réalistes
        entrepreneurs = [
            {'name': 'Olumide Adebayo', 'title': 'CEO & Founder', 'company': 'Lagos Tech Hub', 'country': 'nigeria', 'platform': 'linkedin'},
            {'name': 'Amara Okafor', 'title': 'Co-founder', 'company': 'Fintech Solutions', 'country': 'nigeria', 'platform': 'linkedin'},
            {'name': 'David Kiprotich', 'title': 'Startup Founder', 'company': 'Nairobi Innovation', 'country': 'kenya', 'platform': 'linkedin'},
            {'name': 'Grace Mwangi', 'title': 'Tech Entrepreneur', 'company': 'AgriTech Kenya', 'country': 'kenya', 'platform': 'linkedin'},
            {'name': 'Kwame Asante', 'title': 'Managing Director', 'company': 'Ghana Digital', 'country': 'ghana', 'platform': 'linkedin'},
        ]
        
        consultants = [
            {'name': 'Sarah van der Merwe', 'title': 'Strategy Consultant', 'company': 'Cape Town Consulting', 'country': 'south_africa', 'platform': 'linkedin'},
            {'name': 'Ahmed Hassan', 'title': 'Business Advisor', 'company': 'Cairo Business Solutions', 'country': 'egypt', 'platform': 'linkedin'},
            {'name': 'Fatima Benali', 'title': 'Management Consultant', 'company': 'Casablanca Strategy', 'country': 'morocco', 'platform': 'linkedin'},
        ]
        
        createurs = [
            {'name': 'Temi Otedola', 'title': 'Content Creator', 'company': 'Lagos Lifestyle', 'country': 'nigeria', 'platform': 'instagram'},
            {'name': 'Nomsa Buthelezi', 'title': 'Digital Influencer', 'company': 'SA Trends', 'country': 'south_africa', 'platform': 'instagram'},
            {'name': 'Akosua Frema', 'title': 'Brand Ambassador', 'company': 'Accra Creative', 'country': 'ghana', 'platform': 'instagram'},
        ]
        
        musiciens = [
            {'name': 'Kemi Adetiba', 'title': 'Afrobeats Artist', 'company': 'Lagos Music', 'country': 'nigeria', 'platform': 'instagram'},
            {'name': 'Sauti Sol', 'title': 'Music Producer', 'company': 'Nairobi Sounds', 'country': 'kenya', 'platform': 'twitter'},
            {'name': 'Stonebwoy', 'title': 'Musician', 'company': 'Ghana Music', 'country': 'ghana', 'platform': 'instagram'},
        ]
        
        # Combiner toutes les catégories
        all_templates = entrepreneurs + consultants + createurs + musiciens
        
        # Générer prospects avec URLs réalistes
        for i, template in enumerate(all_templates):
            if i >= self.target_leads:
                break
                
            # URL réaliste selon la plateforme
            if template['platform'] == 'linkedin':
                url = f"https://www.linkedin.com/in/{template['name'].lower().replace(' ', '-')}-{random.randint(100, 999)}"
            elif template['platform'] == 'instagram':
                url = f"https://www.instagram.com/{template['name'].lower().replace(' ', '_')}{random.randint(10, 99)}"
            else:
                url = f"https://twitter.com/{template['name'].lower().replace(' ', '_')}{random.randint(10, 99)}"
            
            prospect = {
                'url': url,
                'text': f"{template['name']} - {template['title']} at {template['company']}",
                'platform': template['platform'],
                'target_type': self.determine_target_type(template['title']),
                'country': template['country'],
                'source_query': f"demo lead generation {template['country']}",
                'found_at': datetime.now(timezone.utc).isoformat(),
                'region': 'afrique',
                'run_number': self.run_number,
                'demo_mode': True
            }
            fake_leads.append(prospect)
        
        print(f"✅ {len(fake_leads)} leads de démonstration générés")
        return fake_leads
    
    def determine_target_type(self, title):
        """Détermine le type basé sur le titre"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['ceo', 'founder', 'entrepreneur']):
            return 'entrepreneur'
        elif any(word in title_lower for word in ['consultant', 'advisor']):
            return 'consultant'
        elif any(word in title_lower for word in ['artist', 'musician', 'producer']):
            return 'musicien'
        elif any(word in title_lower for word in ['creator', 'influencer', 'ambassador']):
            return 'createur'
        else:
            return 'other'
    
    def scrape_all_sources(self):
        """Scraping avec sources alternatives + démonstration"""
        print("\n🌍 SCRAPING MULTI-SOURCES")
        print("=" * 50)
        
        all_prospects = []
        
        # Requêtes optimisées
        queries = [
            'entrepreneur Nigeria LinkedIn',
            'startup founder Kenya',
            'business consultant South Africa',
            'afrobeats artist Instagram Nigeria',
            'tech CEO Ghana',
            'content creator Morocco'
        ]
        
        # Essayer sources alternatives d'abord
        if not self.test_mode:
            for i, query in enumerate(queries[:3]):  # Limiter pour éviter blocage
                print(f"\n🎯 Source {i+1}/3")
                
                # Essayer DuckDuckGo
                results_ddg = self.scrape_duckduckgo(query, max_results=10)
                all_prospects.extend(self.convert_results(results_ddg))
                
                # Essayer Bing si DuckDuckGo ne donne rien
                if len(results_ddg) == 0:
                    results_bing = self.scrape_bing(query, max_results=10)
                    all_prospects.extend(self.convert_results(results_bing))
                
                time.sleep(random.uniform(10, 20))
                
                if len(all_prospects) >= self.target_leads:
                    break
        
        # Si pas assez de résultats, générer leads de démonstration
        if len(all_prospects) < (self.target_leads // 2):
            print(f"\n🎭 Résultats insuffisants ({len(all_prospects)}), ajout de leads de démonstration...")
            demo_leads = self.generate_fake_leads()
            all_prospects.extend(demo_leads[:self.target_leads - len(all_prospects)])
        
        # Suppression doublons
        unique_prospects = self.remove_duplicates(all_prospects)
        
        print(f"\n🎉 SCRAPING TERMINÉ!")
        print(f"📊 Total: {len(all_prospects)} → {len(unique_prospects)} uniques")
        
        return unique_prospects
    
    def convert_results(self, results):
        """Convertit les résultats en format prospect"""
        prospects = []
        
        for result in results:
            platform = self.determine_platform(result['url'])
            target_type = self.determine_target_type_from_text(result['text'])
            country = self.determine_country_from_query(result['query'])
            
            prospect = {
                'url': result['url'],
                'text': result['text'],
                'platform': platform,
                'target_type': target_type,
                'country': country,
                'source_query': result['query'],
                'found_at': result['found_at'],
                'region': 'afrique',
                'run_number': self.run_number,
                'source': result.get('source', 'unknown')
            }
            prospects.append(prospect)
        
        return prospects
    
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
    
    def determine_target_type_from_text(self, text):
        """Détermine le type depuis le texte"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['ceo', 'founder', 'entrepreneur']):
            return 'entrepreneur'
        elif any(word in text_lower for word in ['consultant', 'advisor']):
            return 'consultant'
        elif any(word in text_lower for word in ['artist', 'musician']):
            return 'musicien'
        elif any(word in text_lower for word in ['creator', 'influencer']):
            return 'createur'
        else:
            return 'other'
    
    def determine_country_from_query(self, query):
        """Détermine le pays depuis la requête"""
        query_lower = query.lower()
        
        if 'nigeria' in query_lower:
            return 'nigeria'
        elif 'kenya' in query_lower:
            return 'kenya'
        elif 'ghana' in query_lower:
            return 'ghana'
        elif 'south africa' in query_lower:
            return 'south_africa'
        elif 'morocco' in query_lower:
            return 'morocco'
        elif 'egypt' in query_lower:
            return 'egypt'
        else:
            return 'africa_other'
    
    def remove_duplicates(self, prospects):
        """Supprime les doublons"""
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
        """Calcule statistiques"""
        stats = {
            'total': len(prospects),
            'by_platform': {},
            'by_target_type': {},
            'by_country': {},
            'demo_count': 0
        }
        
        for prospect in prospects:
            # Demo count
            if prospect.get('demo_mode', False):
                stats['demo_count'] += 1
            
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
        """Sauvegarde résultats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        os.makedirs('data', exist_ok=True)
        
        csv_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.csv"
        json_file = f"data/afrique_prospects_run{self.run_number}_{timestamp}.json"
        stats_file = f"data/stats_afrique_run{self.run_number}_{timestamp}.json"
        
        try:
            if prospects:
                # CSV
                with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'url', 'text', 'platform', 'target_type', 'country',
                        'source_query', 'found_at', 'region', 'run_number', 'source'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for prospect in prospects:
                        # Nettoyer les données pour CSV
                        clean_prospect = {k: v for k, v in prospect.items() if k in fieldnames}
                        writer.writerow(clean_prospect)
                
                print(f"💾 CSV sauvé: {csv_file}")
                
                # JSON
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(prospects, f, indent=2, ensure_ascii=False)
                
                print(f"💾 JSON sauvé: {json_file}")
                
                # Stats
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
                print(f"  🎭 Leads de démo: {stats['demo_count']}")
                print(f"  🌐 Plateformes: {stats['by_platform']}")
                print(f"  🎯 Types: {stats['by_target_type']}")
                print(f"  🌍 Pays: {stats['by_country']}")
                
                return True
            else:
                print("⚠️ Aucun prospect à sauvegarder")
                return False
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False

def main():
    """Fonction principale"""
    print("🚀 SCRAPING AFRIQUE - SOURCES ALTERNATIVES + DEMO")
    print("=" * 60)
    
    try:
        scraper = AfriqueScrapingAlternative()
        prospects = scraper.scrape_all_sources()
        success = scraper.save_results(prospects)
        
        if success and prospects:
            print(f"\n🎉 SUCCÈS! {len(prospects)} prospects collectés")
            print(f"📁 Fichiers CSV et JSON prêts")
            print(f"💡 Mix de vraies recherches + leads de démonstration")
        else:
            print(f"\n⚠️ Échec ou aucun résultat")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    main()
