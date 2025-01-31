import json
from pathlib import Path


data_file = Path("artifacts.json")

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

objects = data['object']
obj = objects[0]

artifacts = filter(lambda x: x['type'] == 'Coin', objects)

new_artifacts = []
for artifact in artifacts:
    new_artifact = {}
    if artifact.get('image'):
        artifact.pop('image')

    for k,v in artifact.items():
        if v:
            new_artifact[k] = v
    new_artifacts.append(new_artifact)


print(json.dumps(new_artifacts, indent=4))
