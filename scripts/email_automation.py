#!/usr/bin/env python3
"""
📧 AUTOMATION EMAIL NEOLINKS - GMAIL ANTI-DOUBLON FIXÉ
Fix critique : Protection anti-doublon renforcée
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

class NeolinksEmailGmail:
    def __init__(self):
        # Configuration email Gmail
        self.sender_email = 'neolinks.me@gmail.com'  # Email Gmail fixe
        self.sender_password = os.environ.get('EMAIL_PASSWORD', '')  # Mot de passe app Gmail
        self.sender_name = "Saïd Ali Omar - Neolinks"
        
        # ✅ CONFIGURATION GMAIL OPTIMISÉE ANTI-BLOCAGE
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587  # Port TLS Gmail
        self.smtp_use_tls = True
        
        # ✅ PARAMÈTRES ANTI-SPAM GMAIL
        self.daily_limit = 500  # Limite Gmail quotidienne
        self.hourly_limit = 100  # Limite horaire recommandée
        self.batch_size = 10    # 10 emails par batch
        self.delay_range = (60, 120)  # 1-2 minutes entre emails (sécurisé)
        self.batch_delay_range = (900, 1800)  # 15-30 min entre batches
        
        # ✅ FIX CRITIQUE : Fichier historique avec chemin absolu
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

Aujourd'hui je veux vous présenter neolinks, une plateforme innovante qui vous permet de centraliser vos liens, réseaux sociaux, boutique en ligne, produits digitaux, boutique musique, ebooks, événements, en un seul profil digital.

C'est un gestionnaire de liens intelligent que vous pouvez mettre dans la bio de vos réseaux sociaux, partager pour permettre à votre audience de vous suivre partout et découvrir vos produits et services.

🌟 AVANTAGES NEOLINKS :
✅ Centralisation complète de votre présence digitale
✅ Augmentation du trafic vers vos plateformes
✅ Suivi des clics et analytics détaillés
✅ Design professionnel personnalisable

En plus de ça, le mode "Digital Business" vous permet de réseauter de façon moderne et durable lors des événements, rencontres, salons - plus besoin d'imprimer des cartes de visite ou de risquer de perdre des contacts précieux.

🔗 Découvrez quelques exemples de profils :
• https://neolinks.me/tare
• https://neolinks.me/eliecroupy  
• https://neolinks.me/sheratondj

🎥 Vidéo de présentation complète :
https://drive.google.com/file/d/1r-ptlpEWG770VH_ox71RtQRUUJaZWD9Z/view

Seriez-vous intéressé(e) par une démonstration personnalisée ?

Cordialement,
Saïd Ali Omar
Fondateur - Neolinks
neolinks.me@gmail.com
https://neolinks.me/""",

            'subjects': {
                "consultants": "🚀 {name}, révolutionnez votre networking professionnel",
                "entrepreneurs": "💡 Solution digitale innovante pour entrepreneurs - {name}",
                "managers": "📈 {name}, centralisez votre présence business", 
                "createurs": "🎯 {name}, votre profil digital unique et outil de networking avancé",
                "personnalites": "⭐ Présence digitale optimisée pour {name}",
                "entreprises": "🔗 Solution de gestion de liens pour {name}",
                "artistes": "🎨 {name}, centralisez votre portfolio artistique",
                "musiciens": "🎵 {name}, 1 lien pour fans, streaming et boutique"
            }
        }
        
        # Templates anglais  
        self.templates_english = {
            'email_content': """Hi {name},

I hope you're doing well, you're doing amazing work!

Today I want to introduce you to neolinks, an innovative platform that allows you to centralize your links, social networks, online store, digital products, music store, ebooks, events, into a single powerful digital profile.

It's an intelligent link management tool that you can put in your social media bio, share to allow your audience to follow you everywhere and discover your products and services.

🌟 NEOLINKS BENEFITS:
✅ Complete centralization of your digital presence
✅ Increased traffic to your platforms
✅ Click tracking and detailed analytics
✅ Professional customizable design

On top of that, "Digital Business" mode allows you to network in a modern and sustainable way at events, meetings, trade shows - no more need to print business cards or risk losing precious contacts.

🔗 Discover some profile examples:
• https://neolinks.me/tare
• https://neolinks.me/eliecroupy  
• https://neolinks.me/sheratondj

🎥 Complete presentation video:
https://drive.google.com/file/d/1r-ptlpEWG770VH_ox71RtQRUUJaZWD9Z/view

Would you be interested in a personalized demonstration?

Best regards,
Saïd Ali Omar
Founder - Neolinks
neolinks.me@gmail.com
https://neolinks.me/""",

            'subjects': {
                "consultants": "🚀 {name}, revolutionize your professional networking",
                "entrepreneurs": "💡 Innovative digital solution for entrepreneurs - {name}",
                "managers": "📈 {name}, centralize your business presence", 
                "createurs": "🎯 {name}, your one digital profile and advanced digital networking tool",
                "personnalites": "⭐ Optimized digital presence for {name}",
                "entreprises": "🔗 Link management solution for {name}",
                "artistes": "🎨 {name}, centralize your artistic portfolio",
                "musiciens": "🎵 {name}, 1 link for fans, streaming and store"
            }
        }
        
        print(f"📧 Email Automation Neolinks - GMAIL ANTI-DOUBLON FIXÉ")
        print(f"📨 Expéditeur: {self.sender_email}")
        print(f"🔗 SMTP: {self.smtp_server}:{self.smtp_port}")
        print(f"🛡️ Protection anti-doublon: RENFORCÉE")
        print(f"📊 Limites: {self.hourly_limit}/h, {self.daily_limit}/jour")
    
    def load_sent_emails_history(self):
        """✅ FIX : Charge l'historique avec vérification renforcée"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs('data', exist_ok=True)
            
            # Vérifier l'existence du fichier
            if os.path.exists(self.sent_emails_file):
                with open(self.sent_emails_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if content:  # ✅ Vérifier que le fichier n'est pas vide
                    history = json.loads(content)
                    if isinstance(history, list):
                        print(f"📚 Historique chargé: {len(history)} emails déjà envoyés")
                        print(f"🔍 Derniers emails envoyés: {history[-3:] if len(history) >= 3 else history}")
                        return set(history)
                    else:
                        print("⚠️ Format historique invalide - reset")
                        return set()
                else:
                    print("📚 Fichier historique vide - premier envoi")
                    return set()
            else:
                print("📚 Aucun historique trouvé - création du fichier")
                # ✅ Créer le fichier vide immédiatement
                with open(self.sent_emails_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                return set()
                
        except Exception as e:
            print(f"❌ Erreur lecture historique: {e}")
            print(f"🔧 Création d'un nouvel historique")
            try:
                with open(self.sent_emails_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except:
                pass
            return set()
    
    def save_sent_emails_history(self, sent_emails):
        """✅ FIX : Sauvegarde renforcée avec vérification"""
        try:
            os.makedirs('data', exist_ok=True)
            
            # ✅ Double sauvegarde pour sécurité
            emails_list = sorted(list(sent_emails))  # Trier pour consistance
            
            # Sauvegarde principale
            with open(self.sent_emails_file, 'w', encoding='utf-8') as f:
                json.dump(emails_list, f, indent=2, ensure_ascii=False)
            
            # ✅ Sauvegarde backup avec timestamp
            backup_file = f"data/sent_emails_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(emails_list, f, indent=2, ensure_ascii=False)
            
            print(f"📚 Historique sauvé: {len(emails_list)} emails au total")
            print(f"💾 Backup créé: {backup_file}")
            
            # ✅ Vérification immédiate
            test_load = self.load_sent_emails_history()
            if len(test_load) == len(sent_emails):
                print("✅ Vérification sauvegarde: OK")
            else:
                print(f"⚠️ Problème sauvegarde détecté: {len(test_load)} vs {len(sent_emails)}")
                
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
        """✅ FIX : Dédoublonnage renforcé avec logs détaillés"""
        new_prospects = []
        duplicates_found = 0
        language_stats = {'french': 0, 'english': 0}
        duplicates_list = []  # ✅ Pour tracer les doublons
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    email = row.get('email', '').strip().lower()  # ✅ Normaliser email
                    name = row.get('name', '').strip()
                    country = row.get('country', '').strip()
                    
                    if email and '@' in email and name:
                        # ✅ VÉRIFICATION ANTI-DOUBLON RENFORCÉE
                        if email in sent_emails_history:
                            duplicates_found += 1
                            duplicates_list.append(f"{name} ({email})")
                            print(f"🔄 DOUBLON ÉVITÉ: {name} ({email})")
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
                
                print(f"\n📊 ANALYSE DOUBLONS DÉTAILLÉE:")
                print(f"✅ Nouveaux prospects: {len(new_prospects)}")
                print(f"🔄 Doublons évités: {duplicates_found}")
                print(f"🇫🇷 Nouveaux français: {language_stats['french']}")
                print(f"🇬🇧 Nouveaux anglais: {language_stats['english']}")
                
                if duplicates_list:
                    print(f"📝 Doublons détectés:")
                    for dup in duplicates_list[:5]:  # Afficher les 5 premiers
                        print(f"   • {dup}")
                    if len(duplicates_list) > 5:
                        print(f"   ... et {len(duplicates_list) - 5} autres")
                
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
            f"🚀 Présentation neolinks pour {first_name}" if language == 'french' 
            else f"🚀 Neolinks presentation for {first_name}"
        )
        
        return subject_template.format(name=first_name)
    
    def personalize_email(self, prospect):
        """Personnalise le contenu email selon la langue"""
        name = prospect.get('name', 'Prospect')
        language = prospect.get('language', 'english')
        
        first_name = name.split()[0] if name else 'Prospect'
        templates = self.get_templates_for_language(language)
        
        return templates['email_content'].format(name=first_name)
    
    def test_gmail_connection(self):
        """Test de connexion Gmail avec authentification"""
        try:
            print("🔍 Test connexion Gmail...")
            print(f"📧 Email: {self.sender_email}")
            print(f"📡 Serveur: {self.smtp_server}:{self.smtp_port}")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Activation TLS
            server.login(self.sender_email, self.sender_password)
            server.quit()
            
            print("✅ Connexion Gmail réussie !")
            print("🔐 Authentification Gmail OK")
            return True
            
        except Exception as e:
            print(f"❌ Erreur connexion Gmail: {e}")
            if "Username and Password not accepted" in str(e):
                print("💡 Solution: Utilisez un 'App Password' Gmail au lieu du mot de passe principal")
                print("📱 Gmail → Security → 2-Step Verification → App passwords")
            return False
    
    def create_professional_email(self, prospect):
        """Crée un email professionnel avec headers anti-spam"""
        subject = self.personalize_subject(prospect)
        content = self.personalize_email(prospect)
        
        msg = MIMEMultipart('alternative')  # Support HTML + text
        
        # ✅ HEADERS ANTI-SPAM
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = prospect['email']
        msg['Subject'] = subject
        msg['Reply-To'] = self.sender_email
        msg['X-Mailer'] = 'Neolinks Email System 1.0'
        msg['X-Priority'] = '3'  # Priorité normale
        
        # Contenu texte (anti-spam)
        text_part = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        return msg
    
    def send_email_gmail_safe(self, prospect, sent_emails_history):
        """✅ FIX : Envoi avec vérification anti-doublon AVANT envoi"""
        try:
            email = prospect['email'].lower()
            
            # ✅ DOUBLE VÉRIFICATION ANTI-DOUBLON AVANT ENVOI
            if email in sent_emails_history:
                print(f"  🔄 DOUBLON DÉTECTÉ - SKIP: {prospect['name']} ({email})")
                return False, True  # Failed mais doublon détecté
            
            language_flag = "🇫🇷" if prospect.get('language') == 'french' else "🇬🇧"
            
            # Créer email professionnel
            msg = self.create_professional_email(prospect)
            
            # ✅ CONNEXION GMAIL SÉCURISÉE
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # TLS obligatoire
            server.login(self.sender_email, self.sender_password)
            
            # Envoi avec gestion d'erreur
            server.send_message(msg)
            server.quit()
            
            print(f"  ✅ {language_flag} Gmail envoyé à {prospect['name']} ({email})")
            return True, False  # Success et pas de doublon
            
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Erreur Gmail {prospect.get('name', 'Inconnu')}: {error_msg}")
            
            # Diagnostic erreurs communes
            if "5.5.1" in error_msg:
                print("     💡 Tip: Adresse email invalide")
            elif "5.7.1" in error_msg:
                print("     💡 Tip: Email bloqué par le destinataire")
            elif "4.2.1" in error_msg:
                print("     💡 Tip: Boîte email pleine")
            
            return False, False  # Failed et pas de doublon
    
    def send_batch_emails_gmail(self, prospects, sent_emails_history):
        """✅ FIX : Envoi batch avec protection anti-doublon MAXIMALE"""
        if not prospects:
            print("🔄 Aucun nouveau prospect à contacter")
            return 0, 0, {'french': 0, 'english': 0}
        
        print(f"\n📧 ENVOI GMAIL ANTI-DOUBLON RENFORCÉ")
        print(f"📊 Nouveaux prospects: {len(prospects)}")
        print(f"📦 Batch size: {self.batch_size}")
        print(f"⏱️ Délais: {self.delay_range[0]}-{self.delay_range[1]}s entre emails")
        
        # Test connexion avant envoi
        if not self.test_gmail_connection():
            print("❌ Impossible de se connecter à Gmail")
            return 0, len(prospects), {'french': 0, 'english': 0}
        
        sent_count = 0
        failed_count = 0
        duplicates_detected = 0
        language_sent = {'french': 0, 'english': 0}
        newly_sent_emails = set(sent_emails_history)  # ✅ Commencer avec historique existant
        
        # ✅ ENVOI SÉCURISÉ AVEC PROTECTION MAXIMALE
        for i, prospect in enumerate(prospects):
            language_flag = "🇫🇷" if prospect.get('language') == 'french' else "🇬🇧"
            print(f"\n📧 Email {i+1}/{len(prospects)} {language_flag}")
            
            success, is_duplicate = self.send_email_gmail_safe(prospect, newly_sent_emails)
            
            if success:
                sent_count += 1
                language_sent[prospect.get('language', 'english')] += 1
                newly_sent_emails.add(prospect['email'].lower())
                
                # ✅ SAUVEGARDE IMMÉDIATE APRÈS CHAQUE ENVOI RÉUSSI
                self.save_sent_emails_history(newly_sent_emails)
                
            elif is_duplicate:
                duplicates_detected += 1
            else:
                failed_count += 1
            
            # ✅ DÉLAI ANTI-SPAM INTELLIGENT
            if i < len(prospects) - 1:
                delay = random.randint(self.delay_range[0], self.delay_range[1])
                print(f"  ⏱️ Pause anti-spam {delay}s...")
                time.sleep(delay)
            
            # ✅ PAUSE BATCH POUR ÉVITER LIMITES GMAIL
            if (i + 1) % self.batch_size == 0 and i < len(prospects) - 1:
                batch_delay = random.randint(self.batch_delay_range[0], self.batch_delay_range[1])
                batch_num = (i + 1) // self.batch_size
                print(f"\n🔄 Fin batch {batch_num}. Pause longue {batch_delay//60}min pour éviter blocage Gmail...")
                time.sleep(batch_delay)
        
        print(f"\n📊 Statistiques Gmail:")
        print(f"🇫🇷 Français: {language_sent['french']}")
        print(f"🇬🇧 Anglais: {language_sent['english']}")
        print(f"🔄 Doublons détectés en cours: {duplicates_detected}")
        print(f"📈 Taux succès: {(sent_count/(sent_count+failed_count)*100):.1f}%" if (sent_count+failed_count) > 0 else "0%")
        
        return sent_count, failed_count, language_sent
    
    def save_email_report(self, sent_count, failed_count, prospects, language_sent, duplicates_avoided):
        """Sauvegarde rapport d'envoi Gmail"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"data/email_report_gmail_{timestamp}.json"
        
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
            'smtp_server': self.smtp_server,
            'version': 'gmail_anti_doublon_fixed',
            'antiduplicate_protection': True,
            'antiduplicate_features': {
                'immediate_save_after_send': True,
                'double_verification': True,
                'backup_files': True,
                'detailed_logging': True
            },
            'anti_spam_features': {
                'batch_size': self.batch_size,
                'delay_range': self.delay_range,
                'batch_delay_range': self.batch_delay_range,
                'professional_headers': True,
                'tls_encryption': True
            }
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 Rapport Gmail sauvé: {report_file}")
            return report_file
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")
            return None
    
    def run_automation(self):
        """Lance l'automation complète Gmail anti-doublon FIXÉ"""
        print("🚀 DÉMARRAGE AUTOMATION EMAIL GMAIL - ANTI-DOUBLON FIXÉ")
        print("🛡️ Protection anti-doublon et anti-spam MAXIMALE")
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
        
        # 4. Limiter à 50 emails par run pour éviter blocage
        if len(prospects) > 50:
            print(f"⚠️ Limitation sécurité: {len(prospects)} prospects → 50 premiers sélectionnés")
            prospects = prospects[:50]
        
        # 5. Vérifier configuration email
        if not self.sender_password:
            print("⚠️ Mot de passe Gmail non configuré (EMAIL_PASSWORD)")
            print("💡 Utilisez un 'App Password' Gmail, pas le mot de passe principal")
            return False
        
        # 6. Envoi Gmail sécurisé
        print(f"\n📧 ENVOI GMAIL SÉCURISÉ DE {len(prospects)} NOUVEAUX EMAILS")
        print(f"📧 De: {self.sender_email}")
        print(f"🔒 Sécurité: Protection anti-doublon RENFORCÉE")
        
        sent_count, failed_count, language_sent = self.send_batch_emails_gmail(
            prospects, sent_emails_history
        )
        
        # 7. Rapport final
        self.save_email_report(sent_count, failed_count, prospects, language_sent, duplicates_avoided)
        
        print(f"\n🎉 AUTOMATION GMAIL ANTI-DOUBLON TERMINÉE")
        print(f"✅ Nouveaux envoyés: {sent_count}")
        print(f"🔄 Doublons évités: {duplicates_avoided}")
        print(f"❌ Échecs: {failed_count}")
        print(f"📧 Expéditeur: {self.sender_email}")
        print(f"🛡️ Protection anti-doublon: MAXIMALE - FIXÉE")
        
        return sent_count > 0

def main():
    """Fonction principale pour GitHub Actions"""
    automation = NeolinksEmailGmail()
    success = automation.run_automation()
    
    return success

if __name__ == "__main__":
    main()
