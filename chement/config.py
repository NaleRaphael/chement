import json
import os.path as osp

__all__ = ['Configuration', 'MeshConfiguration', 'ChebiConfiguration', 'EntrezConfiguration']


class DummyObject(dict):
    def __init__(self, *args, **kwargs):
        super(DummyObject, self).__init__()

    def __repr__(self):
        return str(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __getitem__(self, key):
        return self.__dict__[key]


class DictObjectConverter(object):
    @classmethod
    def convert(cls, obj, d):
        for k in d:
            cls._kv2attr(obj, d, k)

    @classmethod
    def _kv2attr(cls, obj, d, k):
        if not isinstance(d[k], dict):
            setattr(obj, k, d[k])
        else:
            setattr(obj, k, DummyObject())
            attr = getattr(obj, k)
            for k_ in d[k]:
                cls._kv2attr(attr, d[k], k_)


class Configuration(DummyObject):
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = DummyObject.__new__(cls, *args, **kwargs)
        return cls._instance

    def load(self, fn=None):
        if fn is None:
            raise ValueError('`fn` is not defined.')

        with open(fn, 'r') as f:
            conf = json.load(f)
            DictObjectConverter.convert(self, conf)
        return self


class MeshConfiguration(Configuration):
    _instance = None
    DEFAULT_CONFIG_PATH = osp.join(osp.dirname(__file__), 'mesh.config')

    def load(self, fn=DEFAULT_CONFIG_PATH):
        DEFAULT_API_KEY_PATH = osp.join(osp.dirname(__file__), 'mesh.api.key')
        api_key = None
        if osp.isfile(DEFAULT_API_KEY_PATH):
            with open(DEFAULT_API_KEY_PATH, 'r') as f:
                api_key = f.read()
        config = super(MeshConfiguration, self).load(fn=fn)
        config.api_key = api_key
        return config


class ChebiConfiguration(Configuration):
    _instance = None
    DEFAULT_CONFIG_PATH = osp.join(osp.dirname(__file__), 'chebi.config')

    def load(self, fn=DEFAULT_CONFIG_PATH):
        return super(ChebiConfiguration, self).load(fn=fn)


class EntrezConfiguration(Configuration):
    _instance = None
    DEFAULT_CONFIG_PATH = osp.join(osp.dirname(__file__), 'entrez.config')
    DEFAULT_API_KEY_PATH = osp.join(osp.dirname(__file__), 'entrez.api.key')

    def load(self, fn=DEFAULT_CONFIG_PATH):
        api_key = None
        if osp.isfile(self.DEFAULT_API_KEY_PATH):
            with open(self.DEFAULT_API_KEY_PATH, 'r') as f:
                api_key = f.read()
        config = super(EntrezConfiguration, self).load(fn=fn)
        config.api_key = api_key
        return config


if __name__ == '__main__':
    meshconfig = MeshConfiguration().load()
    print(meshconfig)

    chebiconfig = ChebiConfiguration().load()
    print(chebiconfig)

    entrezconfig = EntrezConfiguration().load()
    print(entrezconfig)

    import pdb; pdb.set_trace()
