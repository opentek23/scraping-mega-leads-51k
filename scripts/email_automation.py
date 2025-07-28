#!/usr/bin/env python3
"""
📧 AUTOMATION EMAIL NEOLINKS MULTILINGUE + ANTI-DOUBLON
Évite d'envoyer plusieurs fois à la même personne
"""

import smtplib
import csv
import time
import random
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import glob

class NeolinksEmailSafe:
    def __init__(self):
        # Configuration email
        self.sender_email = os.environ.get('SENDER_EMAIL', 'contact@neolinks.me')
        self.sender_password = os.environ.get('EMAIL_PASSWORD', '')
        self.sender_name = "Saïd Ali Omar"
        
        # Configuration SMTP Hostinger
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.hostinger.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '465'))
        self.smtp_use_ssl = os.environ.get('SMTP_USE_SSL', 'true').lower() == 'true'
        
        # Fichier historique des emails envoyés
        self.sent_emails_file = "data/sent_emails_history.json"
        
        # Configuration langues par pays
        self.country_languages = {
            # Pays francophones
            'senegal': 'french', 'cote_divoire': 'french', 'burkina_faso': 'french',
            'mali': 'french', 'niger': 'french', 'guinea': 'french', 'benin': 'french',
            'togo': 'french', 'gabon': 'french', 'cameroon': 'french', 'chad': 'french',
            'central_african_republic': 'french', 'congo': 'french', 'drc': 'french',
            'madagascar': 'french', 'mauritius': 'french', 'comoros': 'french',
            'djibouti': 'french', 'tunisia': 'french', 'algeria': 'french', 'morocco': 'french',
            
            # Pays anglophones
            'nigeria': 'english', 'ghana': 'english', 'kenya': 'english', 'uganda': 'english',
            'tanzania': 'english', 'rwanda': 'english', 'south_africa': 'english',
            'botswana': 'english', 'zambia': 'english', 'zimbabwe': 'english',
            'malawi': 'english', 'ethiopia': 'english', 'sudan': 'english',
            'south_sudan': 'english', 'liberia': 'english', 'sierra_leone': 'english',
            'gambia': 'english', 'egypt': 'english'
        }
        
        # Templates français
        self.templates_french = {
            'email_content': """Salut {name},

J'espère que vous allez bien, vous faites un formidable travail !

Aujourd'hui je veux vous présenter neolinks, une plateforme qui vous permet de centraliser vos liens, réseaux sociaux, boutique en ligne, produits digitaux, boutique musique, ebooks, événements, en un seul profil digital - un gestionnaire de liens que vous pouvez mettre dans la bio de vos réseaux sociaux, partager pour permettre à votre audience de vous suivre partout et d'acheter vos produits et services.

Et en plus de ça, le mode digital business vous permet de réseauter de façon sûre et durable lors des événements, rencontres, salons sans avoir à imprimer de cartes de visite ou risquer de perdre des contacts qui parfois compromettent les opportunités.

Je vous laisse quelques liens de profils digitaux, et un lien vidéo de présentation de notre innovation digitale :

🔗 Exemples de profils :
- https://neolinks.me/tare
- https://neolinks.me/eliecroupy  
- https://neolinks.me/sheratondj

🎥 Vidéo de présentation :
https://drive.google.com/file/d/1r-ptlpEWG770VH_ox71RtQRUUJaZWD9Z/view

---
Saïd Ali Omar
contact@neolinks.me
https://neolinks.me/""",

            'subjects': {
                "consultants": "{name}, optimisez votre networking professionnel",
                "entrepreneurs": "Solution digitale pour entrepreneurs - {name}",
                "managers": "{name}, centralisez votre présence business", 
                "createurs": "{name}, boostez votre audience avec 1 seul lien",
                "personnalites": "Présence digitale optimisée pour {name}",
                "entreprises": "Solution de gestion de liens pour {name}",
                "artistes": "{name}, centralisez votre portfolio artistique",
                "musiciens": "{name}, 1 lien pour fans, streaming et boutique"
            }
        }
        
        # Templates anglais  
        self.templates_english = {
            'email_content': """Hi {name},

I hope you're doing well, you're doing amazing work!

Today I want to introduce you to neolinks, a platform that allows you to centralize your links, social networks, online store, digital products, music store, ebooks, events, into a single digital profile - a link management tool that you can put in your social media bio, share to allow your audience to follow you everywhere and buy your products and services.

And on top of that, digital business mode allows you to network safely and sustainably at events, meetings, trade shows without having to print business cards or risk losing contacts that sometimes compromise opportunities.

Here are some digital profile links, and a video link presenting our digital innovation:

🔗 Profile examples:
- https://neolinks.me/tare
- https://neolinks.me/eliecroupy  
- https://neolinks.me/sheratondj

🎥 Presentation video:
https://drive.google.com/file/d/1r-ptlpEWG770VH_ox71RtQRUUJaZWD9Z/view

---
Saïd Ali Omar
contact@neolinks.me
https://neolinks.me/""",

            'subjects': {
                "consultants": "{name}, optimize your professional networking",
                "entrepreneurs": "Digital solution for entrepreneurs - {name}",
                "managers": "{name}, centralize your business presence", 
                "createurs": "{name}, boost your audience with 1 single link",
                "personnalites": "Optimized digital presence for {name}",
                "entreprises": "Link management solution for {name}",
                "artistes": "{name}, centralize your artistic portfolio",
                "musiciens": "{name}, 1 link for fans, streaming and store"
            }
        }
        
        print(f"📧 Email Automation Neolinks avec Anti-Doublon")
        print(f"📨 Expéditeur: {self.sender_email}")
        print(f"🛡️ Protection contre doublons activée")
    
    def load_sent_emails_history(self):
        """Charge l'historique des emails envoyés"""
        try:
            if os.path.exists(self.sent_emails_file):
                with open(self.sent_emails_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                print(f"📚 Historique chargé: {len(history)} emails déjà envoyés")
                return set(history)
            else:
                print("📚 Aucun historique trouvé - premier envoi")
                return set()
        except Exception as e:
            print(f"⚠️ Erreur lecture historique: {e}")
            return set()
    
    def save_sent_emails_history(self, sent_emails):
        """Sauvegarde l'historique des emails envoyés"""
        try:
            os.makedirs('data', exist_ok=True)
            
            with open(self.sent_emails_file, 'w', encoding='utf-8') as f:
                json.dump(list(sent_emails), f, indent=2)
            
            print(f"📚 Historique sauvé: {len(sent_emails)} emails au total")
        except Exception as e:
            print(f"❌ Erreur sauvegarde historique: {e}")
    
    def find_latest_csv(self):
        """Trouve le CSV le plus récent généré par le scraping"""
        try:
            csv_files = glob.glob("data/afrique_8_cibles_run*.csv")
            
            if not csv_files:
                print("⚠️ Aucun fichier CSV trouvé")
                return None
            
            latest_csv = max(csv_files, key=os.path.getctime)
            print(f"📁 CSV trouvé: {latest_csv}")
            return latest_csv
            
        except Exception as e:
            print(f"❌ Erreur recherche CSV: {e}")
            return None
    
    def get_language_for_country(self, country):
        """Détermine la langue selon le pays"""
        country_clean = country.lower().replace(' ', '_')
        return self.country_languages.get(country_clean, 'english')
    
    def get_templates_for_language(self, language):
        """Retourne les templates selon la langue"""
        if language == 'french':
            return self.templates_french
        else:
            return self.templates_english
    
    def load_prospects_with_dedup(self, csv_file, sent_emails_history):
        """Charge prospects en filtrant les doublons"""
        new_prospects = []
        duplicates_found = 0
        language_stats = {'french': 0, 'english': 0}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    email = row.get('email', '').strip()
                    name = row.get('name', '').strip()
                    country = row.get('country', '').strip()
                    
                    if email and '@' in email and name:
                        if email in sent_emails_history:
                            duplicates_found += 1
                            print(f"  🔄 Déjà envoyé: {name} ({email})")
                            continue
                        
                        language = self.get_language_for_country(country)
                        language_stats[language] += 1
                        
                        prospect = {
                            'name': name,
                            'email': email,
                            'target_type': row.get('target_type', 'prospect'),
                            'company': row.get('company', ''),
                            'country': country,
                            'location': row.get('location', ''),
                            'title': row.get('title', ''),
                            'phone': row.get('phone', ''),
                            'language': language
                        }
                        new_prospects.append(prospect)
                
                print(f"\n📊 ANALYSE DOUBLONS:")
                print(f"✅ Nouveaux prospects: {len(new_prospects)}")
                print(f"🔄 Doublons évités: {duplicates_found}")
                print(f"🇫🇷 Nouveaux français: {language_stats['french']}")
                print(f"🇬🇧 Nouveaux anglais: {language_stats['english']}")
                
                return new_prospects, duplicates_found
                
        except Exception as e:
            print(f"❌ Erreur lecture CSV: {e}")
            return [], 0
    
    def personalize_subject(self, prospect):
        """Personnalise l'objet selon le type et la langue"""
        target_type = prospect.get('target_type', 'prospect')
        name = prospect.get('name', 'Prospect')
        language = prospect.get('language', 'english')
        
        first_name = name.split()[0] if name else 'Prospect'
        templates = self.get_templates_for_language(language)
        
        subject_template = templates['subjects'].get(
            target_type, 
            f"Présentation neolinks pour {first_name}" if language == 'french' 
            else f"Neolinks presentation for {first_name}"
        )
        
        return subject_template.format(name=first_name)
    
    def personalize_email(self, prospect):
        """Personnalise le contenu email selon la langue"""
        name = prospect.get('name', 'Prospect')
        language = prospect.get('language', 'english')
        
        first_name = name.split()[0] if name else 'Prospect'
        templates = self.get_templates_for_language(language)
        
        return templates['email_content'].format(name=first_name)
    
    def send_email(self, prospect):
        """Envoie un email à un prospect dans sa langue"""
        try:
            subject = self.personalize_subject(prospect)
            content = self.personalize_email(prospect)
            recipient_email = prospect['email']
            language_flag = "🇫🇷" if prospect.get('language') == 'french' else "🇬🇧"
            
            msg = MIMEMultipart()
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # Connexion SMTP Hostinger
            if self.smtp_use_ssl and self.smtp_port == 465:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
            
            print(f"  ✅ {language_flag} Email envoyé à {prospect['name']} ({recipient_email})")
            return True
            
        except Exception as e:
            print(f"  ❌ Erreur envoi à {prospect.get('name', 'Inconnu')}: {e}")
            return False
    
    def send_batch_emails_safe(self, prospects, sent_emails_history, batch_size=10, delay_range=(30, 60)):
        """Envoie emails par batch avec mise à jour de l'historique"""
        if not prospects:
            print("🔄 Aucun nouveau prospect à contacter")
            return 0, 0, {'french': 0, 'english': 0}
        
        print(f"\n📧 DÉMARRAGE ENVOI SÉCURISÉ")
        print(f"📊 Nouveaux prospects: {len(prospects)}")
        print(f"📦 Taille batch: {batch_size}")
        
        sent_count = 0
        failed_count = 0
        language_sent = {'french': 0, 'english': 0}
        newly_sent_emails = set()
        
        for i, prospect in enumerate(prospects):
            language_flag = "🇫🇷" if prospect.get('language') == 'french' else "🇬🇧"
            print(f"\n📧 Email {i+1}/{len(prospects)} {language_flag}")
            
            if self.send_email(prospect):
                sent_count += 1
                language_sent[prospect.get('language', 'english')] += 1
                newly_sent_emails.add(prospect['email'])
            else:
                failed_count += 1
            
            # Délai anti-spam
            if i < len(prospects) - 1:
                delay = random.randint(delay_range[0], delay_range[1])
                print(f"  ⏱️ Pause {delay}s...")
                time.sleep(delay)
            
            # Pause entre batches
            if (i + 1) % batch_size == 0 and i < len(prospects) - 1:
                batch_delay = random.randint(300, 600)
                print(f"\n🔄 Fin batch {(i+1)//batch_size}. Pause {batch_delay//60}min...")
                time.sleep(batch_delay)
        
        # Mettre à jour l'historique
        updated_history = sent_emails_history.union(newly_sent_emails)
        self.save_sent_emails_history(updated_history)
        
        print(f"\n📊 Statistiques envoi:")
        print(f"🇫🇷 Français: {language_sent['french']}")
        print(f"🇬🇧 Anglais: {language_sent['english']}")
        
        return sent_count, failed_count, language_sent
    
    def save_email_report(self, sent_count, failed_count, prospects, language_sent, duplicates_avoided):
        """Sauvegarde rapport d'envoi avec info doublons"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/email_report_safe_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_prospects_in_csv': len(prospects) + duplicates_avoided,
            'new_prospects': len(prospects),
            'duplicates_avoided': duplicates_avoided,
            'emails_sent': sent_count,
            'emails_failed': failed_count,
            'success_rate': round((sent_count / len(prospects)) * 100, 2) if prospects else 0,
            'by_language': language_sent,
            'sender': self.sender_email,
            'antiduplicate_protection': True
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 Rapport sécurisé sauvé: {report_file}")
            return report_file
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")
            return None
    
    def run_automation(self):
        """Lance l'automation complète avec protection anti-doublon"""
        print("🚀 DÉMARRAGE AUTOMATION EMAIL SÉCURISÉE")
        print("🛡️ Protection anti-doublon activée")
        print("🌍 Français + Anglais selon pays")
        print("=" * 70)
        
        # 1. Charger l'historique des emails envoyés
        sent_emails_history = self.load_sent_emails_history()
        
        # 2. Trouver le CSV le plus récent
        csv_file = self.find_latest_csv()
        if not csv_file:
            print("❌ Aucun CSV trouvé.")
            return False
        
        # 3. Charger prospects en filtrant les doublons
        prospects, duplicates_avoided = self.load_prospects_with_dedup(csv_file, sent_emails_history)
        
        if not prospects:
            print("🔄 Tous les prospects ont déjà reçu un email")
            print(f"📊 {duplicates_avoided} doublons évités")
            return True
        
        # 4. Vérifier configuration email
        if not self.sender_password:
            print("⚠️ Mot de passe email non configuré (EMAIL_PASSWORD)")
            print("📧 Mode simulation activé")
            
            for i, prospect in enumerate(prospects[:3]):
                subject = self.personalize_subject(prospect)
                language_flag = "🇫🇷" if prospect.get('language') == 'french' else "🇬🇧"
                
                print(f"\n📧 EMAIL SIMULÉ {i+1} {language_flag}:")
                print(f"À: {prospect['email']}")
                print(f"Objet: {subject}")
            
            print(f"\n🎭 {len(prospects)} NOUVEAUX emails seraient envoyés")
            return True
        
        # 5. Envoi réel avec protection
        print(f"\n📧 ENVOI SÉCURISÉ DE {len(prospects)} NOUVEAUX EMAILS")
        sent_count, failed_count, language_sent = self.send_batch_emails_safe(
            prospects, sent_emails_history
        )
        
        # 6. Rapport final
        self.save_email_report(sent_count, failed_count, prospects, language_sent, duplicates_avoided)
        
        print(f"\n🎉 AUTOMATION SÉCURISÉE TERMINÉE")
        print(f"✅ Nouveaux envoyés: {sent_count}")
        print(f"🔄 Doublons évités: {duplicates_avoided}")
        print(f"❌ Échecs: {failed_count}")
        print(f"🛡️ Protection anti-doublon: ACTIVE")
        
        return sent_count > 0

def main():
    """Fonction principale pour GitHub Actions"""
    automation = NeolinksEmailSafe()
    success = automation.run_automation()
    
    if success:
        print("::set-output name=email_success::true")
    else:
        print("::set-output name=email_success::false")
    
    return success

if __name__ == "__main__":
    main()
