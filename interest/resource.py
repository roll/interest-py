import asyncio
import inspect
from .helpers import OrderedMetaclass, http
from .binding import Binding
from .endpoint import Endpoint


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
        self.__add_endpoints()

    # TODO: optimize on metaclass level to reduce calls stack?
    @asyncio.coroutine
    def __call__(self, request):
        return (yield from self.process(request))

    def __getitem__(self, param):
        if isinstance(param, int):
            return list(iter(self.__endpoints))[param]
        return self.__endpoints[param]

    def __iter__(self):
        return self.__endpoints.values()

    def __bool__(self):
        return bool(self.__endpoints)

    def __len__(self):
        return len(self.__endpoints)

    def __repr__(self):
        template = (
            '<Resource path="{self.path}" '
            'endpoints="{endpoints}">')
        compiled = template.format(
            self=self, endpoints=self.__endpoints)
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
        for endpoint in self:
            path = self.service.path + self.path + endpoint.path
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
            meth = getattr(self, name)
            data = getattr(func, http.MARKER, None)
            if data is not None:
                endpoint = Endpoint(meth, **data)
                self.__endpoints[name] = endpoint
