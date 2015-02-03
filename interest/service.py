import asyncio
from .logger import SystemLogger  # @UnusedImport
from .handler import Handler  # @UnusedImport
from .helpers import Chain, ExistentMatch, NonExistentMatch, http
from .pattern import Pattern
from .route import ExistentRoute, NonExistentRoute
from .converter import (FloatConverter, IntegerConverter,
                        PathConverter, StringConverter)


class Service(dict):
    """Service representation.

    Service provides high-level abstraction for end-user and incapsulates
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
    resources: list
        :class:`.Resource` subclasses list.
    converters: list
        :class:`.Converter` subclasses list.
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
            resources=[CustomResourse],
            converters=[CustomConverter],
            handler=CustomHandler,
            logger=CustomLogger)
        service['data'] = 'data'
        service.listen('127.0.0.1', 9000)

    .. seealso:: API: :attr:`dict`
    """

    # Public

    def __init__(self, *, path='', loop=None,
                 resources=None, converters=None,
                 handler=Handler, logger=SystemLogger):
        if loop is None:
            loop = asyncio.get_event_loop()
        if resources is None:
            resources = []
        if converters is None:
            converters = []
        self.__path = path
        self.__loop = loop
        self.__handler = handler(self)
        self.__logger = logger(self)
        self.__patterns = {}
        self.__resources = Chain()
        self.__converters = Chain()
        self.__middlewares = Chain(
            self.__on_middlewares_change)
        # Add default converters
        self.__add_default_converters()
        # Add the given components
        self.__add_resources(resources)
        self.__add_converters(converters)

    def __bool__(self):
        return True

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

    @property
    def path(self):
        """Path prefix for HTTP path routing (read-only).
        """
        return self.__path

    @property
    def loop(self):
        """asyncio's loop (read-only).
        """
        return self.__loop

    @property
    def handler(self):
        """:class:`.Handler` instance (read/write).
        """
        return self.__handler

    @handler.setter
    def handler(self, value):
        self.__handler = value

    @property
    def logger(self):
        """:class:`.Logger` instance (read/write).
        """
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value

    @asyncio.coroutine
    def route(self, request):
        """Route a request.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        :class:`.Route`
            Route instance.
        """
        route = NonExistentRoute(http.NotFound())
        # Check the service
        root = self.path
        match = self.__match_root(request, root)
        if not match:
            return route
        # Check the resources
        match = False
        for resource in self.resources:
            root = self.path + resource.path
            match = self.__match_root(request, root)
            if match:
                break
        if not match:
            return route
        # Check the bingings
        for binding in resource.bindings:
            path = self.path + resource.path + binding.path
            match1 = self.__match_path(request, path)
            if not match1:
                continue
            match2 = self.__match_methods(request, binding.methods)
            if not match2:
                return NonExistentRoute(
                    http.MethodNotAllowed(request.method, binding.methods))
            return ExistentRoute(binding.responder, match1)
        return route

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
    def url(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    def middlewares(self):
        """:class:`.Chain` of middlewares.

        Order corresponds with order of adding and affects order of
        middlewares applying. Client may add middleware instance
        manually to that list.
        """
        return self.__middlewares

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
        if not self.middlewares:
            raise RuntimeError('No middlawares added')
        try:
            response = yield from self.middlewares[0].process(request)
        except http.Exception as exception:
            return exception
        if not isinstance(response, http.StreamResponse):
            raise RuntimeError('Last reply is not a StreamResponse')
        return response

    @property
    def resources(self):
        """:class:`.Chain` of resources.
        """
        return self.__resources

    @property
    def converters(self):
        """:class:`.Chain` of converters.
        """
        return self.__converters

    # Private

    def __add_default_converters(self):
        self.converters.add(StringConverter(self))
        self.converters.add(IntegerConverter(self))
        self.converters.add(FloatConverter(self))
        self.converters.add(PathConverter(self))

    def __add_resources(self, resources):
        for resource in resources:
            resource = resource(self)
            self.resources.add(resource)

    def __add_converters(self, converters):
        for converter in converters:
            converter = converter(self)
            self.converters.add(converter)

    def __on_middlewares_change(self):
        next_middleware = None
        for middleware in reversed(self.middlewares):
            if next_middleware is not None:
                middleware.next = next_middleware.process
            next_middleware = middleware

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
            self.__patterns[path] = Pattern.create(path, self.converters)
        return self.__patterns[path]
