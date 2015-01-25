import asyncio
import traceback
from ..helpers import http
from .record import Record


class Handler(http.Handler):
    """Handler representation.

    Handler is used by :class:`.Service` for handling HTTP requests
    on low-level. It's derived from :class:`.http.Handler`
    and implements :class:`asyncio.Protocol`.

    Example
    -------
    You can tweak some handler parameters like connection timeout
    by subclassing handler. Also you can fully reimplent service's request
    handling logic. Of course it's not recommended but it's possible.
    May be you want to implement a different middleware interface,
    change dispatching logic or provide some optimization::

        class CustomHandler(Handler):

            # Basic

            connection_timeout = 30

            # Advanced

            @asyncio.coroutine
            def handle_request(self, message, payload):
                request = Request(
                    None, message, payload,
                    self.transport, self.reader, self.writer)
                response = ...
                response_message = response.start(request)
                yield from response.write_eof()
                self.keep_alive(response_message.keep_alive())

        service = Service(path='/api/v1', handler=CustomHandler)

    Parameters
    ----------
    service: :class:`.Service`
        Service instance.
    """

    # Public

    connection_timeout = 75
    """Time to keep connection opened in seconds.
    """
    request_timeout = 15
    """Slow request timeout in seconds.
    """

    def __init__(self, service):
        self.__service = service
        loop = None
        if service is not None:
            loop = service.loop
        super().__init__(
            loop=loop,
            keep_alive=self.connection_timeout,
            timeout=self.request_timeout)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def fork(self):
        """Handler factory for asyncio's loop.create_server.
        """
        return type(self)(self.service)

    @asyncio.coroutine
    def handle_request(self, message, payload):
        """Handle a request.

        Parameters
        ----------
        message
            Request's message.
        payload
            Request's payload.
        """
        start_time = self.service.loop.time()
        request = http.Request(
            None, message, payload,
            self.transport, self.reader, self.writer)
        response = yield from self.service.processor.process(request)
        resp_msg = response.start(request)
        yield from response.write_eof()
        self.keep_alive(resp_msg.keep_alive())
        stop_time = self.service.loop.time()
        self.log_access(message, None, resp_msg, stop_time - start_time)

    # Internal (ServerHttpProtocol's API hooks)

    def log_access(self, message, environ, response, time):
        try:
            record = Record(
                request=message, response=response,
                transport=self.transport, duration=time)
            self.service.logger.access(record)
        except:
            self.service.logger.error(traceback.format_exc())

    def log_debug(self, message, *args, **kwargs):
        self.service.logger.debug(message, *args, **kwargs)

    def log_exception(self, message, *args, **kwargs):
        self.service.logger.exception(message, *args, **kwargs)
