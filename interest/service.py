import asyncio
from .backend import http
from .logger import Logger
from .handler import Handler
from .router import Router
from .middleware import Middleware


class Service(Middleware):
    """Service representation.

    Service provides a high-level abstraction for end-user and incapsulates
    all internal components. Service is a dict. You can use service instance
    to store application data. Service is fully customizable by passing
    subclasses of main interest's classes to the constructor.
    See full list of parameters below.

    Parameters
    ----------
    loop: object
        Custom asyncio's loop.
    logger: type
        :class:`.Logger` subclass.
    handler: type
        :class:`.Handler` subclass.
    router: type
        :class:`.Router` subclass.

    Example
    -------
    Imagine we have custom details of all types. That's how will be looking
    most general usage case of service. Explore following documentation
    to decide which components you do want to customize and which you don't::

        service = Service(
            path='/api/v1',
            loop=custom_loop,
            handler=CustomHandler,
            logger=CustomLogger)
        service['data'] = 'data'
        service.listen('127.0.0.1', 9000)

    .. seealso:: API: :class:`.Chain`
    .. seealso:: API: :class:`.Middleware`
    """

    # Public

    LOOP = asyncio.get_event_loop()
    LOGGER = Logger
    HANDLER = Handler
    ROUTER = Router
    MIDDLEWARES = []
    PROVIDERS = {}

    def __init__(self, service=None, *,
                name=None, path=None, methods=None, endpoint=None,
                loop=None, logger=None, handler=None, router=None,
                middlewares=None, providers=None):
        if service is None:
            service = self
        if loop is None:
            loop = self.LOOP
        if logger is None:
            logger = self.LOGGER
        if handler is None:
            handler = self.HANDLER
        if router is None:
            router = self.ROUTER
        if middlewares is None:
            middlewares = self.MIDDLEWARES
        if providers is None:
            providers = self.PROVIDERS
        super().__init__(service,
            name=name, path=path, methods=methods, endpoint=endpoint)
        self.__loop = loop
        self.__logger = logger(self)
        self.__handler = handler(self)
        self.__router = router(self)
        self.__add_middlewares(middlewares)
        self.__add_providers(providers)
        self.__patterns = {}

    def __repr__(self):
        template = (
            '<Service path="{self.path}" '
            'methods="{self.methods}" '
            'middlewares={middlewares}>')
        compiled = template.format(
            self=self, middlewares=list(self))
        return compiled

    @property
    def loop(self):
        """asyncio's loop (read-only).
        """
        return self.__loop

    @property
    def logger(self):
        """:class:`.Logger` instance (read-only).
        """
        return self.__logger

    @property
    def handler(self):
        """:class:`.Handler` instance (read-only).
        """
        return self.__handler

    @property
    def router(self):
        """:class:`.Router` instance (read-only).
        """
        return self.__router

    def listen(self, *, host, port):
        """Listen forever on TCP/IP socket.

        Parameters
        ----------
        host: str
            Host like '127.0.0.1'
        port:
            Port like 80.
        """
        server = self.loop.create_server(self.handler.fork, host, port)
        server = self.loop.run_until_complete(server)
        self.logger.info(
            'Start listening at http://{host}:{port}'.
            format(host=host, port=port))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    @asyncio.coroutine
    def process(self, request):
        if self:
            return (yield from self[0](request))
        raise http.NotFound()

    # Private

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            if not asyncio.iscoroutine(middleware):
                middleware = middleware(self)
            self.push(middleware)
        self.__on_change()

    def __add_providers(self, providers):
        self.__providers = {}
        for key, cls in providers.items():
            provider = cls(self)
            value = self.loop.run_until_complete(
                provider.provide())
            setattr(self, key, value)
            self.__providers[key] = provider

    def __on_change(self):
        next_middleware = None
        for middleware in reversed(self):
            if next_middleware is not None:
                middleware.next = next_middleware
            next_middleware = middleware
