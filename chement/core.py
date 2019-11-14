import logging
import requests
from .config import MeshConfiguration, ChebiConfiguration, EntrezConfiguration
from .parser import BasicParser, ChebiObjectParser
from .objbase import MeshObject
from .sparql import SparqlQuery, QueryTerm2UI

__all__ = ['MeshURI', 'MeshRDFRequest', 'MeshRDFResponse', 'MeshSearchRequest', 'MeshSearchResponse',
           'ChebiRequest', 'ChebiSearchResponse', 'EntrezSearchRequest', 'EntrezSearchResponse',
           'MeshESearchRequest', 'MeshESearchResponse']


MeshConfig = MeshConfiguration().load()
ChebiConfig = ChebiConfiguration().load()
EntrezConfig = EntrezConfiguration().load()

class BaseRequest(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('This method should be implemented by child class.')

    def get_response(self):
        raise NotImplementedError('This method should be implemented by child class.')


class BaseResponse(object):
    def __init__(self, response, parser, **kwargs):
        if not isinstance(response, requests.Response):
            raise TypeError('Type of given response should be `requests.Response`.')
        self.response = response
        self.parser = parser()
        self.content = None
        self.parse()

    def parse(self):
        try:
            self.content = self.parser.parse(self.response)
        except Exception as ex:
            print(self.response.url)
            logging.exception(ex)
            self.content = []


class MeshURI(object):
    @classmethod
    def build(cls, limit, year, format, inference, query, offset):
        uri = MeshConfig.sparql.base_url + '?'
        uri += 'query={}'.format(query)
        uri += 'limit={}'.format(limit)
        uri += 'year={}'.format(year)
        uri += 'inference={}'.format(inference)
        uri += 'offset={}'.format(offset)
        return uri


class MeshRDFRequest(BaseRequest):
    def __init__(self, fmt='json', inference=True, limit=10, 
                 offset=0, query='', year='current'):
        if not isinstance(query, SparqlQuery):
            raise TypeError('Given `query` should be an instance of `SparqlQuery`.')

        self.fmt = fmt
        self.inference = inference
        self.limit = limit
        self.inference = 'true' if inference else 'false'
        self.limit = limit
        self.offset = offset
        self.query = query
        self.year = year

    def get_response(self):
        uri = MeshConfig.sparql.base_url + '?'
        payload = {
            'query': self.query,
            'limit': self.limit,
            'year': self.year,
            'format': self.fmt,
            'inference': self.inference,
            'offset': self.offset
        }
        resp = None
        try:
            resp = requests.get(uri, params=payload)
        except ex:
            logging.exception(ex)
        finally:
            return resp


class MeshRDFResponse(BaseResponse):
    def __init__(self, response, parser):
        super(MeshRDFResponse, self).__init__(response, parser)


class MeshSearchRequest(BaseRequest):
    def __init__(self, query='', exact=True):
        self.query = query
        self.exact = exact

    def get_response(self):
        d = MeshConfig.search.option
        uri = MeshConfig.search.base_url + '?' + MeshConfig.search.query.format(query=self.query)
        payload = {
            "searchInField": d.searchInField.terms[1],      # "termDescriptor"
            "size": d.size,
            "searchType": d.searchType[0] if self.exact else d.searchType[2],
            "searchMethod": d.searchMethod[0],      # "FullWord"
            "sort": d.sort.Relevance
        }
        resp = None
        try:
            resp = requests.get(uri, params=payload)
        except ex:
            logging.exception(ex)
        finally:
            return resp


class MeshSearchResponse(BaseResponse):
    def __init__(self, response, parser):
        super(MeshSearchResponse, self).__init__(response, parser)


class MeshESearchRequest(BaseRequest):
    def __init__(self, query='', exact=True, api_key=None):
        self.query = query
        self.exact = exact
        self.api_key = MeshConfig.api_key if api_key is None else api_key

    def get_response(self):
        d = MeshConfig.esearch.option
        uri = MeshConfig.esearch.base_url + '?' + MeshConfig.esearch.query.format(query=self.query)

        if self.exact:
            uri += '+AND+{}'.format(MeshConfig.esearch.cond.orgn_human)

        payload = {k: d.get(k) for k in d.keys()}
        if self.api_key is not None:
            payload['api_key'] = self.api_key

        resp = None
        try:
            resp = requests.get(uri, params=payload)
        except ex:
            logging.exceotion(ex)
        finally:
            return resp


class MeshESearchResponse(BaseResponse):
    def __init__(self, response, parser):
        super(MeshESearchResponse, self).__init__(response, parser)


class ChebiSearchRequest(BaseRequest):
    def __init__(self, query='', exact=True):
        self.query = query
        self.exact = exact

    def get_response(self):
        d = ChebiConfig.search.option
        uri = ChebiConfig.search.base_url + '?' + ChebiConfig.search.query.format(query=self.query)

        payload = {k: d.get(k) for k in d.keys()}
        payload['exact'] = 'true' if self.exact else 'false'

        resp = None
        try:
            resp = requests.get(uri, params=payload)
        except ex:
            logging.exception(ex)
        finally:
            return resp


class ChebiSearchResponse(BaseResponse):
    def __init__(self, response, parser):
        super(ChebiSearchResponse, self).__init__(response, parser)


class EntrezSearchRequest(BaseRequest):
    def __init__(self, query='', api_key=None, human_only=True):
        self.query = query
        self.api_key = EntrezConfig.api_key if api_key is None else api_key
        self.human_only = human_only

    def get_response(self):
        d = EntrezConfig.esearch.option
        uri = EntrezConfig.esearch.base_url + '?' + EntrezConfig.esearch.query.format(query=self.query)

        # Search genes that only in human
        if self.human_only:
            uri += '+AND+{}'.format(EntrezConfig.esearch.cond.orgn_human)

        payload = {k: d.get(k) for k in d.keys()}
        if self.api_key is not None:
            payload['api_key'] = self.api_key

        resp = None
        try:
            resp = requests.get(uri, params=payload)
        except ex:
            logging.exception(ex)
        finally:
            return resp


class EntrezSearchResponse(BaseResponse):
    def __init__(self, response, parser):
        super(EntrezSearchResponse, self).__init__(response, parser)


if __name__ == '__main__':
    query = 'Rab10'
    req = EntrezSearchRequest(query)
    resp = EntrezSearchRequest(req.get_response(), ChebiObjectParser)
    import pdb; pdb.set_trace()
    print(resp)
