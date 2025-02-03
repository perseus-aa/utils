""" Tools for working with images and image metadata.

The original XML data has been converted into JSON files.
In addition, XQuery was used to add a name field to each
image record, where name is the name of the object the image
represents.


What we really want here is a index of {objid: [imgid]

"""

from functools import partial
from pathlib import Path
import json
import sys

data_dir = Path("/Users/wulfmanc/gh/perseus-aa/utils/data")
images_f = data_dir / Path('images.json')
vases_f = data_dir / Path('vases.json')



with open(images_f) as f:
    images = json.load(f)

with open(vases_f) as f:
    vases = json.load(f)


def retrieve_by_prop(prop, val, dict_list):
    return filter(lambda x: x.get(prop) == val, dict_list)

img_by_name = partial(retrieve_by_prop, "name", dict_list=images)

obj_by_id = partial(retrieve_by_prop, 'id', dict_list=vases)

def object_images(object_id):
    object = next(obj_by_id(object_id))
    return img_by_name(object['name'])
    

def object_image_map(objects, images):
    imap = {}
    for o in objects:
        if imap.get(o['id']) is None:
            imap[o['id']] = []

        for i in object_images(o['id']):
            imap[o['id']].append(i['id'])
    return imap



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog = "map_images",
        description = "creates index of artifact ids and image ids")

    parser.add_argument("imagefile")
    parser.add_argument("artifactfile")

    args = parser.parse_args()

    imgfile = Path(args.imagefile)
    artifactfile = Path(args.artifactfile)


    with open(imgfile, 'r') as f:
        images = json.load(f)

    with open(artifactfile, 'r') as f:
        artifacts = json.load(f)


    artifact_image_map = object_image_map(artifacts, images)

    json.dump(artifact_image_map, sys.stdout, indent=4)
        
        
    
