import asyncio
from abc import ABCMeta


class Middleware(metaclass=ABCMeta):
    """Middleware representation (abstract).

    Middlewares is used by :class:`.Processor` to process
    handlers and requests.

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Example
    -------
    By default interest doesn't know what to do with data returned
    by processor. We have to implement convertation midleware::

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

    @asyncio.coroutine
    def __call__(self, request):
        """Process a request (coroutine) (proxy).
        """
        return (yield from self.next(request))

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        return type(self).__name__.lower()

    @asyncio.coroutine
    def next(self, request):
        """Call the next middleware (coroutine).
        """
        raise RuntimeError('No next middleware')
