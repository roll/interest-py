import sys
from importlib import import_module


class PluginImporter:

    # Public

    def __init__(self, *, source, target):
        self.__source = source
        self.__target = target

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.source == other.source and
                self.target == other.target)

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    def register(self):
        if self not in sys.meta_path:
            sys.meta_path.append(self)

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
