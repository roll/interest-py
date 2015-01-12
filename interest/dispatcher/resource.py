from abc import ABCMeta
from .binding import Binding


class Resource(metaclass=ABCMeta):

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        return self.__service

    @property
    def path(self):
        return '/' + type(self).__name__.lower()

    @property
    def bindings(self):
        bindings = []
        for name in dir(self):
            if name == 'bindings':
                continue
            if name.startswith('_'):
                continue
            attr = getattr(self, name)
            binding = getattr(attr, Binding.MARKER, None)
            if binding is not None:
                bindings.append(binding)
        return bindings
