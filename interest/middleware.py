import asyncio
from abc import ABCMeta
from functools import partial
from .helpers import http


class Middleware(metaclass=ABCMeta):
    """Middleware representation (abstract).

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.

    Example
    -------
    By default interest doesn't know what to do with any request.
    We have to implement a minimal midleware::

        class MinimalMiddleware(Middleware):

            # Public

            @asyncio.coroutine
            def __call__(self, request):
                return Response(text='Hello World!')

        service = Service(path='/api/v1')
        service.add_middleware(MinimalMiddleware)
    """

    # Public

    def __init__(self, service):
        self.__service = service

    # TODO: optimize on metaclass level to reduce calls stack?
    @asyncio.coroutine
    def __call__(self, request):
        return (yield from self.process(request))

    @classmethod
    def config(cls, **kwargs):
        return partial(cls, **kwargs)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        """Middlewares' name.
        """
        return type(self).__name__.lower()

    @asyncio.coroutine
    def process(self, request):
        """Process a request (coroutine).
        """
        return (yield from self.next(request))

    @asyncio.coroutine
    def next(self, request):
        """Call the next middleware (coroutine).
        """
        raise http.NotFound()
