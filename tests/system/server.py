import os
import time
import socket
import asyncio
import aiohttp
import subprocess
from sugarbowl import cachedproperty


class Server:

    # Public

    def __init__(self, path):
        self.__path = path
        self.__loop = asyncio.get_event_loop()

    def listen(self):
        self.process = subprocess.Popen(
            [self.python, self.script, self.hostname, str(self.port)],
            env=self.environ)
        time.sleep(1)

    def close(self):
        self.process.terminate()

    def make_request(self, method, path):
        @asyncio.coroutine
        def coroutine():
            response = yield from aiohttp.request(method, self.make_url(path))
            try:
                response.text = yield from response.text()
                response.json = yield from response.json()
            except Exception:
                pass
            return response
        response = self.__loop.run_until_complete(coroutine())
        return response

    def make_path(self, *paths):
        return os.path.join(os.path.dirname(__file__), '..', '..', *paths)

    def make_url(self, path=''):
        url = 'http://{self.hostname}:{self.port}'.format(self=self)
        url += path
        return url

    @cachedproperty
    def python(self):
        try:
            venv = os.environ['VIRTUAL_ENV']
            return os.path.join(venv, 'bin', 'python3')
        except KeyError:
            return 'python3'

    @cachedproperty
    def script(self):
        return self.make_path(self.__path)

    @cachedproperty
    def hostname(self):
        return '127.0.0.1'

    @cachedproperty
    def port(self):
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    @cachedproperty
    def environ(self):
        env = os.environ.copy()
        env['PYTHONPATH'] = env.get('PYTHONPATH', '') + ':' + self.make_path()
        return env
