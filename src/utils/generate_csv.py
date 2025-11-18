import csv
import json
import httpx

input = "/Users/wulfmanc/gh/perseus-aa/json/artifacts/metadata/vases_r.json"


with open(input, 'r', encoding='utf-8') as f:
    data = json.load(f)
    



field_names: list[str] =[
    'objectid',
    'title',
    'creator',
    'date',
    'description',
    'subject',
    'location',
    'latitude',
    'longitude',
    'source',
    'internet_archive_link',
    'identifier',
    'type',
    'format',
    'language',
    'rights',
    'rightsstatement',
    'display_template',
    'object_location',
    'image_small',
    'image_thumb',
    'image_alt_text',
    'object_transcript',
]

with open("/tmp/v.csv", "w") as f:
    writer = csv.DictWriter(f, field_names)
    writer.writeheader()
    for item in data:
        print(f"converting {item['id']}")
        row:dict[str,str] = {}
        manifest_uri = f"https://iiif-metadata.perseus.tufts.edu/{item['id']}.json"
        r = httpx.get(manifest_uri)
        manifest = json.loads(r.text)
        try:
            thumbnail = manifest['metadata'][0]['value']['en'][0]
            row['image_thumb'] = thumbnail
        except (KeyError, IndexError):
            pass
        
        row['display_template'] = 'iiif'
        row['type'] = "Image;StillImage"
        row['format'] = "image/jpeg"
        row['objectid'] = item['id']
        row['identifier'] = item['id']
        row['title'] = item['name']
        row['source'] = item['type']
        row['object_location'] = f"https://iiif-metadata.perseus.tufts.edu/{item['id']}.json"
        
        writer.writerow(row)
