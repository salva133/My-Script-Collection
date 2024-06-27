import os

# Zu ersetzende Substrings
replacements = {
    ":USA": ":OCE",
    ":MEX": ":OCE",
    ":HBC": ":OCE",
    ":HAW": ":OCE",
    ":ONT": ":OCE",
    ":NBS": ":OCE",
    ":NVS": ":OCE",
    ":QUE": ":OCE",
    ":GBR": ":ASO",
    ":ORG": ":OCE",
    ":TEX": ":OCE",
    ":SEQ": ":OCE",
    ":RUS": ":EUR",
    ":CHI": ":EAS"
}

# Funktion zum Ersetzen der Substrings in einer Datei
def replace_in_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.write(content)
        print(f"Bearbeitet: {file_path}")

# Durchsuche das aktuelle Arbeitsverzeichnis und seine Unterverzeichnisse
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            replace_in_file(file_path, replacements)

print("Ersetzung abgeschlossen.")
