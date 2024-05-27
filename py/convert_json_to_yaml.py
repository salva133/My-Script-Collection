"""
Script Name: json2yaml.py
Description: This script converts a JSON file into a YAML file. It is designed to facilitate data transformation between these two popular formats, making it easier to work with configuration files, data exchange between languages, or for use in applications that require YAML format.

Usage:
    - The script currently converts 'list-pharmacies.json' to 'list-pharmacies.yml'.
    - To convert a different JSON file, replace 'list-pharmacies.json' with the path to the desired file.
    - The output YAML will be named 'list-pharmacies.yml', but this can be changed to any desired output file name.
"""


import yaml
import json

with open("list-pharmacies.json") as json_file:
    json_data = json.load(json_file)

with open("list-pharmacies.yml", "w") as yaml_file:
    yaml.dump(json_data, yaml_file, allow_unicode=True, default_flow_style=False)
