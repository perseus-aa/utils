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


class Db:
    def __init__(self, artifact_file, image_file):
        with open(image_file, 'r') as f:
            self.images = json.load(f)

        with open(artifact_file, 'r') as f:
            self.artifacts = json.load(f)


    def obj_by_id(self, obj_id):
        return filter(lambda x: x.get('id') == obj_id, self.artifacts)

    def obj_name(self, obj_id):
        objects = self.obj_by_id(obj_id)
        return next(objects)['name']

    def imgs_by_name(self, name):
        return filter(lambda x: x.get('name') and name in x.get('name'), self.images)

    def obj_images(self, obj_id):
        obj_name = self.obj_name(obj_id)
        return self.imgs_by_name(obj_name)


    def obj_image_map(self):
        imap = {}

        for artifact in self.artifacts:
            a_id = artifact['id']

            if imap.get(a_id) is None:
                imap[a_id] = []

            for i in self.obj_images(a_id):
                imap[a_id].append(i['id'])

        return imap



data_dir = Path("/Users/wulfmanc/gh/perseus-aa/json")
images_f = data_dir / Path('images.json')
vases_f = data_dir / Path('vases.json')

db = Db(vases_f, images_f)




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
        
        
    
