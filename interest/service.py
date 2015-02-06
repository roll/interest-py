import asyncio
from .logger import Logger
from .handler import Handler
from .helpers import loop
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
            prefix='/api/v1',
            loop=custom_loop,
            handler=CustomHandler,
            logger=CustomLogger)
        service['data'] = 'data'
        service.listen('127.0.0.1', 9000)

    .. seealso:: API: :class:`.Middleware`
    """

    # Public

    LOOP = loop
    LOGGER = Logger
    HANDLER = Handler
    ROUTER = Router
    PROVIDERS = []

    def __init__(self, service=None, *,
                name=None, prefix=None, methods=None,
                middlewares=None, endpoint=None,
                loop=None, logger=None, handler=None, router=None,
                providers=None):
        if loop is None:
            loop = self.LOOP
        if logger is None:
            logger = self.LOGGER
        if handler is None:
            handler = self.HANDLER
        if router is None:
            router = self.ROUTER
        if providers is None:
            providers = self.PROVIDERS
        service = self
        super().__init__(service,
            name=name, prefix=prefix, methods=methods,
            middlewares=middlewares, endpoint=endpoint)
        self.__loop = loop
        self.__logger = logger(self)
        self.__handler = handler(self)
        self.__router = router(self)
        self.__apply_providers(providers)

    def __repr__(self):
        template = (
            '<Service name="{self.name}" '
            'path="{self.path}" methods="{self.methods}" '
            'middlewares={middlewares}>')
        compiled = template.format(
            self=self, middlewares=list(self))
        return compiled

    @property
    def loop(self):
        """asyncio's loop (read-only).
        """
        return self.__loop

    def listen(self, *, host, port, async=False, **kwargs):
        """Listen forever on TCP/IP socket.

        Parameters
        ----------
        host: str
            Host like '127.0.0.1'
        port:
            Port like 80.
        """
        server = self.loop.create_server(
            self.__handler.fork, host, port, **kwargs)
        server = self.loop.run_until_complete(server)
        if async:
            return server
        self.log('info',
            'Start listening host="{host}" port="{port}"'.
            format(host=host, port=port))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def match(self, request, *, root=None, path=None, methods=None):
        return self.__router.match(
            request, root=root, path=path, methods=methods)

    def url(self, pointer, *, query=None, **match):
        return self.__router.url(pointer, query=query, **match)

    def log(self, level, *args, **kwargs):
        target = getattr(self.__logger, level)
        target(*args, **kwargs)

    # Private

    def __apply_providers(self, providers):
        for provider in providers:
            if not asyncio.iscoroutine(provider):
                provider = provider(self)
            self.loop.run_until_complete(
                provider(self))
