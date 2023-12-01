import xml.etree.ElementTree as ET
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def find_broken_images(url):
    broken_images = []

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            img_url = img.get('src')
            if not img_url or img_url.startswith('data:') or 'fallback' not in img_url:
                continue

            full_url = urljoin(url, img_url)
            try:
                img_response = requests.head(full_url)
                if img_response.status_code != 200:
                    broken_images.append(full_url)
            except requests.RequestException:
                # Fehler bei der Verarbeitung der URL
                print(f"Fehler beim Überprüfen des Bildes: {full_url}")

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

def ensure_directory_exists(file_path):
    """
    Stellt sicher, dass das Verzeichnis für die angegebene Datei existiert.
    Erstellt das Verzeichnis, falls es nicht existiert.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_to_file(file_path, page_url, broken_images):
    """
    Schreibt die kaputten Bild-URLs und die Seiten-URLs, auf denen sie gefunden wurden, in eine Datei.
    """
    with open(file_path, 'a') as file:
        for img in broken_images:
            file.write(f"{page_url} -> {img}\n")

# Sitemap-URL
sitemap_url = 'https://www.digestio.de/sitemap.xml'

# Verzeichnispfad für die Ergebnisse auf der gleichen Ebene wie das Skript
script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'findings')
results_file = 'results.txt'
results_path = os.path.join(results_dir, results_file)

# Neuer Dateipfad für distinct Ergebnisse
results_distinct_file = 'results_distinct.txt'
results_distinct_path = os.path.join(results_dir, results_distinct_file)

try:
    start_time = time.time()  # Start der Zeitmessung

    # Stelle sicher, dass das Verzeichnis existiert
    ensure_directory_exists(results_path)
    print("Verzeichnis für Ergebnisse überprüft und bereit.")

    # URLs aus der Sitemap extrahieren
    print(f"Lade Sitemap von {sitemap_url}...")
    all_pages = get_urls_from_sitemap(sitemap_url)
    print(f"Anzahl gefundener Seiten in der Sitemap: {len(all_pages)}")

    # Überprüfen aller Seiten auf kaputte Bilder und in Datei schreiben
    for page in all_pages:
        print(f"Überprüfe {page} auf kaputte Bilder...")
        broken_images = find_broken_images(page)
        if broken_images:
            print(f"Gefundene kaputte Bilder: {len(broken_images)}")
            write_to_file(results_path, page, broken_images)
        else:
            print("Keine kaputten Bilder gefunden.")


    # Einzigartige Ergebnisse verarbeiten und in einer neuen Datei speichern
    with open(results_path, 'r') as file:
        unique_images = set(file.readlines())

    with open(results_distinct_path, 'w') as file:
        file.writelines(unique_images)
    
    print(f"Einzigartige kaputte Bilder wurden in {results_distinct_path} gespeichert.")

    end_time = time.time()  # Ende der Zeitmessung
    total_time = end_time - start_time
    print(f"Laufzeit des Programms: {total_time:.2f} Sekunden")

except KeyboardInterrupt:
    print("Skript wurde manuell unterbrochen.")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")