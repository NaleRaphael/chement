from .config import MeshConfiguration

__all__ = ['SparqlFormatError', 'SparqlQuery']


MeshConfig = MeshConfiguration().load()

class SparqlFormatError(Exception):
    pass


class SparqlQuery(object):
    def __init__(self):
        self.content = ''
        self.variables = '*'
        self.from_source = ''
        self.conditions = []

    def add_newline(self, line):
        self.content += '\n' + line

    def __str__(self):
        return str(self.content)

    def build(self):
        """
        Build sparql query.

        Parameters
        ----------
        variables : str
            Desired variables to be presented.
        from_source : str
            Source url to be queried.
        conditions : list of string
            Content of `WHERE` statement.

            e.g.
            Desired conditions:
            ```sparql
            WHERE {
                ?obj meshv:identifier "D006332" .
                ?obj meshv:concept ?c
            }
            ```

            So that `conditions` should be
            ```python
            conditions = [
                `?obj meshv:identifier "D006332" .`,
                '?obj meshv:concept ?c'
            ]
            ```
        """
        base_url = MeshConfig.url

        # --- PREFIX ---
        obj = MeshConfig.sparql.prefix
        for k in sorted(MeshConfig.sparql.prefix.keys()):
            self.add_newline('PREFIX {}: {}'.format(k, MeshConfig.sparql.prefix.get(k)))

        # --- SELECT ---
        self.add_newline('SELECT {}'.format(self.variables))

        # --- FROM ... WHRE ... (condition) ---
        self.add_newline('FROM <{}>'.format(self.from_source))
        self.add_newline('WHERE {')
        for line in self.conditions:
            # check that each line should be endded with a '.'
            if line[-1] != '.':
                raise SparqlFormatError('Line should be endded with a \'.\'')
            self.add_newline(line)
        self.add_newline('}')
        return self


class QueryTerm2UI(SparqlQuery):
    def __init__(self, term=''):
        super(QueryTerm2UI, self).__init__()
        self.variables = '?ui ?label ?plabel'
        self.from_source = r'http://id.nlm.nih.gov/mesh'
        self.conditions = [
            '?d a meshv:Descriptor .',
            '?d meshv:identifier ?ui .',
            '?d rdfs:label ?label .',
            '?d meshv:concept ?c .',
            '?c meshv:term ?ct .',
            '?ct meshv:prefLabel ?plabel .'
            'FILTER(REGEX(?plabel,"{}","i")) .'.format(term),
        ]
