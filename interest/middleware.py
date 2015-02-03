import asyncio
import inspect
from .endpoint import Endpoint
from .helpers import Configurable, Chain, OrderedMetaclass, http


class Middleware(Chain, Configurable, metaclass=OrderedMetaclass):
    """Middleware representation (abstract).

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Example
    -------
    By default interest doesn't know what to do with any request.
    We have to implement a minimal midleware::

        class MinimalMiddleware(Middleware):

            # Public

            @asyncio.coroutine
            def __call__(self, request):
                return Response(text='Hello World!')

        service = Service(path='/api/v1')
        service.add_middleware(MinimalMiddleware)
    """

    # Public

    NAME = property(lambda self: type(self).__name__.lower())
    PATH = ''
    METHODS = None

    def __init__(self, service, *, name=None, path=None, methods=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
        super().__init__()
        self.__service = service
        self.__name = name
        self.__path = path
        self.__methods = methods
        self.__add_endpoints()

    # TODO: implement filter
    @asyncio.coroutine
    def __call__(self, request):
        return (yield from self.process(request))

    # TODO: improve
    def __repr__(self):
        template = (
            '<Middleware path="{self.path}" '
            'endpoints={endpoints}>')
        compiled = template.format(
            self=self, endpoints=list(self))
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        """Middleware's name (read-only).
        """
        return self.__name

    @property
    def path(self):
        """Middleware's path (read-only).
        """
        return self.__path

    @property
    def methods(self):
        """Middleware's methods (read-only).
        """
        return self.__methods

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

    @asyncio.coroutine
    def next(self, request):
        """Call the next middleware (coroutine).
        """
        raise http.NotFound()

    # Private

    def __add_endpoints(self):
        for name in self.__order__:
            if name.startswith('_'):
                continue
            func = getattr(type(self), name)
            if inspect.isdatadescriptor(func):
                continue
            constraints = getattr(func, http.MARKER, None)
            if constraints is not None:
                endpoint = Endpoint(self, name=name, **constraints)
                self._add(endpoint, name=endpoint.name)
