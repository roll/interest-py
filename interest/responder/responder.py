import asyncio
from builtins import isinstance
from aiohttp.web import StreamResponse
from ..helpers import FeedbackList


class Responder:
    """Responder representation.

    Responder is used by :class:`.Service` to respond a response
    on a HTTP request. Responder uses middlewares to make actual job.

    Example
    -------
    For example we don't want to process our responds by middlewares
    in production for performance's sake (save some CPU ticks)::

        class ProductionResponder(Responder):

            # Public

            @asyncio.coroutine
            def process_response(self, request, response):
                return response

        service = Service(path='/api/v1', responder=ProductionResponder)

    Actually we can exclude all middleware logic at all reimplementing
    all Responder.process_* methods. In that case we have to do all
    actual job in Responder's methods.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__middlewares = FeedbackList(
            self.__on_middlewares_change)
        self.__handler = self.process_request

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def middlewares(self):
        """List of middlewares.

        Order corresponds with order of adding and affects order of
        middlewares applying. Client may add middleware instance
        manually to that list.
        """
        return self.__middlewares

    def add_middleware(self, middleware):
        """Add a middleware.

        Parameters
        ----------
        middleware: type
            :class:`.Middleware` subclass.
        """
        middleware = middleware(self.service)
        self.middlewares.append(middleware)

    @asyncio.coroutine
    def respond(self, request):
        """Process request (coroutine).

        Request will be processed by every middleware with
        process_request method in straight order.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.

        Returns
        -------
        :class:`aiohttp.web.Request`
            Processed request instance.
        """
        reply = yield from self.handler(request)
        if not isinstance(reply, StreamResponse):
            raise TypeError('Last reply is not a StreamResponse')
        return reply

    @asyncio.coroutine
    def process_handler(self, handler=None):
        if handler is None:
            handler = self.process_request
        for middleware in reversed(self.middlewares):
            handler = yield from middleware.process_handler(handler)
        self.handler = handler
        return handler

    @asyncio.coroutine
    def process_request(self, request):
        """Process a request (coroutine).
        """
        match = yield from self.service.dispatcher.resolve(request)
        request.match = match
        if not match:
            raise match.exception
        reply = yield from match.route.handler(request)
        return reply

    @property
    def handler(self):
        """Handler (read/write).
        """
        return self.__handler

    @handler.setter
    def handler(self, value):
        self.__handler = value

    # Private

    def __on_middlewares_change(self):
        self.service.loop.run_until_complete(self.process_handler())
