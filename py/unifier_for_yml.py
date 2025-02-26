import os
import logging

# Logger Konfiguration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    """Liest eine Datei mit verschiedenen Encodings und gibt den Inhalt zurück."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                logger.debug(f"Erfolgreich gelesen: {file_path} mit Encoding {encoding}")
                return file.read()
        except UnicodeDecodeError:
            logger.warning(f"Fehlgeschlagenes Encoding für Datei {file_path}: {encoding}")
            continue
        except Exception as e:
            logger.error(f"Fehler beim Lesen von {file_path}: {e}")
            return None
    return None

def combine_yml_files(output_file, search_directory):
    """Durchläuft alle Unterverzeichnisse von search_directory und kombiniert .yml-Dateien."""
    if not os.path.exists(search_directory):
        logger.error(f"Das Verzeichnis '{search_directory}' existiert nicht!")
        raise FileNotFoundError(f"Das Verzeichnis '{search_directory}' existiert nicht.")
    
    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.endswith('.yml'):
                    file_path = os.path.join(root, file)
                    content = read_file(file_path)
                    if content:
                        outfile.write(f"# Datei: {file}\n")  # Optional: Dateinamen in der Ausgabe speichern
                        outfile.write(content + '\n')
                        logger.info(f"Inhalt von {file_path} hinzugefügt.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
    search_directory = script_dir  # Durchsuche das Verzeichnis des Skripts rekursiv
    output_file = os.path.join(script_dir, 'combined.yml')  # Speichert das kombinierte File im gleichen Ordner
    
    try:
        logger.info(f"Starte das Zusammenführen von .yml-Dateien in {search_directory}")
        combine_yml_files(output_file, search_directory)
        logger.info(f"Alle .yml-Dateien wurden in {output_file} kombiniert.")
    except FileNotFoundError:
        logger.exception("Fehlgeschlagen: Verzeichnis nicht gefunden.")
    except Exception as e:
        logger.exception(f"Unerwarteter Fehler: {e}")
