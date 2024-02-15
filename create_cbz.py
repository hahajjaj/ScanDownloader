import os
import zipfile
import re

def extract_chapter_parts(chapitre_nom):
    # Cette fonction extrait les numéros du chapitre et de la partie à partir du nom du dossier.
    # Par exemple, "Chapitre_1_1" deviendra (1, 1), "Chapitre_1" deviendra (1, 0).
    parts = re.findall(r'\d+', chapitre_nom)
    parts = [int(part) for part in parts]
    if len(parts) == 1:
        parts.append(0)  # Ajoute un 0 pour les chapitres sans partie.
    return tuple(parts)

def create_cbz(dossier_parent, intervalle=10):
    chapitres = [d for d in os.listdir(dossier_parent) if os.path.isdir(os.path.join(dossier_parent, d))]
    # Tri des chapitres en utilisant la fonction extract_chapter_parts.
    chapitres.sort(key=extract_chapter_parts)

    for i in range(0, len(chapitres), intervalle):
        chapitres_selectionnes = chapitres[i:i + intervalle]
        nom_fichier_cbz = f"Chapitres_{i+1}_à_{i+len(chapitres_selectionnes)}.cbz"

        with zipfile.ZipFile(nom_fichier_cbz, 'w') as zipf:
            for chap in chapitres_selectionnes:
                dossier_chap = os.path.join(dossier_parent, chap)
                for fichier in os.listdir(dossier_chap):
                    if fichier.lower().endswith(('.png', '.jpg', '.jpeg')):
                        chemin_fichier = os.path.join(dossier_chap, fichier)
                        # Ajouter le fichier au zip en conservant la structure des dossiers.
                        zipf.write(chemin_fichier, arcname=os.path.join(chap, fichier))

        print(f"Fichier {nom_fichier_cbz} créé avec succès.")

# Utilisez la fonction comme suit
create_cbz('./FRIEREN')
