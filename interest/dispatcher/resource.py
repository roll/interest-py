from ..helpers import OrderedMetaclass
from .binding import Binding


class Resource(metaclass=OrderedMetaclass):
    """Resource representation (abstract).
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__bindings = None

    def __repr__(self):
        template = (
            '<Resource path="{self.path}" '
            'bindings="{self.bindings}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        return self.__service

    @property
    def path(self):
        return '/' + type(self).__name__.lower()

    @property
    def bindings(self):
        if self.__bindings is None:
            self.__bindings = []
            for name in self.__order__:
                if name == 'bindings':
                    continue
                if name.startswith('_'):
                    continue
                attr = getattr(self, name)
                factory = getattr(attr, Binding.MARKER, None)
                if factory is not None:
                    binding = factory(attr)
                    self.__bindings.append(binding)
        return self.__bindings
