import asyncio
from builtins import isinstance
from aiohttp.web import Response
from .middleware import Middleware


class Processor:
    """Processor representation.

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
        return self.__service

    @property
    def middlewares(self):
        return self.__middlewares

    def add_middleware(self, *middlewares, source=None):
        for middleware in middlewares:
            middleware = middleware(self.service)
            self.middlewares.append(middleware)
        if source is not None:
            for middleware in vars(source).values():
                if isinstance(middleware, type):
                    if issubclass(middleware, Middleware):
                        self.add_middleware(middleware)

    @asyncio.coroutine
    def process_request(self, request):
        for middleware in self.middlewares:
            if hasattr(middleware, 'process_request'):
                request = yield from middleware.process_request(request)
        return request

    @asyncio.coroutine
    def process_result(self, request, result):
        for middleware in self.middlewares:
            if isinstance(result, Response):
                break
            if hasattr(middleware, 'process_data'):
                result = yield from middleware.process_data(request, result)
        if not isinstance(result, Response):
            raise RuntimeError(
                'Middlewares have not properly converted data to response')
        return result

    @asyncio.coroutine
    def process_response(self, request, response):
        """Process response.

        Parameters
        ----------
        request: :class:`aiohttp.web.Request`
            Request instance.
        response: :class:`aiohttp.web.Response`
            Response instance.

        Returns
        -------
        :class:`aiohttp.web.Response`
            Processed response instance.
        """
        for middleware in reversed(self.middlewares):
            if hasattr(middleware, 'process_response'):
                response = (yield from
                    middleware.process_response(request, response))
        return response

    @asyncio.coroutine
    def process_exception(self, request, exception):
        for middleware in reversed(self.middlewares):
            if hasattr(middleware, 'process_exception'):
                exception = (yield from
                    middleware.process_exception(request, exception))
        return exception
