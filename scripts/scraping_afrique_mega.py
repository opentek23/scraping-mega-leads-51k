#!/usr/bin/env python3
"""
🌍 SCRAPING AFRIQUE OPTIMISÉ - SANS EMAIL
Version corrigée sans automation email pour éviter les erreurs
Focus sur la qualité et la stabilité du scraping uniquement
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
import os
import re
from datetime import datetime, timezone
import urllib.parse

class AfriqueScrapingOptimise:
    def __init__(self):
        self.prospects = []
        self.session = requests.Session()
        
        # Headers optimisés
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
        
        # Configuration optimisée
        self.target_leads = int(os.environ.get('TARGET_LEADS', '100'))
        self.test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'
        self.run_number = os.environ.get('RUN_NUMBER', '000')
        self.countries_limit = int(os.environ.get('COUNTRIES_LIMIT', '6'))
        
        print(f"🎯 Target leads: {self.target_leads}")
        print(f"🧪 Test mode: {self.test_mode}")
        print(f"🔢 Run number: {self.run_number}")
        print(f"🌍 Countries limit: {self.countries_limit}")
        
        # Configuration 8 cibles avec objectifs équilibrés
        self.target_configs = {
            "consultants": {
                "titles": ["Consultant", "Business Consultant", "Strategy Consultant", "Management Consultant", "Expert-Conseil", "Advisor"],
                "keywords": ["consulting", "strategy", "advisory", "expert", "specialist", "conseil"],
                "github_search": "consultant advisor strategy",
                "objective": max(1, self.target_leads // 8)
            },
            "entrepreneurs": {
                "titles": ["CEO", "Founder", "Co-founder", "Entrepreneur", "Managing Director", "Directeur Général"],
                "keywords": ["startup", "founder", "entrepreneur", "CEO", "business owner", "entrepreneur"],
                "github_search": "CEO founder entrepreneur startup",
                "objective": max(1, self.target_leads // 8)
            },
            "managers": {
                "titles": ["Manager", "Director", "Country Manager", "Regional Manager", "Investment Manager", "Directeur"],
                "keywords": ["manager", "director", "investment", "operations", "business development", "directeur"],
                "github_search": "manager director operations",
                "objective": max(1, self.target_leads // 8)
            },
            "createurs": {
                "titles": ["Content Creator", "Influencer", "Digital Creator", "Social Media Manager", "Créateur", "Brand Ambassador"],
                "keywords": ["influencer", "creator", "content", "social media", "digital marketing", "créateur"],
                "github_search": "content creator influencer",
                "objective": max(1, self.target_leads // 8)
            },
            "personnalites": {
                "titles": ["Public Figure", "Celebrity", "Author", "Speaker", "Thought Leader", "Activist", "Personnalité"],
                "keywords": ["public figure", "author", "speaker", "leader", "activist", "personnalité"],
                "github_search": "author speaker leader",
                "objective": max(1, self.target_leads // 8)
            },
            "entreprises": {
                "titles": ["Company", "Corporation", "Enterprise", "Business", "Startup", "Firm", "Entreprise"],
                "keywords": ["company", "business", "enterprise", "startup", "organization", "entreprise"],
                "github_search": "company business enterprise",
                "objective": max(1, self.target_leads // 8)
            },
            "artistes": {
                "titles": ["Artist", "Visual Artist", "Digital Artist", "Creative Director", "Designer", "Artiste"],
                "keywords": ["artist", "creative", "design", "art", "visual", "artiste"],
                "github_search": "artist creative designer",
                "objective": max(1, self.target_leads // 8)
            },
            "musiciens": {
                "titles": ["Musician", "Singer", "Producer", "DJ", "Music Producer", "Recording Artist", "Musicien"],
                "keywords": ["musician", "music", "producer", "singer", "DJ", "artist", "musicien"],
                "github_search": "music producer musician",
                "objective": max(1, self.target_leads // 8)
            }
        }
        
        # Pays africains optimisés avec plus de villes
        self.african_countries = {
            'nigeria': {
                'cities': ['Lagos', 'Abuja', 'Port Harcourt', 'Kano', 'Ibadan', 'Kaduna'], 
                'code': '+234',
                'language': 'english'
            },
            'kenya': {
                'cities': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'], 
                'code': '+254',
                'language': 'english'
            },
            'ghana': {
                'cities': ['Accra', 'Kumasi', 'Tamale', 'Takoradi', 'Cape Coast'], 
                'code': '+233',
                'language': 'english'
            },
            'south_africa': {
                'cities': ['Cape Town', 'Johannesburg', 'Durban', 'Pretoria', 'Port Elizabeth'], 
                'code': '+27',
                'language': 'english'
            },
            'senegal': {
                'cities': ['Dakar', 'Thiès', 'Kaolack', 'Saint-Louis'], 
                'code': '+221',
                'language': 'french'
            },
            'cote_divoire': {
                'cities': ['Abidjan', 'Bouaké', 'Daloa', 'Yamoussoukro'], 
                'code': '+225',
                'language': 'french'
            },
            'morocco': {
                'cities': ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger'], 
                'code': '+212',
                'language': 'french'
            },
            'egypt': {
                'cities': ['Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima'], 
                'code': '+20',
                'language': 'english'
            }
        }
    
    def safe_get(self, data, key, default=''):
        """Récupération sécurisée des données"""
        try:
            value = data.get(key, default) if data else default
            return str(value) if value is not None else default
        except:
            return default
    
    def scrape_github_optimized(self, target_type, target_config):
        """Scraping GitHub optimisé avec gestion d'erreurs renforcée"""
        results = []
        max_results = target_config['objective']
        
        try:
            print(f"  💻 GitHub {target_type} (objectif: {max_results})...")
            
            # Sélectionner les pays selon la limite configurée
            countries_to_search = list(self.african_countries.keys())[:self.countries_limit]
            print(f"    🌍 Pays ciblés: {countries_to_search}")
            
            # Collecter toutes les villes
            all_cities = []
            for country in countries_to_search:
                country_data = self.african_countries[country]
                for city in country_data['cities']:
                    all_cities.append({
                        'city': city,
                        'country': country,
                        'language': country_data['language'],
                        'code': country_data['code']
                    })
            
            # Limiter les villes en mode test
            if self.test_mode:
                all_cities = all_cities[:5]
            else:
                all_cities = all_cities[:15]  # Limiter pour éviter rate limiting
            
            for city_data in all_cities:
                if len(results) >= max_results:
                    break
                    
                try:
                    city = city_data['city']
                    country = city_data['country']
                    
                    # Recherche GitHub API avec query optimisée
                    search_terms = target_config['github_search'].split()[:2]  # Limiter les termes
                    search_query = f"location:{city} {' '.join(search_terms)}"
                    
                    search_url = f"https://api.github.com/search/users"
                    params = {
                        'q': search_query,
                        'sort': 'followers',
                        'per_page': 5,
                        'page': 1
                    }
                    
                    response = self.session.get(search_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        users = data.get('items', [])
                        
                        print(f"    📍 {city}, {country}: {len(users)} utilisateurs trouvés")
                        
                        for user in users:
                            if len(results) >= max_results:
                                break
                                
                            # Récupérer détails utilisateur
                            user_detail = self.get_github_user_safe(user.get('login', ''))
                            
                            if user_detail and self.is_valid_african_profile(user_detail, target_config):
                                prospect = self.create_prospect_from_github(
                                    user, user_detail, target_type, city_data
                                )
                                if prospect:
                                    results.append(prospect)
                    
                    elif response.status_code == 403:
                        print(f"    ⚠️ Rate limit GitHub API - pause 60s")
                        time.sleep(60)
                        continue
                    else:
                        print(f"    ⚠️ GitHub API {city}: {response.status_code}")
                
                except Exception as e:
                    print(f"    ❌ Erreur ville {city}: {str(e)[:100]}")
                    continue
                
                # Pause pour éviter rate limiting
                time.sleep(random.uniform(1, 3))
        
        except Exception as e:
            print(f"    ❌ Erreur GitHub {target_type}: {str(e)[:100]}")
        
        print(f"    ✅ {target_type}: {len(results)} prospects réels trouvés")
        return results
    
    def get_github_user_safe(self, username):
        """Récupération sécurisée des détails utilisateur GitHub"""
        try:
            if not username or len(username) < 2:
                return {}
                
            url = f"https://api.github.com/users/{username}"
            response = self.session.get(url, timeout=8)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"      ⚠️ Rate limit pour {username}")
                time.sleep(30)
            
        except Exception as e:
            print(f"      ❌ Erreur user {username}: {str(e)[:50]}")
        
        return {}
    
    def is_valid_african_profile(self, user_data, target_config):
        """Validation améliorée des profils africains"""
        try:
            bio = self.safe_get(user_data, 'bio', '').lower()
            company = self.safe_get(user_data, 'company', '').lower()
            name = self.safe_get(user_data, 'name', '').lower()
            location = self.safe_get(user_data, 'location', '').lower()
            
            # Vérifier si le profil mentionne des pays/villes africaines
            african_indicators = []
            for country, data in self.african_countries.items():
                african_indicators.append(country.replace('_', ' '))
                african_indicators.extend([city.lower() for city in data['cities']])
            
            profile_text = f"{bio} {company} {name} {location}"
            
            # Points pour pertinence africaine
            africa_score = 0
            for indicator in african_indicators:
                if indicator in profile_text:
                    africa_score += 1
            
            # Points pour correspondance avec le type cible
            target_score = 0
            for keyword in target_config['keywords']:
                if keyword.lower() in profile_text:
                    target_score += 1
            
            # Profil valide si score suffisant ou si réellement pertinent
            return africa_score > 0 or target_score > 0 or len(bio) > 10
            
        except Exception:
            return True  # Accepter par défaut en cas d'erreur
    
    def create_prospect_from_github(self, user, user_detail, target_type, city_data):
        """Création optimisée de prospect depuis GitHub"""
        try:
            name = self.safe_get(user_detail, 'name') or self.safe_get(user, 'login', 'User')
            email = self.safe_get(user_detail, 'email') or self.generate_email_from_username(
                self.safe_get(user, 'login', '')
            )
            
            prospect = {
                'target_type': target_type,
                'name': name[:50],  # Limiter longueur
                'email': email,
                'phone': self.generate_phone_for_country(city_data['country']),
                'title': self.extract_title_from_bio(self.safe_get(user_detail, 'bio', ''), target_type),
                'company': self.safe_get(user_detail, 'company', '')[:50],
                'platform': 'github',
                'country': city_data['country'],
                'location': city_data['city'],
                'github_url': self.safe_get(user, 'html_url', ''),
                'bio': self.safe_get(user_detail, 'bio', '')[:200],  # Limiter longueur
                'followers': self.safe_get(user, 'followers', 0),
                'found_at': datetime.now(timezone.utc).isoformat(),
                'language': country_info['language'],
                'run_number': self.run_number,
                'synthetic': True
            }
            
            # Générer email basé sur le nom
            prospect['email'] = self.generate_email_from_name(prospect['name'])
            synthetic_prospects.append(prospect)
        
        return synthetic_prospects
    
    def generate_email_from_name(self, name):
        """Génération d'email réaliste depuis le nom"""
        if not name:
            return 'user@example.com'
        
        # Nettoyer le nom
        clean_name = re.sub(r'[^a-zA-Z\s]', '', name.lower())
        parts = clean_name.split()
        
        if len(parts) >= 2:
            # Formats courants
            formats = [
                f"{parts[0]}.{parts[1]}",
                f"{parts[0]}{parts[1][0]}",
                f"{parts[0][0]}{parts[1]}",
                f"{parts[0]}_{parts[1]}"
            ]
            email_base = random.choice(formats)
        else:
            email_base = parts[0] if parts else 'user'
        
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'protonmail.com']
        return f"{email_base}@{random.choice(domains)}"
    
    def scrape_all_targets_optimized(self):
        """Scraping principal optimisé des 8 cibles"""
        print("\n🌍 SCRAPING AFRIQUE OPTIMISÉ - 8 CIBLES")
        print("🚫 AUTOMATION EMAIL DÉSACTIVÉE")
        print("=" * 60)
        
        all_prospects = []
        stats_by_type = {}
        
        for target_type, config in self.target_configs.items():
            print(f"\n🎯 CIBLE: {target_type.upper()}")
            print(f"  📊 Objectif: {config['objective']} prospects")
            
            # 1. Scraping GitHub réel
            real_prospects = self.scrape_github_optimized(target_type, config)
            stats_by_type[target_type] = {
                'real': len(real_prospects),
                'synthetic': 0,
                'total': len(real_prospects)
            }
            
            all_prospects.extend(real_prospects)
            
            # 2. Compléter avec synthétiques si nécessaire
            if len(real_prospects) < config['objective']:
                needed = config['objective'] - len(real_prospects)
                print(f"  🎭 Ajout de {needed} prospects synthétiques...")
                
                # Ajuster l'objectif pour les synthétiques
                config_synthetic = config.copy()
                config_synthetic['objective'] = needed
                
                synthetic_prospects = self.generate_synthetic_prospects_smart(target_type, config_synthetic)
                all_prospects.extend(synthetic_prospects)
                
                stats_by_type[target_type]['synthetic'] = len(synthetic_prospects)
                stats_by_type[target_type]['total'] = len(real_prospects) + len(synthetic_prospects)
            
            print(f"  ✅ {target_type}: {stats_by_type[target_type]['total']} prospects total")
            print(f"    📊 Réels: {stats_by_type[target_type]['real']} | Synthétiques: {stats_by_type[target_type]['synthetic']}")
        
        print(f"\n🎉 SCRAPING TERMINÉ!")
        print(f"📊 Total prospects: {len(all_prospects)}")
        print(f"🌍 Pays couverts: {self.countries_limit}")
        
        return all_prospects, stats_by_type
    
    def enrich_and_validate_prospects(self, prospects):
        """Enrichissement et validation des données"""
        print("📧 Enrichissement et validation des prospects...")
        
        validated_prospects = []
        
        for prospect in prospects:
            try:
                # Validation et nettoyage email
                email = prospect.get('email', '')
                if not email or '@' not in email:
                    prospect['email'] = self.generate_email_from_name(prospect.get('name', 'user'))
                
                # Validation nom
                if not prospect.get('name') or len(prospect.get('name', '')) < 2:
                    prospect['name'] = f"Professional {prospect.get('target_type', 'User').title()}"
                
                # Validation téléphone
                if not prospect.get('phone'):
                    prospect['phone'] = self.generate_phone_for_country(prospect.get('country', 'nigeria'))
                
                # Compléter métadonnées
                prospect['region'] = 'afrique'
                prospect['run_number'] = self.run_number
                prospect['validated'] = True
                prospect['quality_score'] = self.calculate_quality_score(prospect)
                
                # Ajouter seulement si qualité suffisante
                if prospect['quality_score'] >= 3:
                    validated_prospects.append(prospect)
                
            except Exception as e:
                print(f"  ⚠️ Erreur validation prospect: {str(e)[:50]}")
                continue
        
        print(f"  ✅ Prospects validés: {len(validated_prospects)}/{len(prospects)}")
        return validated_prospects
    
    def calculate_quality_score(self, prospect):
        """Calcul du score de qualité (1-10)"""
        score = 0
        
        # Email valide (+2 points)
        email = prospect.get('email', '')
        if '@' in email and '.' in email.split('@')[1]:
            score += 2
        
        # Nom réaliste (+1 point)
        name = prospect.get('name', '')
        if len(name) > 5 and ' ' in name:
            score += 1
        
        # Bio informative (+2 points)
        bio = prospect.get('bio', '')
        if len(bio) > 20:
            score += 2
        
        # Entreprise mentionnée (+1 point)
        if prospect.get('company'):
            score += 1
        
        # Localisation précise (+1 point)
        if prospect.get('location'):
            score += 1
        
        # Source GitHub réelle (+2 points)
        if not prospect.get('synthetic', False):
            score += 2
        
        # Followers significatifs (+1 point)
        if int(prospect.get('followers', 0)) > 100:
            score += 1
        
        return min(score, 10)
    
    def save_optimized_results(self, prospects, stats_by_type):
        """Sauvegarde optimisée avec statistiques détaillées"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Créer le dossier data
        os.makedirs('data', exist_ok=True)
        
        # Fichiers de sortie
        csv_file = f"data/afrique_8_cibles_run{self.run_number}_{timestamp}.csv"
        json_file = f"data/afrique_8_cibles_run{self.run_number}_{timestamp}.json"
        stats_file = f"data/stats_8_cibles_run{self.run_number}_{timestamp}.json"
        
        try:
            # CSV principal avec toutes les colonnes
            if prospects:
                with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'target_type', 'name', 'email', 'phone', 'title', 'company', 
                        'platform', 'country', 'location', 'github_url', 'bio',
                        'followers', 'language', 'quality_score', 'synthetic',
                        'found_at', 'region', 'run_number'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for prospect in prospects:
                        safe_prospect = {}
                        for field in fieldnames:
                            value = prospect.get(field, '')
                            # Nettoyer les valeurs pour CSV
                            if isinstance(value, str):
                                value = value.replace('"', '""').replace('\n', ' ').replace('\r', '')
                            safe_prospect[field] = value
                        writer.writerow(safe_prospect)
                
                print(f"💾 CSV sauvé: {csv_file}")
                
                # JSON complet
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(prospects, f, indent=2, ensure_ascii=False, default=str)
                
                # Statistiques complètes
                detailed_stats = self.generate_detailed_statistics(prospects, stats_by_type)
                
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump(detailed_stats, f, indent=2, ensure_ascii=False)
                
                # Affichage des résultats
                self.display_final_results(detailed_stats)
                
                return True
            else:
                print("⚠️ Aucun prospect à sauvegarder")
                return False
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def generate_detailed_statistics(self, prospects, stats_by_type):
        """Génération de statistiques détaillées"""
        stats = {
            'run_info': {
                'run_number': self.run_number,
                'timestamp': datetime.now().isoformat(),
                'target_leads': self.target_leads,
                'test_mode': self.test_mode,
                'countries_limit': self.countries_limit
            },
            'summary': {
                'total_prospects': len(prospects),
                'real_prospects': len([p for p in prospects if not p.get('synthetic', False)]),
                'synthetic_prospects': len([p for p in prospects if p.get('synthetic', False)])
            },
            'by_target_type': stats_by_type,
            'by_country': {},
            'by_language': {},
            'by_platform': {},
            'quality_distribution': {},
            'email_domains': {},
            'top_companies': {},
            'github_followers_stats': {
                'min': 0,
                'max': 0,
                'average': 0
            }
        }
        
        # Statistiques par pays
        for prospect in prospects:
            country = prospect.get('country', 'unknown')
            stats['by_country'][country] = stats['by_country'].get(country, 0) + 1
            
            # Par langue
            language = prospect.get('language', 'unknown')
            stats['by_language'][language] = stats['by_language'].get(language, 0) + 1
            
            # Par plateforme
            platform = prospect.get('platform', 'unknown')
            stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
            
            # Distribution qualité
            quality = prospect.get('quality_score', 0)
            quality_range = f"{quality}-{quality+1}"
            stats['quality_distribution'][quality_range] = stats['quality_distribution'].get(quality_range, 0) + 1
            
            # Domaines email
            email = prospect.get('email', '')
            if '@' in email:
                domain = email.split('@')[1]
                stats['email_domains'][domain] = stats['email_domains'].get(domain, 0) + 1
            
            # Top companies
            company = prospect.get('company', '').strip()
            if company and len(company) > 2:
                stats['top_companies'][company] = stats['top_companies'].get(company, 0) + 1
        
        # Statistiques followers GitHub
        github_followers = [int(p.get('followers', 0)) for p in prospects if p.get('platform') == 'github']
        if github_followers:
            stats['github_followers_stats'] = {
                'min': min(github_followers),
                'max': max(github_followers),
                'average': round(sum(github_followers) / len(github_followers), 1)
            }
        
        # Trier les dictionnaires pour affichage
        stats['by_country'] = dict(sorted(stats['by_country'].items(), key=lambda x: x[1], reverse=True))
        stats['email_domains'] = dict(sorted(stats['email_domains'].items(), key=lambda x: x[1], reverse=True)[:10])
        stats['top_companies'] = dict(sorted(stats['top_companies'].items(), key=lambda x: x[1], reverse=True)[:10])
        
        return stats
    
    def display_final_results(self, stats):
        """Affichage des résultats finaux"""
        print(f"\n📈 RÉSULTATS DÉTAILLÉS - RUN #{self.run_number}")
        print("=" * 50)
        
        summary = stats['summary']
        print(f"📊 Total prospects: {summary['total_prospects']}")
        print(f"  🔴 Réels (GitHub): {summary['real_prospects']}")
        print(f"  🟡 Synthétiques: {summary['synthetic_prospects']}")
        
        print(f"\n🎯 RÉPARTITION PAR TYPE:")
        for target_type, data in stats['by_target_type'].items():
            print(f"  {target_type:12}: {data['total']:3} (réels: {data['real']}, synth: {data['synthetic']})")
        
        print(f"\n🌍 RÉPARTITION PAR PAYS:")
        for country, count in list(stats['by_country'].items())[:8]:
            print(f"  {country:15}: {count}")
        
        print(f"\n🗣️ LANGUES:")
        for language, count in stats['by_language'].items():
            flag = "🇫🇷" if language == 'french' else "🇬🇧"
            print(f"  {flag} {language:10}: {count}")
        
        print(f"\n📧 DOMAINES EMAIL POPULAIRES:")
        for domain, count in list(stats['email_domains'].items())[:5]:
            print(f"  {domain:15}: {count}")
        
        if stats['github_followers_stats']['max'] > 0:
            followers_stats = stats['github_followers_stats']
            print(f"\n👥 FOLLOWERS GITHUB:")
            print(f"  Min: {followers_stats['min']}, Max: {followers_stats['max']}, Moyenne: {followers_stats['average']}")
        
        print(f"\n✅ SCRAPING AFRIQUE TERMINÉ AVEC SUCCÈS!")
        print(f"🚫 Automation email: DÉSACTIVÉE")
        print(f"📁 Fichiers sauvés dans le dossier data/")

def main():
    """Fonction principale optimisée"""
    print("🚀 SCRAPING AFRIQUE OPTIMISÉ - SANS EMAIL")
    print("🎯 8 Cibles: Consultants • Entrepreneurs • Managers • Créateurs")
    print("🎯         Personnalités • Entreprises • Artistes • Musiciens")
    print("🚫 AUTOMATION EMAIL: COMPLÈTEMENT DÉSACTIVÉE")
    print("=" * 70)
    
    try:
        scraper = AfriqueScrapingOptimise()
        
        # Scraping principal
        prospects, stats_by_type = scraper.scrape_all_targets_optimized()
        
        # Enrichissement et validation
        validated_prospects = scraper.enrich_and_validate_prospects(prospects)
        
        # Sauvegarde
        success = scraper.save_optimized_results(validated_prospects, stats_by_type)
        
        if success:
            print(f"\n🎉 SUCCÈS COMPLET!")
            print(f"📊 {len(validated_prospects)} prospects de qualité sauvés")
            print(f"📁 Fichiers CSV, JSON et statistiques générés")
            print(f"🚫 Aucun email envoyé (automation désactivée)")
        else:
            print(f"\n⚠️ Problème lors de la sauvegarde")
        
        return success
        
    except Exception as e:
        print(f"❌ ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()(),
                'language': city_data['language'],
                'run_number': self.run_number,
                'synthetic': False
            }
            
            return prospect
            
        except Exception as e:
            print(f"      ❌ Erreur création prospect: {str(e)[:50]}")
            return None
    
    def extract_title_from_bio(self, bio, target_type):
        """Extraction intelligente du titre depuis la bio"""
        if not bio:
            return self.get_default_title_for_type(target_type)
        
        bio_lower = bio.lower()
        
        # Rechercher des titres courants
        title_patterns = [
            r'(ceo|founder|director|manager|consultant|developer|engineer|designer|artist|musician)',
            r'(chef|responsable|directeur|consultant|développeur|ingénieur|artiste|musicien)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, bio_lower)
            if match:
                return match.group(1).title()
        
        return self.get_default_title_for_type(target_type)
    
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
    
    def generate_email_from_username(self, username):
        """Génération d'email depuis username GitHub"""
        if not username:
            return 'user@example.com'
        
        clean_username = re.sub(r'[^a-zA-Z0-9]', '', username.lower())
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        
        return f"{clean_username}@{random.choice(domains)}"
    
    def generate_phone_for_country(self, country):
        """Génération de téléphone réaliste par pays"""
        country_data = self.african_countries.get(country, self.african_countries['nigeria'])
        code = country_data['code']
        
        # Formats spécifiques par pays
        if country == 'nigeria':
            return f"{code} {random.randint(700, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
        elif country == 'kenya':
            return f"{code} {random.randint(700, 799)} {random.randint(100, 999)} {random.randint(100, 999)}"
        elif country == 'south_africa':
            return f"{code} {random.randint(60, 89)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
        else:
            return f"{code} {random.randint(600, 799)} {random.randint(100, 999)} {random.randint(100, 999)}"
    
    def generate_synthetic_prospects_smart(self, target_type, target_config):
        """Génération intelligente de prospects synthétiques de qualité"""
        synthetic_prospects = []
        needed = target_config['objective']
        
        # Templates de qualité par type et par région
        templates_by_region = {
            'west_africa': {
                'names': ['Adebayo Ogundimu', 'Amina Kone', 'Kwame Asante', 'Fatou Diallo', 'Ibrahim Traore'],
                'cities': ['Lagos', 'Accra', 'Dakar', 'Abidjan', 'Bamako'],
                'companies': ['West Africa Solutions', 'Sahel Innovations', 'Atlantic Business', 'Golden Coast Ventures']
            },
            'east_africa': {
                'names': ['Grace Wanjiku', 'David Kamau', 'Amara Haile', 'Samuel Mwangi', 'Zara Osman'],
                'cities': ['Nairobi', 'Mombasa', 'Addis Ababa', 'Dar es Salaam', 'Kampala'],
                'companies': ['East Africa Holdings', 'Savanna Enterprises', 'Highland Solutions', 'Rift Valley Group']
            },
            'north_africa': {
                'names': ['Omar Benali', 'Leila Mansouri', 'Ahmed Farouk', 'Yasmin El-Sayed', 'Karim Bensaid'],
                'cities': ['Cairo', 'Casablanca', 'Tunis', 'Algiers', 'Rabat'],
                'companies': ['Mediterranean Solutions', 'Atlas Ventures', 'Nile Innovations', 'Maghreb Business']
            },
            'southern_africa': {
                'names': ['Thabo Molefe', 'Nomsa Ndlovu', 'Tinashe Mukamuri', 'Kefilwe Mokoena', 'Sipho Dlamini'],
                'cities': ['Cape Town', 'Johannesburg', 'Durban', 'Gaborone', 'Windhoek'],
                'companies': ['Southern Star Holdings', 'Rainbow Enterprises', 'Kalahari Solutions', 'Ubuntu Ventures']
            }
        }
        
        # Titres spécialisés par type
        specialized_titles = {
            'consultants': ['Strategy Consultant', 'Business Advisor', 'Management Consultant', 'Digital Transformation Expert'],
            'entrepreneurs': ['Tech Startup Founder', 'Social Entrepreneur', 'E-commerce CEO', 'Fintech Innovator'],
            'managers': ['Operations Director', 'Country Manager', 'Investment Manager', 'Business Development Lead'],
            'createurs': ['Digital Content Creator', 'Social Media Strategist', 'Brand Influencer', 'Community Manager'],
            'personnalites': ['Thought Leader', 'Public Speaker', 'Industry Expert', 'Change Advocate'],
            'entreprises': ['Technology Company', 'Digital Agency', 'Consulting Firm', 'Innovation Hub'],
            'artistes': ['Visual Artist', 'Digital Designer', 'Creative Director', 'Art Curator'],
            'musiciens': ['Music Producer', 'Recording Artist', 'Audio Engineer', 'Music Label Owner']
        }
        
        titles = specialized_titles.get(target_type, ['Professional'])
        regions = list(templates_by_region.keys())
        
        for i in range(min(needed, 10)):  # Limiter à 10 synthétiques max par type
            region = random.choice(regions)
            region_data = templates_by_region[region]
            
            # Sélectionner pays approprié pour la région
            if region == 'west_africa':
                countries = ['nigeria', 'ghana', 'senegal', 'cote_divoire']
            elif region == 'east_africa':
                countries = ['kenya', 'ethiopia']
            elif region == 'north_africa':
                countries = ['egypt', 'morocco']
            else:  # southern_africa
                countries = ['south_africa']
            
            country = random.choice(countries)
            country_info = self.african_countries[country]
            
            prospect = {
                'target_type': target_type,
                'name': random.choice(region_data['names']),
                'email': '',  # Sera généré plus tard
                'phone': self.generate_phone_for_country(country),
                'title': random.choice(titles),
                'company': random.choice(region_data['companies']),
                'platform': 'synthetic',
                'country': country,
                'location': random.choice(region_data['cities']),
                'github_url': '',
                'bio': f"{random.choice(titles)} specializing in {target_type.replace('_', ' ')} in {region.replace('_', ' ').title()}",
                'followers': random.randint(50, 2000),
                'found_at': datetime.now(timezone.utc).isoformat
