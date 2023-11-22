import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_broken_images(url):
    """
    Diese Funktion sucht nach kaputten Bildern auf der angegebenen URL.
    """
    broken_images = []

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            img_url = img.get('src')
            if not img_url:
                continue

            full_url = urljoin(url, img_url)
            img_response = requests.head(full_url)
            if img_response.status_code != 200:
                broken_images.append(full_url)

    except requests.RequestException as e:
        print(f"Ein Fehler ist aufgetreten beim Abrufen der URL {url}: {e}")

    return broken_images

def get_urls_from_sitemap(sitemap_url):
    """
    Diese Funktion lädt die Sitemap und extrahiert alle URLs.
    """
    urls = set()

    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        sitemap = ET.fromstring(response.content)

        for url in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            urls.add(loc)

    except requests.RequestException as e:
        print(f"Ein Fehler ist aufgetreten beim Abrufen der Sitemap: {e}")

    return urls

# Sitemap-URL
sitemap_url = 'https://www.digestio.de/sitemap.xml'

# URLs aus der Sitemap extrahieren
all_pages = get_urls_from_sitemap(sitemap_url)

# Überprüfen aller Seiten auf kaputte Bilder
for page in all_pages:
    broken_images = find_broken_images(page)
    if broken_images:
        print(f"Kaputte Bilder auf {page}:")
        for img in broken_images:
            print(img)
    else:
        print(f"Keine kaputten Bilder auf {page}.")
