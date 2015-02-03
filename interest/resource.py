import asyncio
from .helpers import OrderedMetaclass, http
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
        self.__init_responders()

    # TODO: optimize on metaclass level to reduce calls stack?
    @asyncio.coroutine
    def __call__(self, request):
        return (yield from self.process(request))

    def __repr__(self):
        template = (
            '<Resource path="{self.path}" '
            'bindings="{self.bindings}">')
        compiled = template.format(self=self)
        return compiled

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

    @asyncio.coroutine
    def process(self, request):
        for responder in self.__responders:
            path = self.service.path + self.path + responder.path
            match1 = self.service.match(request, path=path)
            if not match1:
                continue
            match2 = self.service.match(request, methods=responder.methods)
            if not match2:
                raise http.MethodNotAllowed(request.method, responder.methods)
            return (yield from responder(request, **match1))
        return (yield from self.next(request))

    # Private

    # TODO: reimplement data dict
    # TODO: skip properties
    def __init_responders(self):
        self.__responders = []
        for name in self.__order__:
            if name.startswith('_'):
                continue
            meth = getattr(self, name)
            func = getattr(type(self), name)
            data = getattr(func, http.MARKER, None)
            if data is not None:
                for key, value in data.items():
                    setattr(func, key, value)
                self.__responders.append(meth)
