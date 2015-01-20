import asyncio
from .dispatcher import Dispatcher  # @UnusedImport
from .formatter import JSONFormatter  # @UnusedImport
from .handler import Handler  # @UnusedImport
from .logger import SystemLogger  # @UnusedImport
from .processor import Processor  # @UnusedImport


class Service(dict):
    """Service representation.

    Service is fully customizable by passing subclasses of
    main interest's elements like Logger or Formatter. See
    full list of parameters.

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
    processor: type
        :class:`.Processor` subclass.
    handler: type
        :class:`.Handler` subclass.
    """

    # Public

    def __init__(self, *, path='', loop=None,
                 logger=SystemLogger, formatter=JSONFormatter,
                 dispatcher=Dispatcher, processor=Processor, handler=Handler):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.__path = path
        self.__loop = loop
        self.__logger = logger(self)
        self.__formatter = formatter(self)
        self.__dispatcher = dispatcher(self)
        self.__processor = processor(self)
        self.__handler = handler(self)

    def __bool__(self):
        return True

    def add_middleware(self, *middlewares, source=None):
        self.processor.add_middleware(*middlewares, source=source)

    def add_resource(self, *resources, source=None):
        self.dispatcher.add_resource(*resources, source=source)

    def listen(self, *, hostname, port):
        server = self.loop.create_server(self.handler.fork, hostname, port)
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
    def processor(self):
        """:class:`.Processor` instance (read/write).
        """
        return self.__processor

    @processor.setter
    def processor(self, value):
        self.__processor = value

    @property
    def handler(self):
        """:class:`.Handler` instance (read/write).
        """
        return self.__handler

    @handler.setter
    def handler(self, value):
        self.__handler = value
