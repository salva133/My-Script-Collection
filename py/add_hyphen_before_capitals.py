"""
Script Name: add_hyphen_before_capitals.py
Description: This script processes a JSON file containing pharmacy names and modifies each name to insert hyphens before any uppercase letters that follow lowercase letters. This is typically used to improve readability or meet specific formatting requirements.

Functions:
    add_hyphen_before_capitals(s) - Inserts hyphens before uppercase letters that follow lowercase letters in a given string.

Workflow:
    1. Reads a JSON file ('pharmacies.json') containing pharmacy names.
    2. Applies the add_hyphen_before_capitals function to each pharmacy name.
    3. Writes the modified names back to the JSON file, preserving the original format and encoding.
"""


import json
import re


def add_hyphen_before_capitals(s):
    return re.sub(r"(?<=[a-z])[A-Z]", r"-\g<0>", s)


# Lesen Sie die Datei
with open("pharmacies.json", "r") as f:
    data = json.load(f)

# Füge Bindestriche hinzu
for pharmacy in data:
    if "Apothekenname" in pharmacy:
        pharmacy["Apothekenname"] = add_hyphen_before_capitals(
            pharmacy["Apothekenname"]
        )

# Speichern Sie die Datei
with open("pharmacies.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
