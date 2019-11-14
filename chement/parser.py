from .objbase import MeshObject, ChebiObject, EntrezObject, MeshESearchObject


__all__ = ['BasicParser', 'MeshSubjectIDParser', 'MeshObjectParser',
           'ChebiObjectParser', 'EntrezObjectParser', 'MeshESearchObjectParser']


class BasicParser(object):
    def parse(self, resp):
        return resp


class MeshSubjectIDParser(BasicParser):
    def parse(self, resp):
        result = resp.json()['results']['bindings']

        n_result = len(result)
        if n_result == 0:
            return []
        else:
            obj_list = []
            for i in range(n_result):
                meshobj = MeshObject(
                        result[i]['ui']['value'],
                        result[i]['label']['value'],
                        result[i]['plabel']['value']
                    )
                obj_list.append(meshobj)
            return obj_list


class MeshObjectParser(BasicParser):
    def parse(self, resp):
        result = resp.json()['hits']['hits']

        n_result = len(result)
        if n_result == 0:
            return []
        else:
            obj_list = []
            for i in range(n_result):
                cptlist = result[i]['_source']['ConceptList']['Concept']
                plabel = ''.join([cpt['ConceptName']['String']['t'] for cpt in cptlist])
                meshobj = MeshObject(
                        result[i]['_id'],
                        result[i]['_source']['_generated']['RecordName'],
                        plabel
                    )
                obj_list.append(meshobj)
            return obj_list


class MeshESearchObjectParser(BasicParser):
    def parse(self, resp):
        result = resp.json()['esearchresult']   # ESearch result

        n_result = int(result['retmax'])
        if n_result == 0:
            return []
        else:
            obj_list = []
            for i in range(n_result):
                entrezobj = MeshESearchObject(id_=result['idlist'][i])
                obj_list.append(entrezobj)
            return obj_list


class ChebiObjectParser(BasicParser):
    def parse(self, resp):
        result = resp.json()

        n_result = result['response']['numFound']
        if n_result == 0:
            return []
        else:
            obj_list = []
            docs = result['response']['docs']
            for doc in docs:
                chebiobj = ChebiObject(
                        id_=doc['id'],
                        iri=doc['iri'],
                        short_form=doc['short_form'],
                        obo_id=doc['obo_id'],
                        label=doc['label'],
                        ontology_name=doc['ontology_name'],
                        ontology_prefix=doc['ontology_prefix'],
                        type_=doc['type']
                    )
                obj_list.append(chebiobj)
            return obj_list


class EntrezObjectParser(BasicParser):
    def parse(self, resp):
        result = resp.json()['esearchresult']   # ESearch result

        n_result = int(result['retmax'])
        if n_result == 0:
            return []
        else:
            obj_list = []
            for i in range(n_result):
                entrezobj = EntrezObject(id_=result['idlist'][i])
                obj_list.append(entrezobj)
            return obj_list
