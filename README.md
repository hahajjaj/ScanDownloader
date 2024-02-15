# SushiScan Scan Downloader with CBZ and PDF Support

This Python script allows for the automatic downloading of manga scans from the SushiScan website. It offers the flexibility to group downloaded scans into CBZ or PDF files, depending on the user's choice, by a defined number of chapters. This feature makes managing and reading your favorite mangas both convenient and enjoyable.

## Main Features

* Automatic Scan Downloading: Download the latest chapters of your favorite mangas directly from SushiScan.
* Multi-Format Support: Choose to group the downloaded chapters into CBZ or PDF files, according to your preference.
* Customizable Grouping: Define the number of chapters to include in each grouped file, thus tailoring the reading to your habits.
* Ease of Use: Enjoy a user-friendly interface for a hassle-free experience.

## Prerequisites

* Python 3.x
* Python Libraries: requests, selenium, beautifulsoup4, tqdm, zipfile (some are included by default with Python)

Install the necessary dependencies via pip:

```Python
  pip install -r requirements.txt
```

## Installation

* Clone the repository or download the script files.
* Install the above-mentioned Python dependencies.
* Ensure you have ChromeDriver installed and updated (necessary for selenium).

## Usage
Launch the script from the terminal with the required arguments:

```python
  python downloader_sushiscan.py based_ddb_link manga_page_url
```

* based_ddb_link: The base URL where the manga images are hosted (found in the page source code).
* manga_page_url: The main page URL of the manga on SushiScan.

## Example

```python
  python downloader_sushiscan.py "https://s22.anime-sama.me" "https://sushiscan.net/catalogue/frieren/"
```

## Notes:
Please note the following points regarding the use and maintenance of the script:

* Script Durability: There's a chance that the current script may become obsolete over time due to potential changes in the targeted site's HTML structure. In such a case, it would be necessary to adjust a few details of the script to align with the changes made to the site. If you have basic programming skills, updating the script according to these changes should be achievable without significant difficulty.
* Additional Scripts: To complement the development of this tool, I've created several additional scripts for testing and experimentation purposes. However, it's important to emphasize that these extra scripts are not essential for the main downloading script's operation. They are provided for reference and can serve as examples or auxiliary tools if you wish to explore more functionalities.
