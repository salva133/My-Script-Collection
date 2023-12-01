import json
import re

def add_hyphen_before_capitals(s):
    return re.sub(r'(?<=[a-z])[A-Z]', r'-\g<0>', s)

# Lesen Sie die Datei
with open('pharmacies.json', 'r') as f:
    data = json.load(f)

# Füge Bindestriche hinzu
for pharmacy in data:
    if 'Apothekenname' in pharmacy:
        pharmacy['Apothekenname'] = add_hyphen_before_capitals(pharmacy['Apothekenname'])

# Speichern Sie die Datei
with open('pharmacies.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
