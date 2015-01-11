import asyncio
from aiohttp.server import ServerHttpProtocol
from aiohttp.web import Request, HTTPException


class Protocol(ServerHttpProtocol):

    def __init__(self, service):
        self.__service = service
        super().__init__(
            loop=service.loop,
            logger=service.logger,
            access_log=service.logger)

    def fork(self):
        return type(self)(self.__service)

    @asyncio.coroutine
    def handle_request(self, message, payload):
        start_time = self.__service.loop.time()
        dispatcher = self.__service.dispatcher
        processor = self.__service.processor
        formatter = self.__service.formatter
        request = Request(
            None, message, payload, self.transport,
            self.writer, self.keep_alive_timeout)
        match = yield from dispatcher.resolve(request)
        request.service = self.__service
        request.match = match
        try:
            request = yield from processor.process_request(request)
            if not match:
                raise match.exception
            data = yield from match.route.handler(request)
            response = formatter.make_response(data)
            response.request = request
            response = yield from processor.process_response(response)
        except HTTPException as exception:
            exception.request = request
            exception = yield from processor.process_exception(exception)
            response = exception
        resp_msg = response.start(request)
        yield from response.write_eof()
        self.keep_alive(resp_msg.keep_alive())
        stop_time = self.__service.loop.time()
        self.log_access(message, None, resp_msg, stop_time - start_time)
