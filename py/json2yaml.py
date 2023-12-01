import yaml
import json

with open("list-pharmacies.json") as json_file:
    json_data = json.load(json_file)

with open("list-pharmacies.yml", "w") as yaml_file:
    yaml.dump(json_data, yaml_file, allow_unicode=True, default_flow_style=False)
