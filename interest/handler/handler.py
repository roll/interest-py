import asyncio
import traceback
from aiohttp.server import ServerHttpProtocol
from aiohttp.web import Request, HTTPException
from .interaction import Interaction


class Handler(ServerHttpProtocol):
    """Handler representation.
    """

    # Public

    def __init__(self, service):
        self.__service = service
        super().__init__(loop=service.loop)

    @property
    def service(self):
        return self.__service

    def fork(self):
        return type(self)(self.service)

    @asyncio.coroutine
    def handle_request(self, message, payload):
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
            response = (yield from
                processor.process_exception(request, exception))
        response_message = response.start(request)
        yield from response.write_eof()
        self.keep_alive(response_message.keep_alive())
        stop_time = self.service.loop.time()
        self.log_access(message, None, response_message, stop_time - start_time)

    def log_access(self, message, environ, response, time):
        try:
            interaction = Interaction(
                request=message, response=response,
                transport=self.transport, duration=time)
            self.service.logger.access(interaction)
        except:
            self.service.logger.error(traceback.format_exc())

    def log_debug(self, message, *args, **kwargs):
        self.service.logger.debug(message, *args, **kwargs)

    def log_exception(self, message, *args, **kwargs):
        self.service.logger.exception(message, *args, **kwargs)
