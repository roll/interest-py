import asyncio
from .helpers import Chain, http
from .dispatcher import Dispatcher  # @UnusedImport
from .logger import SystemLogger  # @UnusedImport
from .handler import Handler  # @UnusedImport


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
    middlewares: list
        :class:`.Middleware` subclasses list.
    resources: list
        :class:`.Resource` subclasses list.
    converters: list
        :class:`.Converter` subclasses list.
    dispatcher: type
        :class:`.Dispatcher` subclass.
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
            middlewares=[CustomMiddleware],
            resources=[CustomResourse],
            converters=[CustomConverter],
            dispatcher=CustomDispatcher,
            handler=CustomHandler,
            logger=CustomLogger)
        service['data'] = 'data'
        service.listen('127.0.0.1', 9000)

    .. seealso:: API: :attr:`dict`
    """

    # Public

    def __init__(self, *, path='', loop=None,
                 middlewares=None, resources=None, converters=None,
                 dispatcher=Dispatcher,
                 handler=Handler, logger=SystemLogger):
        if loop is None:
            loop = asyncio.get_event_loop()
        if middlewares is None:
            middlewares = []
        if resources is None:
            resources = []
        if converters is None:
            converters = []
        self.__path = path
        self.__loop = loop
        self.__dispatcher = dispatcher(self)
        self.__handler = handler(self)
        self.__logger = logger(self)
        self.__middlewares = Chain(
            self.__on_middlewares_change)
        # Add the given components
        self.__add_middlewares(middlewares)
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
    def dispatcher(self):
        """:class:`.Dispatcher` instance (read/write).
        """
        return self.__dispatcher

    @dispatcher.setter
    def dispatcher(self, value):
        self.__dispatcher = value

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
        return (yield from self.dispatcher.route(request))

    @asyncio.coroutine
    def match(self, request, *, root=None, path=None, methods=None):
        return self.dispatcher.match(
            request, root=root, path=path, methods=methods)

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

    # Private

    def __add_resources(self, resources):
        for resource in resources:
            resource = resource(self)
            self.dispatcher.resources.add(resource)

    def __add_converters(self, converters):
        for converter in converters:
            converter = converter(self)
            self.dispatcher.converters.add(converter)

    def __on_middlewares_change(self):
        next_middleware = None
        for middleware in reversed(self.middlewares):
            if next_middleware is not None:
                middleware.next = next_middleware.process
            next_middleware = middleware

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            middleware = middleware(self)
            self.middlewares.add(middleware)
