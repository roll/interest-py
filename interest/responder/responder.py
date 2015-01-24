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

    @asyncio.coroutine
    def respond(self, request):
        """Respond a response to a request (coroutine).

        Request will be processed by middleware chain in straight order.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.

        Returns
        -------
        :class:`aiohttp.web.StreamResponse`
            Response instance.

        Raises
        ------
        :class:`TypeError`
            If middleware chain doesn't return
            :class:`aiohttp.web.StreamResponse`.
        """
        response = yield from (self.middlewares + [self.last])[0](request)
        if not isinstance(response, StreamResponse):
            raise TypeError('Last reply is not a StreamResponse')
        return response

    @asyncio.coroutine
    def last(self, request):
        """Call the last (virtual) middleware (coroutine).
        """
        match = yield from self.service.dispatcher.resolve(request)
        request.match = match
        if not match:
            raise match.exception
        reply = yield from match.route.handler(request)
        return reply

    # Private

    def __on_middlewares_change(self):
        next_middleware = None
        for middleware in reversed(self.middlewares):
            middleware.respond = self.last
            if next_middleware is not None:
                middleware.next = next_middleware
            next_middleware = middleware
