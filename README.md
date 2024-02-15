# Téléchargeur de Scans SushiScan avec Support CBZ et PDF

Ce script Python permet de télécharger automatiquement des scans de mangas depuis le site SushiScan. Il offre la flexibilité de regrouper les scans téléchargés en fichiers CBZ ou PDF, selon le choix de l'utilisateur, par un nombre défini de chapitres. Cette fonctionnalité rend la gestion et la lecture de vos mangas préférés à la fois pratique et agréable.

## Fonctionnalités Principales

* Téléchargement Automatique des Scans : Téléchargez les derniers chapitres de vos mangas préférés directement depuis SushiScan.
* Support Multi-Format : Choisissez de regrouper les chapitres téléchargés en fichiers CBZ ou PDF, selon votre préférence.
* Groupement Personnalisable : Définissez le nombre de chapitres à inclure dans chaque fichier groupé, adaptant ainsi la lecture à vos habitudes.
* Facilité d'Utilisation : Profitez d'une interface utilisateur conviviale pour une expérience sans tracas.

## Prérequis

* Python 3.x
* Bibliothèques Python : requests, selenium, beautifulsoup4, tqdm, zipfile (certaines sont incluses par défaut avec Python)

Installez les dépendances nécessaires via pip :

```Python
  pip install -r requirements.txt
```

## Installation

* Clonez le dépôt ou téléchargez les fichiers du script.
* Installez les dépendances Python mentionnées ci-dessus.
* Assurez-vous d'avoir le ChromeDriver installé et mis à jour (nécessaire pour selenium).

## Utilisation
Lancez le script depuis le terminal avec les arguments requis :

```python
  python downloader_sushiscan.py based_ddb_link manga_page_url
```

* based_ddb_link : URL de base où les images du manga sont hébergées (trouvable dans le code source de la page).
* manga_page_url : URL de la page principale du manga sur SushiScan.

## Exemple

```python
  python downloader_sushiscan.py "https://s22.anime-sama.me" "https://sushiscan.net/catalogue/frieren/"
```

## Précisions:
Veuillez noter les points suivants concernant l'utilisation et la maintenance du script :

* Durabilité du Script : Il est probable que le script actuel puisse devenir obsolète après un certain temps, en raison d'éventuelles modifications de la structure HTML du site ciblé. Dans ce cas, il serait nécessaire d'ajuster quelques détails du script pour l'aligner sur les changements apportés au site. Si vous possédez des compétences de base en programmation, la mise à jour du script selon ces modifications devrait être réalisable sans difficulté majeure.
* Scripts Supplémentaires : Pour compléter le développement de cet outil, j'ai créé plusieurs scripts additionnels à des fins de test et d'expérimentation. Cependant, il est important de souligner que ces scripts supplémentaires ne sont pas indispensables au fonctionnement principal du script de téléchargement. Ils sont fournis à titre indicatif et peuvent servir d'exemples ou d'outils auxiliaires si vous souhaitez explorer davantage de fonctionnalités.
