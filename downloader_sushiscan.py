import os
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import zipfile

def create_cbz(dossier_parent, intervalle=10):
    chapitres = [d for d in os.listdir(dossier_parent) if os.path.isdir(os.path.join(dossier_parent, d))]
    chapitres.sort() 

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

def download_images(chapter_links, base_dir='downloaded_manga'):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    chapters_without_images = []

    for chapter_number, links in tqdm(chapter_links, desc="Téléchargement des chapitres"):
        if not links:
            chapters_without_images.append(chapter_number)
            continue

        chapter_dir = os.path.join(base_dir, f'Chapitre_{chapter_number.replace(".", "_")}')
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        images_downloaded = False
        for i, link in enumerate(tqdm(links, desc=f"Chapitre {chapter_number}")):
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    with open(os.path.join(chapter_dir, f'image_{i}.jpg'), 'wb') as f:
                        f.write(response.content)
                        images_downloaded = True
            except Exception as e:
                print(f"Erreur lors du téléchargement de l'image {i} du chapitre {chapter_number}: {e}")

        if not images_downloaded:
            chapters_without_images.append(chapter_number)

    return chapters_without_images

def find_image_links(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_elements = soup.find_all('img')
    image_links = [img['src'].strip() for img in image_elements if img.get('src')]
    return image_links

def get_all_chapter_links(manga_page_url, based_ddb_link, driver):
    driver.get(manga_page_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Trouve tous les liens de chapitre dans la page
    chapter_elements = soup.find_all('a', href=True)
    chapter_urls = [elem['href'] for elem in chapter_elements if 'chapitre' in elem['href']]

    # Extraction des numéros de chapitre
    def chapter_number_key(url):
        match = re.search(r'chapitre-(\d+(?:-\d+)?)', url)
        if match:
            return tuple(map(int, match.group(1).replace('-', '.').split('.')))
        return (0, 0)

    # Trie les chapitres par numéro
    chapter_urls_sorted = sorted(chapter_urls, key=chapter_number_key)

    all_chapter_links = []

    for chapter_url in tqdm(chapter_urls_sorted, desc="Récupération des liens de chapitres"):
        match = re.search(r'chapitre-(\d+(?:-\d+)?)', chapter_url)
        if match:
            chapter_number = match.group(1).replace('-', '.')
            image_links = find_image_links(driver, chapter_url)
            manga_image_links = [link for link in image_links if link.startswith(based_ddb_link)]
            all_chapter_links.append((chapter_number, manga_image_links))
        else:
            print(f"Aucun numéro de chapitre trouvé pour l'URL : {chapter_url}")

    return all_chapter_links

def main(based_ddb_link, manga_page_url):

    # Configuration de Selenium
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    chapter_links = get_all_chapter_links(manga_page_url, based_ddb_link, driver)

    # Affichage des liens filtrés
    for chapter_data in chapter_links:
        chapter_number, links = chapter_data

    driver.quit()

    chapters_without_images = download_images(chapter_links)

    # Affichage des chapitres sans images
    if chapters_without_images:
        print("Aucune image trouvée pour les chapitres suivants :")
        for chapter in chapters_without_images:
            print(f"Chapitre {chapter}")
    else:
        print("Des images ont été trouvées et téléchargées pour tous les chapitres.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharge des images de manga depuis une URL donnée.")
    parser.add_argument("based_ddb_link", help="URL de base des images du manga")
    parser.add_argument("manga_page_url", help="URL de la page principale du manga")

    args = parser.parse_args()
    main(args.based_ddb_link, args.manga_page_url)

based_ddb_link = "https://s22.anime-sama.me"

# URL de la page principale du manga
# manga_page_url = 'https://sushiscan.fr/manga/blue-lock-episode-nagi/'

# exemple : python3 downloader_sushiscan.py "https://s22.anime-sama.me" "https://sushiscan.net/catalogue/frieren/"



