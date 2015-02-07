import asyncio
import traceback
from aiohttp.server import ServerHttpProtocol
from ..backend import http
from ..helpers import Config
from .record import Record


class Handler(Config, ServerHttpProtocol):
    """Handler is a component responsible for the request handling.

    Handler handles requests on low-level. Handler is
    :class:`asyncio.Protocol` implementation derived from
    the aiohttp's :class:`aiohttp.server.ServerHttpProtocol`.

    .. seealso:: Implements:
        :class:`.Config`

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    connection_timeout: int
        Time to keep connection opened in seconds.
    request_timeout: int
        Slow request timeout in seconds.

    Example
    -------
    Let's create a handler and then an asyncio server::

        # Create handler
        handler = Handler(
            '<service>', connection_timeout=25, request_timeout=5)

        # Create server
        loop = asyncio.get_event_loop()
        server = loop.create_server(handler.fork)
        server = self.loop.run_until_complete(server)
    """

    # Public

    CONNECTION_TIMEOUT = 75
    """Time to keep connection opened in seconds (default).
    """
    REQUEST_TIMEOUT = 15
    """Slow request timeout in seconds (default).
    """

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self.__args = args
        self.__kwargs = kwargs
        return self

    def __init__(self, service, *,
                 connection_timeout=None, request_timeout=None):
        if connection_timeout is None:
            connection_timeout = self.CONNECTION_TIMEOUT
        if request_timeout is None:
            request_timeout = self.REQUEST_TIMEOUT
        super().__init__(
            loop=service.loop,
            keep_alive=connection_timeout,
            timeout=request_timeout)
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def fork(self):
        """Handler factory for asyncio's loop.create_server.
        """
        return type(self)(*self.__args, **self.__kwargs)

    # Internal (aiohttp.server.ServerHttpProtocol's hooks)

    @asyncio.coroutine
    def handle_request(self, message, payload):
        start_time = self.service.loop.time()
        request = http.Request(
            None, message, payload,
            self.transport, self.reader, self.writer)
        try:
            response = yield from self.service(request)
        except http.Exception as exception:
            response = exception
        if not isinstance(response, http.StreamResponse):
            raise RuntimeError('Service returned not a StreamResponse')
        resp_msg = response.start(request)
        yield from response.write_eof()
        self.keep_alive(resp_msg.keep_alive())
        stop_time = self.service.loop.time()
        self.log_access(message, None, resp_msg, stop_time - start_time)

    def log_access(self, message, environ, response, time):
        try:
            record = Record(
                request=message, response=response,
                transport=self.transport, duration=time)
            self.service.log('access', record)
        except:
            self.service.log('error', traceback.format_exc())

    def log_debug(self, message, *args, **kwargs):
        self.service.log('debug', message, *args, **kwargs)

    def log_exception(self, message, *args, **kwargs):
        self.service.log('exception', message, *args, **kwargs)
