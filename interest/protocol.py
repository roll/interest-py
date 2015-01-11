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
            None, message, payload, self.transport,
            self.writer, self.keep_alive_timeout)
        match = yield from dispatcher.resolve(request)
        request.match = match
        try:
            request = yield from processor.process_request(request)
            if not match:
                raise match.exception
            result = yield from match.route.handler(request)
            response = yield from processor.process_result(result)
            response = yield from processor.process_response(response)
        except HTTPException as exception:
            response = yield from processor.process_exception(exception)
        resp_msg = response.start(request)
        yield from response.write_eof()
        self.keep_alive(resp_msg.keep_alive())
        stop_time = self.service.loop.time()
        self.log_access(message, None, resp_msg, stop_time - start_time)
