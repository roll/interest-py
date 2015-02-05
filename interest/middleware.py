import asyncio
import inspect
from .backend import http
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
    MIDDLEWARES = []
    ENDPOINT = None

    def __init__(self, service, *,
                 name=None, path=None, methods=None,
                 middlewares=None, endpoint=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
        if middlewares is None:
            middlewares = self.MIDDLEWARES
        if endpoint is None:
            endpoint = self.ENDPOINT
        if endpoint is None:
            from .endpoint import Endpoint
            endpoint = Endpoint
        relpath = path
        abspath = path
        if self is not service:
            abspath = service.path + path
        super().__init__()
        self.__service = service
        self.__name = name
        self.__relpath = relpath
        self.__abspath = abspath
        self.__methods = methods
        self.__endpoint = endpoint
        self.__add_middlewares(middlewares)
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
            'methods="{self.methods}" '
            'middlewares={middlewares}>')
        compiled = template.format(
            self=self, middlewares=list(self))
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
        return self.__abspath

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
        if self:
            return (yield from self[0](request))
        raise http.NotFound()

    @asyncio.coroutine
    def next(self, request):
        """Call the next middleware (coroutine).
        """
        raise http.NotFound()

    # Internal (Chain's hooks)

    def push(self, item, *, index=None):
        super().push(item, index=index)
        self.__on_chain_change()

    def pull(self, *, index=None):
        super().pull(index=index)
        self.__on_chain_change()

    # Private

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            if not asyncio.iscoroutine(middleware):
                middleware = middleware(self.service)
            self.push(middleware)

    def __add_endpoints(self):
        for name in self.__order__:
            if name.startswith('_'):
                continue
            func = getattr(type(self), name)
            if inspect.isdatadescriptor(func):
                continue
            bindings = getattr(func, STICKER, [])
            for binding in reversed(bindings):
                factory = binding.pop(
                    'endpoint', self.__endpoint)
                path = self.__relpath
                path += binding.pop('path', '')
                respond = getattr(self, name)
                endpoint = factory(self.service,
                    name=name, path=path,
                    respond=respond, **binding)
                self.push(endpoint)

    def __on_chain_change(self):
        next_middleware = None
        for middleware in reversed(self):
            if next_middleware is not None:
                if hasattr(middleware, 'next'):
                    middleware.next = next_middleware
            next_middleware = middleware
