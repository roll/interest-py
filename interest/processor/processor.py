import asyncio
from builtins import isinstance
from ..helpers import Chain, http


class Processor:
    """Processor representation.

    Processor is used by :class:`.Service` to process HTTP requests.
    Processor uses middlewares to include user code in request processing.
    Processor needs at least one middleware to work.

    Parameters
    ----------
    service: :class:`Service`
        Service instance.

    Example
    -------
    For example we don't want to process our responds by middlewares
    in production for performance's sake (save some CPU ticks)::

        class ProductionProcessor(Processor):

            # Public

            @asyncio.coroutine
            def process(self, request):
                return http.Response()

        service = Service(path='/api/v1', processor=ProductionProcessor)

    Of course it makes no sense but there is for example's sake.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        self.__middlewares = Chain(
            self.__on_middlewares_change)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def middlewares(self):
        """:class:`.Chain` of middlewares.

        Order corresponds with order of adding and affects order of
        middlewares applying. Client may add middleware instance
        manually to that list.
        """
        return self.__middlewares

    @asyncio.coroutine
    def process(self, request):
        """Respond a response to a request (coroutine).

        Request will be processed by middlewares chain in straight order.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.

        Returns
        -------
        :class:`.http.StreamResponse`
            Response instance.

        Raises
        ------
        :class:`RuntimeError`
            If middlewares chain doesn't return
            :class:`.http.StreamResponse`.
        """
        if not self.middlewares:
            raise RuntimeError('No middlawares added')
        try:
            response = yield from self.middlewares[0].process(request)
        except http.Exception as exception:
            return exception
        if not isinstance(response, http.StreamResponse):
            raise RuntimeError('Last reply is not a StreamResponse')
        return response

    # Private

    def __on_middlewares_change(self):
        next_middleware = None
        for middleware in reversed(self.middlewares):
            if next_middleware is not None:
                middleware.next = next_middleware.process
            next_middleware = middleware
