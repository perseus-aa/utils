# winnow-images.py
#
# Filters image graph to only include images that are
# on the server.

from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS
import httpx


# Namespaces
AAT = Namespace("http://vocab.getty.edu/aat/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
AA = Namespace("http://perseus.tufts.edu/ns/aa/")
SCHEMA = Namespace("https://schema.org/")
IMAGE = Namespace("https://iiif.perseus.tufts.edu/iiif/3/")


AA_NAMESPACES = {
    "crm" : CRM,
    "aat" : AAT,
    "aa" : AA,
    "image" : IMAGE,
    "schema" : SCHEMA,
    "rdf": RDF,
    "rdfs": RDFS   
    }

ARTIFACT = AAT['300117127']
BUILDING = AAT['building']
COIN = AAT['coin']
GEM = AAT['300011172']
SCULPTURE = AAT['sculpture']
SITE = AAT['site']
VASE = AAT['300132254']

ARTIFACT_TYPES = [BUILDING, COIN, GEM, SCULPTURE, SITE, VASE]

image_rdf_dir = Path("/Users/wulfmanc/repos/gh/perseus-aa/rdf/object_image_graphs")


def base_graph() -> Graph:
    graph:Graph = Graph()
    [graph.bind(k,v) for k,v in AA_NAMESPACES.items()]
    return graph
    
def vase_graph() -> Graph:
    the_graph:Graph = base_graph()
    the_graph.parse(image_rdf_dir / Path("vase_map.ttl"))
    return the_graph


def image_missing(image_uri) -> bool:
    resp = httpx.get(f"{image_uri}/info.json")
    return resp.status_code in [404, 500]

def remove_image_from_graph(uri, graph):
    graph.remove(None, CRM['P138i_is_represented_by'], uri)


    
