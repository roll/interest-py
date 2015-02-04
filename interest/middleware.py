import asyncio
from .helpers import Configurable, name
from .protocol import http


class Middleware(Configurable):
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

    NAME = name
    PATH = ''
    METHODS = []

    def __init__(self, service, *, name=None, path=None, methods=None):
        if name is None:
            name = self.NAME
        if path is None:
            path = self.PATH
        if methods is None:
            methods = self.METHODS
        if self is not service:
            path = service.path + path
        self.__service = service
        self.__name = name
        self.__path = path
        self.__methods = methods

    @asyncio.coroutine
    def __call__(self, request):
        match = self.service.router.match(
            request, root=self.path, methods=self.methods)
        if match:
            return (yield from self.process(request))
        return (yield from self.next(request))

    def __repr__(self):
        template = (
            '<Middleware path="{self.path}" '
            'methods="{self.methods}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    def name(self):
        """Middleware's name (read-only).
        """
        return self.__name

    @property
    def path(self):
        """Middleware's path (read-only).
        """
        return self.__path

    @property
    def methods(self):
        """Middleware's methods (read-only).
        """
        return self.__methods

    @asyncio.coroutine
    def process(self, request):
        """Process a request (coroutine).

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
        return (yield from self.next(request))

    @asyncio.coroutine
    def next(self, request):
        """Call the next middleware (coroutine).
        """
        raise http.NotFound()
