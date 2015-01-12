import asyncio
import logging
from .dispatcher import Dispatcher  # @UnusedImport
from .formatter import JSONFormatter  # @UnusedImport
from .handler import Handler  # @UnusedImport
from .processor import Processor  # @UnusedImport


class Service(dict):

    # Public

    def __init__(self, *, path='', loop=None, logger=None,
                 formatter=JSONFormatter, processor=Processor,
                 dispatcher=Dispatcher, handler=Handler):
        if loop is None:
            loop = asyncio.get_event_loop()
        if logger is None:
            logger = logging.getLogger(path)
        self.__path = path
        self.__loop = loop
        self.__logger = logger
        self.__formatter = formatter(self)
        self.__processor = processor(self)
        self.__dispatcher = dispatcher(self)
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
        return self.__path

    @property
    def loop(self):
        return self.__loop

    @property
    def logger(self):
        return self.__logger

    @property
    def formatter(self):
        return self.__formatter

    @formatter.setter
    def formatter(self, value):
        self.__formatter = value

    @property
    def processor(self):
        return self.__processor

    @processor.setter
    def processor(self, value):
        self.__processor = value

    @property
    def dispatcher(self):
        return self.__dispatcher

    @dispatcher.setter
    def dispatcher(self, value):
        self.__dispatcher = value

    @property
    def handler(self):
        return self.__handler

    @handler.setter
    def handler(self, value):
        self.__handler = value
