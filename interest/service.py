import asyncio
from .logger import SystemLogger
from .handler import SystemHandler
from .helpers import Chain, ExistentMatch, NonExistentMatch, http
from .pattern import Pattern
from .middleware import Middleware
from .converter import (FloatConverter, IntegerConverter,
                        PathConverter, StringConverter)


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

    PATH = ''
    LOOP = asyncio.get_event_loop()
    LOGGER = SystemLogger
    HANDLER = SystemHandler
    MIDDLEWARES = []
    PROVIDERS = {}
    CONVERTERS = {
       'str': StringConverter,
       'int': IntegerConverter,
       'float': FloatConverter,
       'path': PathConverter}

    def __init__(self, service=None, *,
                path=None, loop=None, logger=None, handler=None,
                middlewares=None, providers=None, converters=None):
        if service is None:
            service = self
        if path is None:
            path = self.PATH
        if loop is None:
            loop = self.LOOP
        if logger is None:
            logger = self.LOGGER
        if handler is None:
            handler = self.HANDLER
        if middlewares is None:
            middlewares = self.MIDDLEWARES
        if providers is None:
            providers = self.PROVIDERS
        if converters is None:
            converters = self.CONVERTERS
        super().__init__(service)
        self.__path = path
        self.__loop = loop
        self.__logger = logger(self)
        self.__handler = handler(self)
        self.__add_middlewares(middlewares)
        self.__add_providers(providers)
        self.__add_converters(converters)
        self.__patterns = {}

    def __getattr__(self, name):
        if name in self.__providers:
            value = self.__providers[name]
            setattr(self, name, value)
            return value
        raise AttributeError(name)

    def __repr__(self):
        template = (
            '<Service path="{self.path}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def path(self):
        """HTTP path (read-only).
        """
        return self.__path

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

    def add(self, *middlewares, **kwargs):
        for middleware in middlewares:
            name = None
            if not asyncio.iscoroutine(middleware):
                middleware = middleware(self, **kwargs)
                name = middleware.name
            super().add(middleware, name=name)
        self.__on_change()

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
        if not self:
            raise RuntimeError('No middlawares added')
        try:
            response = yield from self[0](request)
        except http.Exception as exception:
            return exception
        if not isinstance(response, http.StreamResponse):
            raise RuntimeError('Last reply is not a StreamResponse')
        return response

    def match(self, request, *, root=None, path=None, methods=None):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        root: str
            HTTP path root relative to the service.path.
        path: str
            HTTP path relative to the service.path.
        methods: list
            HTTP methods.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        match = ExistentMatch()
        if root is not None:
            root = self.path + root
            lmatch = self.__match_root(request, root)
            if not lmatch:
                return NonExistentMatch()
        if path is not None:
            path = self.path + path
            lmatch = self.__match_path(request, path)
            if not lmatch:
                return NonExistentMatch()
            match = lmatch
        if methods is not None:
            lmatch = self.__match_methods(request, methods)
            if not lmatch:
                return NonExistentMatch()
        return match

    # TODO: implement
    # TODO: rename to build?
    def url(self, *args, **kwargs):
        raise NotImplementedError()

    # Private

    def __add_middlewares(self, middlewares):
        for middleware in self.MIDDLEWARES + middlewares:
            self.add(middleware)

    def __add_providers(self, providers):
        self.__providers = {}
        classes = self.PROVIDERS.copy()
        classes.update(providers)
        for key, cls in classes.items():
            self.__providers[key] = cls(self)

    def __add_converters(self, converters):
        self.__converters = {}
        classes = self.CONVERTERS.copy()
        classes.update(converters)
        for key, cls in classes.items():
            self.__converters[key] = cls(self)

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
        if methods is not None:
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
