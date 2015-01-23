import asyncio
from .dispatcher import Dispatcher  # @UnusedImport
from .formatter import JSONFormatter  # @UnusedImport
from .logger import SystemLogger  # @UnusedImport
from .protocol import Protocol  # @UnusedImport
from .responder import Responder  # @UnusedImport


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
    logger: type
        :class:`.Logger` subclass.
    formatter: type
        :class:`.Formatter` subclass.
    dispatcher: type
        :class:`.Dispatcher` subclass.
    responder: type
        :class:`.Responder` subclass.
    protocol: type
        :class:`.Protocol` subclass.

    Example
    -------
    Imagine we have custom details of all types. That's how will be looking
    most general usage case of service. Explore following documentation
    to decide which components you do want to customize and which you don't::

        service = Service(
            path='/api/v1',
            loop=custom_loop,
            logger=CustomLogger,
            formatter=CustomFormatter,
            dispatcher=CustomDispatcher,
            responder=CustomResponder,
            protocol=CustomProtocol)
        service['data'] = 'data'
        service.add_resource(CustomResourse)
        service.add_middleware(CustomMiddleware)
        service.listen('127.0.0.1', 9000)

    .. seealso:: API: :attr:`dict`
    """

    # Public

    def __init__(self, *, path='', loop=None,
                 logger=SystemLogger, formatter=JSONFormatter,
                 dispatcher=Dispatcher, responder=Responder,
                 protocol=Protocol):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.__path = path
        self.__loop = loop
        self.__logger = logger(self)
        self.__formatter = formatter(self)
        self.__dispatcher = dispatcher(self)
        self.__responder = responder(self)
        self.__protocol = protocol(self)

    def __bool__(self):
        return True

    def add_middleware(self, middleware):
        """Add a middleware.

        .. seealso:: Proxy: :meth:`.Responder.add_middleware`
        """
        self.responder.add_middleware(middleware)

    def add_resource(self, resource):
        """Add a resource.

        .. seealso:: Proxy: :meth:`.Dispatcher.add_resource`
        """
        self.dispatcher.add_resource(resource)

    def listen(self, *, hostname, port):
        """Listen forever on TCP/IP socket.

        Parameters
        ----------
        hostname: str
            Hostname like '127.0.0.1'
        port:
            Port like 80.
        """
        server = self.loop.create_server(self.protocol.fork, hostname, port)
        server = self.loop.run_until_complete(server)
        self.logger.info(
            'Start listening at http://{hostname}:{port}'.
            format(hostname=hostname, port=port))
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
    def logger(self):
        """:class:`.Logger` instance (read/write).
        """
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value

    @property
    def formatter(self):
        """:class:`.Formatter` instance (read/write).
        """
        return self.__formatter

    @formatter.setter
    def formatter(self, value):
        self.__formatter = value

    @property
    def dispatcher(self):
        """:class:`.Dispatcher` instance (read/write).
        """
        return self.__dispatcher

    @dispatcher.setter
    def dispatcher(self, value):
        self.__dispatcher = value

    @property
    def responder(self):
        """:class:`.Responder` instance (read/write).
        """
        return self.__responder

    @responder.setter
    def responder(self, value):
        self.__responder = value

    @property
    def protocol(self):
        """:class:`.Protocol` instance (read/write).
        """
        return self.__protocol

    @protocol.setter
    def protocol(self, value):
        self.__protocol = value
