import asyncio
import inspect
from .backend import http
from .endpoint import Endpoint
from .helpers import Chain, Config, OrderedMetaclass, STICKER, name


class Middleware(Chain, Config, metaclass=OrderedMetaclass):
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

    .. seealso:: API: :class:`.Config`
    """

    # Public

    NAME = name
    PATH = ''
    METHODS = []
    ENDPOINT = Endpoint

    def __init__(self, service, *,
                 name=None, path=None, methods=None, endpoint=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
        if endpoint is None:
            endpoint = self.ENDPOINT
        if self is not service:
            path = service.path + path
        super().__init__()
        self.__service = service
        self.__name = name
        self.__path = path
        self.__methods = methods
        self.__endpoint = endpoint
        self.__add_endpoints()

    @asyncio.coroutine
    def __call__(self, request):
        match = self.service.router.match(
            request, root=self.path, methods=self.methods)
        if match:
            return (yield from self.process(request))
        return (yield from self.next(request))

    def __repr__(self):
        template = (
            '<Middleware path="{self.path}" '
            'methods="{self.methods}">')
        compiled = template.format(self=self)
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
        """Process a request (coroutine).

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        :class:`.http.StreamResponse`
            Response instance.

        Raises
        ------
        :class:`RuntimeError`
            If middlewares chain doesn't return
            :class:`.http.StreamResponse`.
        """
        for endpoint in self:
            match = endpoint.match(request)
            if match:
                return (yield from endpoint(request, **match))
        raise http.NotFound()

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
            params = getattr(func, STICKER, None)
            if params is not None:
                factory = params.pop('endpoint', self.__endpoint)
                endpoint = factory(self, name=name, **params)
                self.push(endpoint)
