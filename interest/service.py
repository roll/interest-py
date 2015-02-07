import sys
import asyncio
from .logger import Logger
from .handler import Handler
from .helpers import loop
from .router import Router
from .middleware import Middleware


class Service(Middleware):
    """Service is a middleware capable to listen on TCP/IP socket.

    Service also provides methods :meth:`.Service.match`, :meth:`.Service.url`
    and :meth:`.Service.log` to use in  request processing. This list can be
    updated via :class:`.Provider` system. Concrete service functionality
    is based on :class:`.Router`, :class:`.Logger`
    and :class:`.Handler` classes.

    .. seealso:: Implements:
        :class:`.Middleware`,
        :class:`.Chain`,
        :class:`.Config`

    Parameters
    ----------
    loop: object
        Custom asyncio's loop.
    router: type
        :class:`.Router` subclass.
    logger: type
        :class:`.Logger` subclass.
    handler: type
        :class:`.Handler` subclass.
    providers: list
        List of :class:`.Provider` subclasses.

    Examples
    --------
    Minimal service can be initiated without subclassing and parameters
    passed. But for example we will add some custom components::

        # Create server
        service = Service(
            router='<router>',
            logger='<logger>',
            handler='<handler>',
            providers=['<provider>'],
            middlewares=['<middleware>'])

        # Listen forever
        service.listen(host='127.0.0.1', port=9000, forever=True)
    """

    # Public

    LOOP = loop
    """Default loop parameter.
    """
    ROUTER = Router
    """Default router parameter.
    """
    LOGGER = Logger
    """Default logger parameter.
    """
    HANDLER = Handler
    """Default handler parameter.
    """
    PROVIDERS = []
    """Default providers parameter.
    """

    def __init__(self, service=None, *,
                name=None, prefix=None, methods=None,
                middlewares=None, endpoint=None,
                loop=None, router=None, logger=None, handler=None,
                providers=None):
        if loop is None:
            loop = self.LOOP
        if router is None:
            router = self.ROUTER
        if logger is None:
            logger = self.LOGGER
        if handler is None:
            handler = self.HANDLER
        if providers is None:
            providers = self.PROVIDERS.copy()
        service = self
        super().__init__(service,
            name=name, prefix=prefix, methods=methods,
            middlewares=middlewares, endpoint=endpoint)
        self.__loop = loop
        self.__router = router(self)
        self.__logger = logger(self)
        self.__handler = handler(self)
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

    def listen(self, *, host, port, override=False, forever=False, **kwargs):
        """Listen on TCP/IP socket.

        Parameters
        ----------
        host: str
            Host like '127.0.0.1'
        port:
            Port like 80.
        """
        if override:
            argv = dict(enumerate(sys.argv))
            host = argv.get(1, host)
            port = int(argv.get(2, port))
        server = self.loop.create_server(
            self.__handler.fork, host, port, **kwargs)
        server = self.loop.run_until_complete(server)
        self.log('info',
            'Start listening host="{host}" port="{port}"'.
            format(host=host, port=port))
        if forever:
            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                pass
        return server

    def match(self, request, *, root=None, path=None, methods=None):
        """Return match or None for the request/constraints pair.

        .. seealso:: Proxy:
            :meth:`.Router.match`
        """
        return self.__router.match(
            request, root=root, path=path, methods=methods)

    def url(self, name, *, base=None, query=None, **match):
        """Construct an url for the given parameters.

        .. seealso:: Proxy:
            :meth:`.Router.url`
        """
        return self.__router.url(name, base=base, query=query, **match)

    def log(self, level, *args, **kwargs):
        """Log something.

        .. seealso:: Proxy:
            :class:`.Logger`.level
        """
        target = getattr(self.__logger, level)
        target(*args, **kwargs)

    # Private

    def __apply_providers(self, providers):
        for provider in providers:
            if not asyncio.iscoroutine(provider):
                provider = provider(self)
            self.loop.run_until_complete(
                provider(self))
