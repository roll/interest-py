import sys
from importlib import import_module


class PluginImporter:

    # Public

    source = 'interest.plugins.'
    target = 'interest_'

    @classmethod
    def register(cls):
        for item in sys.meta_path:
            if isinstance(item, cls):
                return
        importer = cls()
        sys.meta_path.append(importer)

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.source):
            return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        if not fullname.startswith(self.source):
            raise ImportError(fullname)
        realname = fullname.replace(self.source, self.target)
        module = import_module(realname)
        sys.modules[realname] = module
        sys.modules[fullname] = module
        return module
