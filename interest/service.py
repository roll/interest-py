import asyncio
from .converter import Converter
from .logger import SystemLogger
from .handler import SystemHandler
from .helpers import Chain, ExistentMatch, NonExistentMatch
from .pattern import Pattern
from .middleware import Middleware
from .protocol import http


class Service(Chain, Middleware):
    """Service representation.

    Service provides a high-level abstraction for end-user and incapsulates
    all internal components. Service is a dict. You can use service instance
    to store application data. Service is fully customizable by passing
    subclasses of main interest's classes to the constructor.
    See full list of parameters below.

    Parameters
    ----------
    path: str
        Path prefix for HTTP path routing.
    loop: object
        Custom asyncio's loop.
    handler: type
        :class:`.Handler` subclass.
    logger: type
        :class:`.Logger` subclass.

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

    .. seealso:: API: :attr:`dict`
    """

    # Public

    LOOP = asyncio.get_event_loop()
    LOGGER = SystemLogger
    HANDLER = SystemHandler
    MIDDLEWARES = []
    CONVERTERS = {}
    PROVIDERS = {}

    def __init__(self, service=None, *,
                name=None, path=None, methods=None,
                loop=None, logger=None, handler=None,
                middlewares=None, converters=None, providers=None):
        if service is None:
            service = self
        if loop is None:
            loop = self.LOOP
        if logger is None:
            logger = self.LOGGER
        if handler is None:
            handler = self.HANDLER
        if middlewares is None:
            middlewares = self.MIDDLEWARES
        if converters is None:
            converters = self.CONVERTERS
        if providers is None:
            providers = self.PROVIDERS
        super().__init__(service, name=name, path=path, methods=methods)
        self.__loop = loop
        self.__logger = logger(self)
        self.__handler = handler(self)
        self.__add_middlewares(middlewares)
        self.__add_converters(converters)
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
        """Respond a response to a request (coroutine).

        Request will be processed by middlewares chain in straight order.

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

    def match(self, request, *, root=None, path=None, methods=None):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        root: str
            HTTP path root relative to the service.
        path: str
            HTTP path relative to the service.
        methods: list
            HTTP methods.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        if path is not None:
            path = self.__fullpath + path
            match = self.__match_path(request, path)
        elif root is not None:
            root = self.__fullpath + root
            match = self.__match_root(request, root)
        else:
            root = self.__fullpath
            match = self.__match_root(request, root)
        if not match:
            return NonExistentMatch()
        if methods is not None:
            lmatch = self.__match_methods(request, methods)
            if not lmatch:
                return NonExistentMatch()
        return match

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    # Private

    __CONVERTERS = {
       'str': Converter.config(
            pattern=r'[^<>/]+', convert=str),
       'int': Converter.config(
            pattern=r'[1-9]+', convert=int),
       'float': Converter.config(
            pattern=r'[1-9.]+', convert=float),
       'path': Converter.config(
            pattern=r'[^<>]+', convert=str)}

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            name = None
            if not asyncio.iscoroutine(middleware):
                middleware = middleware(self)
                name = middleware.name
            self._append(middleware, name=name)
        self.__on_change()

    def __add_converters(self, converters):
        self.__converters = {}
        econverters = self.__CONVERTERS.copy()
        econverters.update(converters)
        for key, cls in econverters.items():
            self.__converters[key] = cls(self)

    def __add_providers(self, providers):
        self.__providers = {}
        for key, cls in providers.items():
            provider = cls(self)
            value = self.loop.run_until_complete(
                provider.provide())
            setattr(self, key, value)
            self.__providers[key] = provider

    def __match_root(self, request, root):
        pattern = self.__get_pattern(root)
        match = pattern.match(request.path, left=True)
        return match

    def __match_path(self, request, path):
        pattern = self.__get_pattern(path)
        match = pattern.match(request.path)
        return match

    def __match_methods(self, request, methods):
        match = ExistentMatch()
        if methods:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return NonExistentMatch()
        return match

    def __get_pattern(self, path):
        if path not in self.__patterns:
            self.__patterns[path] = Pattern.create(
                path, self.__converters)
        return self.__patterns[path]

    def __on_change(self):
        next_middleware = None
        for middleware in reversed(self):
            if next_middleware is not None:
                middleware.next = next_middleware
            next_middleware = middleware

    @property
    def __fullpath(self):
        fullpath = self.service.path
        if self is not self.service:
            fullpath += self.path
        return fullpath
