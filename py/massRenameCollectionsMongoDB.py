from pymongo import MongoClient

DEBUG = True
URL = 'mongodb://localhost:27017/'
DBname = 'myDatabase'

def DebugMsg(msg):
    if DEBUG:
        print(f"DEBUG: {msg}")

# Verbindung zum MongoDB Server herstellen
client = MongoClient(URL)

# Datenbank auswählen
db = client[DBname]

# Array mit alten Collection-Namen und neuen Collection-Namen
collections_to_rename = [
    ('alter_collection_name1', 'neuer_collection_name1'),
    ('alter_collection_name2', 'neuer_collection_name2'),
    # Füge weitere Collection-Namen hier hinzu
]

# Durch die Liste iterieren und Collections umbenennen
for old_name, new_name in collections_to_rename:
    db[old_name].rename(new_name)
    DebugMsg(f"Collection '{old_name}' wurde in '{new_name}' umbenannt.")

print("Collections wurden umbenannt.")
