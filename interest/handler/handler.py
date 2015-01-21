import asyncio
import traceback
from aiohttp.server import ServerHttpProtocol
from aiohttp.web import Request, HTTPException
from .interaction import Interaction


class Handler(ServerHttpProtocol):
    """Handler representation.

    Handler is used by :class:`.Service` for handling HTTP requests
    on low-level. It's derived from :class:`aiohttp.server.ServerHttpProtocol`
    and implements :class:`asyncio.Protocol`.

    Example
    -------
    You can tweak some handler parameters like keep alive timeout
    by subclassing Handler. Also you can fully reimplent service's request
    handling logic. Of course it's not recommended but it's possible.
    May be you want to implement a different middleware interface,
    change dispatching logic or provide some optimization::

        class CustomHandler(Handler):

            # Basic

            # TODO: add parameters tweak!

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

    def __init__(self, service):
        self.__service = service
        loop = None
        if service is not None:
            loop = service.loop
        super().__init__(loop=loop)

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def fork(self):
        """Protocol factory for asyncio's loop.create_server.
        """
        return type(self)(self.service)

    @asyncio.coroutine
    def handle_request(self, message, payload):
        """Handle a request.

        Parameters
        ----------
        message
            Message.
        payload
            Payload.
        """
        start_time = self.service.loop.time()
        dispatcher = self.service.dispatcher
        processor = self.service.processor
        request = Request(
            None, message, payload,
            self.transport, self.reader, self.writer)
        match = yield from dispatcher.resolve(request)
        request.match = match
        try:
            request = yield from processor.process_request(request)
            if not match:
                raise match.exception
            result = yield from match.route.handler(request)
            response = yield from processor.process_result(request, result)
            response = yield from processor.process_response(request, response)
        except HTTPException as exception:
            try:
                response = (yield from
                    processor.process_exception(request, exception))
            except HTTPException as exception:
                response = exception
        resp_message = response.start(request)
        yield from response.write_eof()
        self.keep_alive(resp_message.keep_alive())
        stop_time = self.service.loop.time()
        self.log_access(message, None, resp_message, stop_time - start_time)

    def log_access(self, message, environ, response, time):
        # For internal use (ServerHttpProtocol's API)
        try:
            interaction = Interaction(
                request=message, response=response,
                transport=self.transport, duration=time)
            self.service.logger.access(interaction)
        except:
            self.service.logger.error(traceback.format_exc())

    def log_debug(self, message, *args, **kwargs):
        # For internal use (ServerHttpProtocol's API)
        self.service.logger.debug(message, *args, **kwargs)

    def log_exception(self, message, *args, **kwargs):
        # For internal use (ServerHttpProtocol's API)
        self.service.logger.exception(message, *args, **kwargs)
