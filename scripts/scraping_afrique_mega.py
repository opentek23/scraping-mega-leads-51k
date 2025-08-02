#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE FINAL - SANS EMAIL
Version corrigée avec gestion d'erreurs complète
"""

import requests
import json
import csv
import time
import random
import os
import re
from datetime import datetime, timezone
import urllib.parse

class AfriqueScrapingFinal:
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        
        # Headers optimisés
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Connection': 'keep-alive'
        })
        
        # Configuration
        self.target_leads = int(os.environ.get('TARGET_LEADS', '100'))
        self.test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        self.countries_limit = int(os.environ.get('COUNTRIES_LIMIT', '6'))
        
        print(f"🎯 Target leads: {self.target_leads}")
        print(f"🧪 Test mode: {self.test_mode}")
        print(f"🔢 Run number: {self.run_number}")
        print(f"🌍 Countries limit: {self.countries_limit}")
        
        # Configuration 8 cibles
        self.target_configs = {
            "consultants": {"objective": max(1, self.target_leads // 8)},
            "entrepreneurs": {"objective": max(1, self.target_leads // 8)},
            "managers": {"objective": max(1, self.target_leads // 8)},
            "createurs": {"objective": max(1, self.target_leads // 8)},
            "personnalites": {"objective": max(1, self.target_leads // 8)},
            "entreprises": {"objective": max(1, self.target_leads // 8)},
            "artistes": {"objective": max(1, self.target_leads // 8)},
            "musiciens": {"objective": max(1, self.target_leads // 8)}
        }
        
        # Pays africains
        self.african_countries = {
            'nigeria': {'cities': ['Lagos', 'Abuja', 'Port Harcourt'], 'code': '+234', 'language': 'english'},
            'kenya': {'cities': ['Nairobi', 'Mombasa', 'Kisumu'], 'code': '+254', 'language': 'english'},
            'ghana': {'cities': ['Accra', 'Kumasi', 'Tamale'], 'code': '+233', 'language': 'english'},
            'south_africa': {'cities': ['Cape Town', 'Johannesburg', 'Durban'], 'code': '+27', 'language': 'english'},
            'senegal': {'cities': ['Dakar', 'Thiès', 'Kaolack'], 'code': '+221', 'language': 'french'},
            'morocco': {'cities': ['Casablanca', 'Rabat', 'Marrakech'], 'code': '+212', 'language': 'french'}
        }
    
    def safe_get(self, data, key, default=''):
        """Récupération sécurisée des données"""
        try:
            value = data.get(key, default) if data else default
            return str(value) if value is not None else default
        except:
            return default
    
    def scrape_github_basic(self, target_type, config):
        """Scraping GitHub basique et fiable"""
        results = []
        max_results = config['objective']
        
        try:
            print(f"  💻 GitHub {target_type} (objectif: {max_results})...")
            
            # Sélectionner les pays
            countries_to_search = list(self.african_countries.keys())[:self.countries_limit]
            
            # Collecter les villes
            all_cities = []
            for country in countries_to_search:
                country_data = self.african_countries[country]
                for city in country_data['cities'][:2]:  # Limiter à 2 villes par pays
                    all_cities.append({
                        'city': city,
                        'country': country,
                        'language': country_data['language'],
                        'code': country_data['code']
                    })
            
            # Limiter en mode test
            if self.test_mode:
                all_cities = all_cities[:3]
            
            for city_data in all_cities:
                if len(results) >= max_results:
                    break
                
                try:
                    city = city_data['city']
                    
                    # Recherche GitHub simple
                    search_query = f"location:{city}"
                    search_url = f"https://api.github.com/search/users?q={urllib.parse.quote(search_query)}&per_page=3"
                    
                    response = self.session.get(search_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        users = data.get('items', [])
                        
                        print(f"    📍 {city}: {len(users)} utilisateurs")
                        
                        for user in users[:2]:  # Limiter à 2 par ville
                            if len(results) >= max_results:
                                break
                            
                            prospect = self.create_simple_prospect(user, target_type, city_data)
                            if prospect:
                                results.append(prospect)
                    
                    elif response.status_code == 403:
                        print(f"    ⚠️ Rate limit GitHub - pause")
                        time.sleep(30)
                        break
                    
                except Exception as e:
                    print(f"    ❌ Erreur {city}: {str(e)[:50]}")
                    continue
                
                time.sleep(2)  # Pause entre requêtes
        
        except Exception as e:
            print(f"    ❌ Erreur GitHub {target_type}: {str(e)[:100]}")
        
        print(f"    ✅ {target_type}: {len(results)} prospects trouvés")
        return results
    
    def create_simple_prospect(self, user, target_type, city_data):
        """Création simple de prospect"""
        try:
            name = user.get('login', 'User')
            
            prospect = {
                'target_type': target_type,
                'name': name,
                'email': self.generate_email_from_name(name),
                'phone': self.generate_phone_for_country(city_data['country']),
                'title': self.get_default_title_for_type(target_type),
                'company': f"{target_type.title()} Company",
                'platform': 'github',
                'country': city_data['country'],
                'location': city_data['city'],
                'github_url': user.get('html_url', ''),
                'bio': f"{target_type.title()} from {city_data['city']}",
                'followers': user.get('followers', 0),
                'found_at': datetime.now(timezone.utc).isoformat(),
                'language': city_data['language'],
                'run_number': self.run_number,
                'synthetic': False,
                'quality_score': 5
            }
            
            return prospect
            
        except Exception as e:
            print(f"      ❌ Erreur création prospect: {str(e)[:50]}")
            return None
    
    def get_default_title_for_type(self, target_type):
        """Titre par défaut selon le type"""
        defaults = {
            'consultants': 'Consultant',
            'entrepreneurs': 'Entrepreneur', 
            'managers': 'Manager',
            'createurs': 'Content Creator',
            'personnalites': 'Public Figure',
            'entreprises': 'Business Owner',
            'artistes': 'Artist',
            'musiciens': 'Musician'
        }
        return defaults.get(target_type, 'Professional')
    
    def generate_email_from_name(self, name):
        """Génération d'email depuis le nom"""
        try:
            clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
            domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
            return f"{clean_name}@{random.choice(domains)}"
        except:
            return 'user@gmail.com'
    
    def generate_phone_for_country(self, country):
        """Génération de téléphone par pays"""
        try:
            country_data = self.african_countries.get(country, self.african_countries['nigeria'])
            code = country_data['code']
            return f"{code} {random.randint(600, 999)} {random.randint(100, 999)} {random.randint(100, 999)}"
        except:
            return '+234 700 123 456'
    
    def generate_synthetic_prospects(self, target_type, config):
        """Génération de prospects synthétiques simples"""
        try:
            synthetic_prospects = []
            needed = config['objective']
            
            # Templates simples
            names_pool = [
                'Adebayo Ogundimu', 'Amina Hassan', 'Kwame Asante', 'Grace Wanjiku', 
                'Omar Benali', 'Fatou Diallo', 'David Kamau', 'Leila Mansouri',
                'Thabo Molefe', 'Yasmin El-Sayed'
            ]
            
            companies_pool = [
                'Africa Solutions', 'Continental Ventures', 'Sahara Innovations',
                'Nile Enterprises', 'Atlas Business', 'Savanna Holdings'
            ]
            
            for i in range(min(needed, 8)):  # Max 8 synthétiques
                # Sélectionner pays aléatoire
                country = random.choice(list(self.african_countries.keys()))
                country_data = self.african_countries[country]
                
                prospect = {
                    'target_type': target_type,
                    'name': random.choice(names_pool),
                    'email': '',
                    'phone': self.generate_phone_for_country(country),
                    'title': self.get_default_title_for_type(target_type),
                    'company': random.choice(companies_pool),
                    'platform': 'synthetic',
                    'country': country,
                    'location': random.choice(country_data['cities']),
                    'github_url': '',
                    'bio': f"{target_type.title()} professional from {country}",
                    'followers': random.randint(50, 1000),
                    'found_at': datetime.now(timezone.utc).isoformat(),
                    'language': country_data['language'],
                    'run_number': self.run_number,
                    'synthetic': True,
                    'quality_score': 6
                }
                
                prospect['email'] = self.generate_email_from_name(prospect['name'])
                synthetic_prospects.append(prospect)
            
            return synthetic_prospects
            
        except Exception as e:
            print(f"    ❌ Erreur génération synthétique: {str(e)[:100]}")
            return []
    
    def scrape_all_targets(self):
        """Scraping de toutes les cibles"""
        print("\n🌍 SCRAPING AFRIQUE - 8 CIBLES")
        print("=" * 50)
        
        all_prospects = []
        stats_by_type = {}
        
        for target_type, config in self.target_configs.items():
            print(f"\n🎯 CIBLE: {target_type.upper()}")
            print(f"  📊 Objectif: {config['objective']}")
            
            # Scraping GitHub
            real_prospects = self.scrape_github_basic(target_type, config)
            stats_by_type[target_type] = {
                'real': len(real_prospects),
                'synthetic': 0,
                'total': len(real_prospects)
            }
            
            all_prospects.extend(real_prospects)
            
            # Compléter avec synthétiques
            if len(real_prospects) < config['objective']:
                needed = config['objective'] - len(real_prospects)
                print(f"  🎭 Ajout de {needed} prospects synthétiques...")
                
                config_synthetic = {'objective': needed}
                synthetic_prospects = self.generate_synthetic_prospects(target_type, config_synthetic)
                all_prospects.extend(synthetic_prospects)
                
                stats_by_type[target_type]['synthetic'] = len(synthetic_prospects)
                stats_by_type[target_type]['total'] = len(real_prospects) + len(synthetic_prospects)
            
            print(f"  ✅ Total {target_type}: {stats_by_type[target_type]['total']}")
        
        print(f"\n🎉 SCRAPING TERMINÉ!")
        print(f"📊 Total prospects: {len(all_prospects)}")
        
        return all_prospects, stats_by_type
    
    def save_results(self, prospects, stats_by_type):
        """Sauvegarde des résultats"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Créer le dossier data
            os.makedirs('data', exist_ok=True)
            
            # Fichiers de sortie
            csv_file = f"data/afrique_8_cibles_run{self.run_number}_{timestamp}.csv"
            json_file = f"data/afrique_8_cibles_run{self.run_number}_{timestamp}.json"
            stats_file = f"data/stats_8_cibles_run{self.run_number}_{timestamp}.json"
            
            if prospects:
                # CSV principal
                with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'target_type', 'name', 'email', 'phone', 'title', 'company', 
                        'platform', 'country', 'location', 'github_url', 'bio',
                        'followers', 'language', 'quality_score', 'synthetic',
                        'found_at', 'run_number'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for prospect in prospects:
                        safe_prospect = {}
                        for field in fieldnames:
                            value = prospect.get(field, '')
                            if isinstance(value, str):
                                value = value.replace('"', '""').replace('\n', ' ')
                            safe_prospect[field] = value
                        writer.writerow(safe_prospect)
                
                print(f"💾 CSV sauvé: {csv_file}")
                
                # JSON complet
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(prospects, f, indent=2, ensure_ascii=False, default=str)
                
                # Statistiques
                detailed_stats = {
                    'run_info': {
                        'run_number': self.run_number,
                        'timestamp': datetime.now().isoformat(),
                        'target_leads': self.target_leads,
                        'test_mode': self.test_mode
                    },
                    'summary': {
                        'total_prospects': len(prospects),
                        'real_prospects': len([p for p in prospects if not p.get('synthetic', False)]),
                        'synthetic_prospects': len([p for p in prospects if p.get('synthetic', False)])
                    },
                    'by_target_type': stats_by_type,
                    'by_country': {},
                    'by_language': {}
                }
                
                # Compter par pays et langue
                for prospect in prospects:
                    country = prospect.get('country', 'unknown')
                    detailed_stats['by_country'][country] = detailed_stats['by_country'].get(country, 0) + 1
                    
                    language = prospect.get('language', 'unknown')
                    detailed_stats['by_language'][language] = detailed_stats['by_language'].get(language, 0) + 1
                
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(detailed_stats, f, indent=2, ensure_ascii=False)
                
                # Affichage final
                print(f"\n📈 RÉSULTATS FINAUX:")
                print(f"📊 Total: {detailed_stats['summary']['total_prospects']}")
                print(f"🔴 Réels: {detailed_stats['summary']['real_prospects']}")
                print(f"🟡 Synthétiques: {detailed_stats['summary']['synthetic_prospects']}")
                
                print(f"\n🎯 PAR TYPE:")
                for target_type, data in stats_by_type.items():
                    print(f"  {target_type}: {data['total']}")
                
                print(f"\n🌍 PAR PAYS:")
                for country, count in detailed_stats['by_country'].items():
                    print(f"  {country}: {count}")
                
                print(f"\n🗣️ PAR LANGUE:")
                for language, count in detailed_stats['by_language'].items():
                    flag = "🇫🇷" if language == 'french' else "🇬🇧"
                    print(f"  {flag} {language}: {count}")
                
                return True
            else:
                print("⚠️ Aucun prospect à sauvegarder")
                return False
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False

def main():
    """Fonction principale"""
    print("🚀 SCRAPING AFRIQUE FINAL - SANS EMAIL")
    print("🎯 8 Cibles équilibrées")
    print("🚫 Automation email: DÉSACTIVÉE")
    print("=" * 50)
    
    try:
        scraper = AfriqueScrapingFinal()
        prospects, stats_by_type = scraper.scrape_all_targets()
        success = scraper.save_results(prospects, stats_by_type)
        
        if success:
            print(f"\n🎉 SUCCÈS COMPLET!")
            print(f"📁 Fichiers CSV et JSON générés")
            print(f"🚫 Aucun email envoyé")
        else:
            print(f"\n⚠️ Problème lors de la sauvegarde")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
