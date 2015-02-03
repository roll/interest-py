import asyncio
from .dispatcher import Dispatcher  # @UnusedImport
from .logger import SystemLogger  # @UnusedImport
from .handler import Handler  # @UnusedImport
from .processor import Processor  # @UnusedImport


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
    processor: type
        :class:`.Processor` subclass.
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
            processor=CustomProcessor,
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
                 processor=Processor, dispatcher=Dispatcher,
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
        self.__processor = processor(self)
        self.__dispatcher = dispatcher(self)
        self.__handler = handler(self)
        self.__logger = logger(self)
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
    def processor(self):
        """:class:`.Processor` instance (read/write).
        """
        return self.__processor

    @processor.setter
    def processor(self, value):
        self.__processor = value

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

    # Private

    def __add_middlewares(self, middlewares):
        for middleware in middlewares:
            middleware = middleware(self)
            self.processor.middlewares.add(middleware)

    def __add_resources(self, resources):
        for resource in resources:
            resource = resource(self)
            self.dispatcher.resources.add(resource)

    def __add_converters(self, converters):
        for converter in converters:
            converter = converter(self)
            self.dispatcher.converters.add(converter)
