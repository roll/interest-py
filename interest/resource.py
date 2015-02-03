import asyncio
import inspect
from .helpers import Chain, OrderedMetaclass, http
from .endpoint import Endpoint
from .middleware import Middleware


class Resource(Chain, Middleware, metaclass=OrderedMetaclass):
    """Resource representation (abstract).

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        super().__init__(service)
        self.__add_endpoints()

    def __repr__(self):
        template = (
            '<Resource path="{self.path}" '
            'endpoints="{endpoints}">')
        compiled = template.format(
            self=self, endpoints=self.__endpoints)
        return compiled

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

    def add(self, *endpoints, **kwargs):
        for endpoint in endpoints:
            if not isinstance(endpoint, Endpoint):
                endpoint = endpoint(self, **kwargs)
            super().add(endpoint, name=endpoint.name)

    @asyncio.coroutine
    def process(self, request):
        for endpoint in self:
            path = self.path + (endpoint.path or '')
            match = self.service.match(request, path=path)
            if not match:
                continue
            check = self.service.match(request, methods=endpoint.methods)
            if not check:
                raise http.MethodNotAllowed(request.method, endpoint.methods)
            return (yield from endpoint(request, **match))
        return (yield from self.next(request))

    # Private

    def __add_endpoints(self):
        self.__endpoints = {}
        for name in self.__order__:
            if name.startswith('_'):
                continue
            func = getattr(type(self), name)
            if inspect.isdatadescriptor(func):
                continue
            data = getattr(func, http.MARKER, None)
            if data is not None:
                self.add(Endpoint, name=name, **data)
