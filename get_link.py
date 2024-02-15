import os
import requests
import zipfile

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

base_url = "https://s22.anime-sama.me/s1/scans/Frieren/"
start_chapter = 8  # Le chapitre de départ
end_chapter = 9    # Le dernier chapitre
number_of_pages = n  # Le nombre de pages dans chaque chapitre

for chapter in range(start_chapter, end_chapter + 1):
    for page in range(1, number_of_pages + 1):
        page_url = f"{base_url}{chapter}/{str(page).zfill(2)}.jpg"
        print(page_url)


number_chapitre = 118
for c in range(1, number_chapitre+1):

    base_url = "https://s22.anime-sama.me/s1/scans/Frieren/9/"
    number_of_pages = 19  # Remplacez 'n' par le nombre de pages souhaité


    links = []
    for page_number in range(1, number_of_pages + 1): 
        page_url = f"{base_url}{str(page_number).zfill(2)}.jpg"
        links.append(page_url)

    links_final = [[9, links]]

    download_images(links_final)

# create_cbz('./downloaded_manga')
create_cbz('./downloaded_manga')