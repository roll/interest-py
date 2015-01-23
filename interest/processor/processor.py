import asyncio
from builtins import isinstance
from aiohttp.web import StreamResponse


class Processor:
    """Processor representation.

    Processor is used by :class:`.Service` for
    request/response/reply/exception processing for every HTTP request.
    Processor uses middlewares to make actual job.

    Example
    -------
    For example we don't want to process our responds by middlewares
    in production for performance's sake (save some CPU ticks)::

        class ProductionProcessor(Processor):

            # Public

            @asyncio.coroutine
            def process_response(self, request, response):
                return response

        service = Service(path='/api/v1', processor=ProductionProcessor)

    Actually we can exclude all middleware logic at all reimplementing
    all Processor.process_* methods. In that case we have to do all
    actual job in Processor's methods.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__middlewares = []

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def middlewares(self):
        """List of processor middlewares.

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
    def process_request(self, request):
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
        for middleware in self.middlewares:
            if hasattr(middleware, 'process_request'):
                request = yield from middleware.process_request(request)
        return request

    @asyncio.coroutine
    def process_reply(self, request, reply):
        """Process reply (coroutine).

        While reply is not instance of :class:`aiohttp.web.StreamResponse`
        it will be processed by middlewares with process_data method
        in reverse order.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.
        reply: dict/:class:`aiohttp.web.StreamResponse`
            Endpoint's return.

        Returns
        -------
        :class:`aiohttp.web.StreamResponse`
            Response instance.

        Raises
        ------
        :class:`TypeError`
            If reply is not instance of :class:`aiohttp.web.StreamResponse`
            after processing by all middlewares.
        """
        for middleware in self.middlewares:
            if isinstance(reply, StreamResponse):
                break
            if hasattr(middleware, 'process_data'):
                reply = yield from middleware.process_data(request, reply)
        if not isinstance(reply, StreamResponse):
            raise TypeError(
                'Middlewares have not properly converted data to response')
        return reply

    @asyncio.coroutine
    def process_response(self, request, response):
        """Process response (coroutine).

        Response will be processed by every middleware with
        process_response method in reverse order.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.
        response: :class:`aiohttp.web.StreamResponse`
            Response instance.

        Returns
        -------
        :class:`aiohttp.web.StreamResponse`
            Processed response instance.
        """
        for middleware in reversed(self.middlewares):
            if hasattr(middleware, 'process_response'):
                response = (yield from
                    middleware.process_response(request, response))
        return response

    @asyncio.coroutine
    def process_exception(self, request, exception):
        """Process exception (coroutine).

        Exception will be processed by middlewares with process_exception
        method in reverse order until :class:`aiohttp.web.StreamResponse`
        will be returned otherwise processed exception will be raised.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.
        exception: :class:`aiohttp.web.HTTPException`
            Exception instance.

        Returns
        -------
        :class:`aiohttp.web.StreamResponse`
            Response instance.

        Raises
        ------
        :class:`Exception`
            If no one middleware returns :class:`aiohttp.web.StreamResponse`
            methods raises processed exception.
        """
        for middleware in self.middlewares:
            if hasattr(middleware, 'process_exception'):
                result = (yield from
                    middleware.process_exception(request, exception))
                if isinstance(exception, StreamResponse):
                    return result
                exception = result
        raise exception
