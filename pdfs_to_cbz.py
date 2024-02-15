from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from zipfile import ZipFile
import glob
import os

def list_and_sort_pdfs(directory):
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    pdf_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    return pdf_files

def group_files(files, n):
    for i in range(0, len(files), n):
        yield files[i:i + n]

def convert_group_to_cbz(pdf_group, group_index, temp_folder):
    image_files = []
    for pdf_path in pdf_group:
        # Convertir le PDF en images
        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):
            image_filename = f"{temp_folder}/{os.path.basename(pdf_path)}_page_{i}.jpg"
            image.save(image_filename, 'JPEG')
            image_files.append(image_filename)

    cbz_path = f"resultat_group_{group_index}.cbz"
    with ZipFile(cbz_path, 'w') as zipf:
        for file in image_files:
            zipf.write(file, os.path.basename(file))

    # Nettoyer les images temporaires dans le dossier
    for file in image_files:
        os.remove(file)

if __name__ == "__main__":
    directory = "/Users/hamza/Downloads/TBATE/The Beginning after the End"
    pdf_files = list_and_sort_pdfs(directory)
    pdf_groups = list(group_files(pdf_files, 10))
    temp_folder = "temp_images"
    os.makedirs(temp_folder, exist_ok=True)

    for index, group in enumerate(pdf_groups):
        convert_group_to_cbz(group, index, temp_folder)

    os.rmdir(temp_folder)

