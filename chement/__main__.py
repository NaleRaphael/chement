from argparse import ArgumentParser
import requests
import traceback as tb

from .core import (MeshRDFRequest, MeshRDFResponse, QueryTerm2UI, 
                   MeshSearchRequest, MeshSearchResponse, 
                   MeshESearchRequest, MeshESearchResponse,
                   ChebiSearchRequest, ChebiSearchResponse,
                   EntrezSearchRequest, EntrezSearchResponse)
from .parser import (MeshSubjectIDParser, ChebiObjectParser, EntrezObjectParser, 
                     MeshObjectParser, MeshESearchObjectParser)


def parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='db', help='target database')
    subparsers.required = True  # user should sepcify a subparse to be used

    # Parser for MeSH database
    parser_mesh = subparsers.add_parser('mesh', help='MeSH database')
    parser_mesh.add_argument('term', metavar='term', type=str, default='', nargs='?',
                             help='Name or synonym of a subject to be searched.')
    parser_mesh.add_argument('--exactMatch', action='store_true', 
                             help='Add this flag to search items exactly matching with `term`.')
    parser_mesh.add_argument('--rdf', action='store_true', 
                             help='Add this flag to search on Mesh RDF service.')
    parser_mesh.add_argument('--url', action='store_true',
                             help='Add this flag to show url of query.')
    parser_mesh.add_argument('--esearch', action='store_true',
                             help='Add this flag to search by eutils (same as Entrez)')

    # Parser for ChEBI database
    parser_chebi = subparsers.add_parser('chebi', help='ChEBI database')
    parser_chebi.add_argument('term', metavar='term', type=str, default='', nargs='?', 
                              help='Name or synonym of a subject to be searched.')
    parser_chebi.add_argument('--exactMatch', action='store_true',
                              help='Add this flag to search items exactly matching with `term`.')
    parser_chebi.add_argument('--url', action='store_true',
                              help='Add this flag to show url of query.')

    # Parser for Entrez database
    parser_entrez = subparsers.add_parser('entrez', help='Entrez database')
    parser_entrez.add_argument('term', metavar='term', type=str, default='', nargs='?',
                               help='Name of a subject ot be searched.')
    parser_entrez.add_argument('--human', action='store_true',
                               help='Add this flag to search items only belongs human.')
    parser_entrez.add_argument('--url', action='store_true',
                               help='Add this flag to show url of query.')

    args = parser.parse_args()
    return args


def get_mesh_uid(args):
    term = args.term if args.term != '' else 'Cardiomegaly'  # for demo

    if args.rdf:
        if args.exactMatch:
            term = '^{}$'.format(term)
        query = QueryTerm2UI(term=term).build()
        meshreq = MeshRDFRequest(query=query)
        resp = meshreq.get_response()
        meshresp = MeshRDFResponse(resp, MeshSubjectIDParser)
    elif args.esearch:
        meshreq = MeshESearchRequest(query=term, exact=args.exactMatch)
        resp = meshreq.get_response()
        meshresp = MeshESearchResponse(resp, MeshESearchObjectParser)
    else:
        meshreq = MeshSearchRequest(query=term, exact=args.exactMatch)
        resp = meshreq.get_response()
        meshresp = MeshSearchResponse(resp, MeshObjectParser)

    if args.url:
        print(resp.url)
        print('----------')

    for obj in meshresp.content:
        print(obj)


def get_chebi_uid(args):
    term = args.term if args.term != '' else 'asparagine'

    chebireq = ChebiSearchRequest(query=term, exact=args.exactMatch)
    resp = chebireq.get_response()
    chebiresp = ChebiSearchResponse(resp, ChebiObjectParser)

    if args.url:
        print(resp.url)
        print('----------')

    for obj in chebiresp.content:
        print(obj)


def get_entrez_uid(args):
    """
    Query frequency limit:
        Without an API key: 3 query/sec
        with an API key: 10 query/sec

    ELink (Entrez links)
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?

    ```
    Upload steps that generate a web environment and query key

    esearch.fcgi?db=database&term=query&usehistory=y
    ```
    """
    term = args.term if args.term != '' else 'Rab10'

    entrezreq = EntrezSearchRequest(query=term, human_only=args.human)
    resp = entrezreq.get_response()
    entrezresp = EntrezSearchResponse(resp, EntrezObjectParser)

    if args.url:
        print(resp.url)
        print('----------')

    for obj in entrezresp.content:
        print(obj)


# Given args.db to select corresponding function entry
FUNC_ENTRY = {
    'mesh': get_mesh_uid,
    'chebi': get_chebi_uid,
    'entrez': get_entrez_uid
}

if __name__ == '__main__':
    try:
        args = parse_args()
        FUNC_ENTRY[args.db](args)
    except:
        raise
