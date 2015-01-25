from ..helpers import OrderedMetaclass, http
from .binding import Binding


class Resource(metaclass=OrderedMetaclass):
    """Resource representation (abstract).

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
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
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        """Resource's name.
        """
        return type(self).__name__.lower()

    @property
    def path(self):
        """Resource's path.
        """
        return '/' + self.name

    @property
    def bindings(self):
        """Resource's list of :class:`.Binding`.
        """
        if self.__bindings is None:
            self.__bindings = []
            for name in self.__order__:
                if name == 'bindings':
                    continue
                if name.startswith('_'):
                    continue
                attr = getattr(self, name)
                data = getattr(attr, http.MARKER, None)
                if data is not None:
                    binding = Binding(attr, **data)
                    self.__bindings.append(binding)
        return self.__bindings
