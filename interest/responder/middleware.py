import asyncio
from abc import ABCMeta


class Middleware(metaclass=ABCMeta):
    """Middleware representation.

    Middlewares is used by :class:`.Responder` to process
    handlers and requests.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Example
    -------
    By default interest doesn't know what to do with data returned
    by responder. We have to implement convertation midleware::

        class ConvertationMiddleware(Middleware):

            # Public

            @asyncio.coroutine
            def process_data(self, request, data):
                response = Response(
                    text=self.service.formatter.encode(data),
                    content_type=self.service.formatter.content_type)
                return response

        service = Service(path='/api/v1')
        service.add_middleware(ConvertationMiddleware)
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__handler = self.process_request

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @asyncio.coroutine
    def process_handler(self, handler):
        """Process a handler.
        """
        self.handler = handler
        return self.process_request

    @asyncio.coroutine
    def process_request(self, request):
        """Process a request (no-op).
        """
        pass

    @property
    def handler(self):
        """Handler (read/write).
        """
        return self.__handler

    @handler.setter
    def handler(self, value):
        self.__handler = value
