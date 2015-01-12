import http
import time
import asyncio
import traceback
from aiohttp import Response
from html import escape as html_escape
from aiohttp.helpers import SafeAtoms, atoms
from aiohttp.server import ServerHttpProtocol
from aiohttp.web import Request, HTTPException


RESPONSES = http.server.BaseHTTPRequestHandler.responses
DEFAULT_ERROR_MESSAGE = """
<html>
  <head>
    <title>{status} {reason}</title>
  </head>
  <body>
    <h1>{status} {reason}</h1>
    {message}
  </body>
</html>"""

ACCESS_LOG_FORMAT = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"')

class Handler(ServerHttpProtocol):

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

    @asyncio.coroutine
    def handle_error(self, status=500,
                     message=None, payload=None, exc=None, headers=None):
        """Handle errors.
        Returns http response with specific status code. Logs additional
        information. It always closes current connection."""
        now = time.time()
        try:
            if self._request_handler is None:
                # client has been disconnected during writing.
                return ()
            if status == 500:
                self.log_exception("Error handling request")
            try:
                reason, msg = RESPONSES[status]
            except KeyError:
                status = 500
                reason, msg = '???', ''
            if self.debug and exc is not None:
                try:
                    tb = traceback.format_exc()
                    tb = html_escape(tb)
                    msg += '<br><h2>Traceback:</h2>\n<pre>{}</pre>'.format(tb)
                except:
                    pass
            html = DEFAULT_ERROR_MESSAGE.format(
                status=status, reason=reason, message=msg).encode('utf-8')
            response = Response(self.writer, status, close=True)
            response.add_headers(
                ('CONTENT-TYPE', 'text/html; charset=utf-8'),
                ('CONTENT-LENGTH', str(len(html))))
            if headers is not None:
                response.add_headers(*headers)
            response.send_headers()
            response.write(html)
            drain = response.write_eof()
            self.log_access(message, None, response, time.time() - now)
            return drain
        finally:
            self.keep_alive(False)

    def log_debug(self, *args, **kw):
        if self.debug:
            self.logger.debug(*args, **kw)

    def log_access(self, message, environ, response, time):
        if self.access_log and self.access_log_format:
            try:
                environ = environ if environ is not None else {}
                safe_atoms = SafeAtoms(
                    atoms(message, environ, response, self.transport, time),
                    getattr(message, 'headers', None),
                    getattr(response, 'headers', None))
                self.access_log.info(self.access_log_format % safe_atoms)
            except:
                self.logger.error(traceback.format_exc())

    def log_exception(self, *args, **kw):
        self.logger.exception(*args, **kw)
