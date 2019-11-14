
__all__ = ['Subject', 'MeshObject', 'MeshESearchObject', 'ChebiObject', 'EntrezObject']


class Subject(object):
    pass


class MeshObject(Subject):
    def __init__(self, ui=None, label=None, plabel=None):
        """
        Default object for storing returned result from MeSH RDF.

        Parameters
        ----------
        ui : str
            Unique ID of a subject.
        label : str
            Descriptor of a subject.
        plabel : str
            Term (preferred label) of a subject.
        """
        self.ui = ui
        self.uid = 'MeSH:{}'.format(self.ui)    # formatted ui
        self.label = label
        self.plabel = plabel

    def __str__(self):
        return 'uid: {}, label: {}, plabel: {}'.format(self.uid, self.label, self.plabel)


class MeshESearchObject(Subject):
    def __init__(self, id_=None):
        self.id_ = id_
        h = int(id_[:2])
        if 65 <= h <= 90:
            v = id_.replace(id_[:2], chr(int(id_[:2])))
        else:
            v = id_
        self.uid = 'MeSH:{}'.format(v)  # formatted id_

    def __str__(self):
        return 'uid: {}'.format(self.uid)


class ChebiObject(Subject):
    def __init__(self, id_=None, iri=None, short_form=None, obo_id=None, 
                 label=None, ontology_name=None, ontology_prefix=None, type_=None):
        self.id_ = id_
        self.iri = iri
        self.short_form = short_form
        self.obo_id = obo_id
        self.uid = self.obo_id     # alternative name of self.obo_id for easy access
        self.label = label
        self.ontology_prefix = ontology_prefix
        self.ontology_name = ontology_name
        self.type_ = type_

    def __str__(self):
        return 'obo_id: {}, label: {}, iri: {}'.format(self.obo_id, self.label, self.iri)


class EntrezObject(Subject):
    def __init__(self, id_=None):
        self.id_ = id_
        self.uid = 'Entrez:{}'.format(self.id_)  # formatted id_

    def __str__(self):
        return 'uid: {}'.format(self.uid)
