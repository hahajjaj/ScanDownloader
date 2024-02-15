import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import zipfile
import re
import time

def download_images(chapter_links, base_dir='downloaded_manga'):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for chapter_number, links in chapter_links:
        chapter_dir = os.path.join(base_dir, f'Chapitre_{chapter_number}')
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        for i, link in enumerate(links):
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    with open(os.path.join(chapter_dir, f'image_{i}.jpg'), 'wb') as f:
                        f.write(response.content)
            except Exception as e:
                print(f"Erreur lors du téléchargement de l'image : {e}")

def find_image_links(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_elements = soup.find_all('img')
    image_links = [img['data-src'].strip() for img in image_elements if img.get('data-src')]
    return image_links


def get_chapter_links(start_chapter, end_chapter, base_url_template, driver):
    all_chapter_links = []
    for chapter in range(start_chapter, end_chapter + 1):
        chapter_url = base_url_template.replace('ch-x', f'ch-{chapter}')
        image_links = find_image_links(driver, chapter_url)
        manga_image_links = [link for link in image_links if link.startswith("https://stockage.manga-scantrad")]
        
        if not manga_image_links:
            chapter_url = base_url_template.replace('ch-x', f'chapitre-{chapter}')
            image_links = find_image_links(driver, chapter_url)
            manga_image_links = [link for link in image_links if link.startswith("https://stockage.manga-scantrad")]

        # Ajout du numéro de chapitre à la liste des liens
        chapter_data = [chapter, manga_image_links]
        all_chapter_links.append(chapter_data)
        
    return all_chapter_links


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get('https://manga-scantrad.io/')
input("Résolvez le CAPTCHA et appuyez sur Entrée dans cette console pour continuer...")

start_chapter = 11
end_chapter = 50
base_url = 'https://manga-scantrad.io/manga/sousou-no-frieren/ch-x/'
# Obtention des liens de chapitre
chapter_links = get_chapter_links(start_chapter, end_chapter, base_url, driver)

for chapter_data in chapter_links:
    chapter_number, links = chapter_data
    print(f"Chapitre {chapter_number}:")
    for link in links:
        print(link)
print(len(chapter_links))

driver.quit()

# Téléchargement des images
download_images(chapter_links)

def create_cbz(dossier_parent, intervalle=10):
    chapitres = [d for d in os.listdir(dossier_parent) if os.path.isdir(os.path.join(dossier_parent, d))]
    chapitres.sort()  # Assurez-vous que les chapitres sont triés dans l'ordre

    for i in range(0, len(chapitres), intervalle):
        chapitres_selectionnes = chapitres[i:i + intervalle]
        nom_fichier_cbz = f"Chapitres_{i+1}_à_{i+len(chapitres_selectionnes)}.cbz"

        with zipfile.ZipFile(nom_fichier_cbz, 'w') as zipf:
            for chap in chapitres_selectionnes:
                dossier_chap = os.path.join(dossier_parent, chap)
                for fichier in os.listdir(dossier_chap):
                    if fichier.lower().endswith(('.png', '.jpg', '.jpeg')):
                        chemin_fichier = os.path.join(dossier_chap, fichier)
                        zipf.write(chemin_fichier, arcname=os.path.join(chap, fichier))

        print(f"Fichier {nom_fichier_cbz} créé avec succès.")

# Utilisez la fonction comme suit
create_cbz('./downloaded_manga')