import os
import time
import asyncio
import aiohttp
import subprocess
from .helpers import loop, port, python
from .service import Service


class Tester:

    # Public

    LOOP = loop
    PYTHON = python
    ENVIRON = {}
    SCHEME = 'http'
    HOST = '127.0.0.1'
    PORT = port

    def __init__(self, factory, *,
                 loop=None, python=None, environ=None,
                 scheme=None, host=None, port=None):
        if loop is None:
            loop = self.LOOP
        if python is None:
            python = self.PYTHON
        if environ is None:
            environ = self.ENVIRON
        if scheme is None:
            scheme = self.SCHEME
        if host is None:
            host = self.HOST
        if port is None:
            port = self.PORT
        self.__factory = factory
        self.__loop = loop
        self.__python = python
        self.__environ = environ
        self.__scheme = scheme
        self.__host = host
        self.__port = port
        self.__server = None

    def start(self):
        if isinstance(self.__factory, Service):
            self.__server = self.__loop.create_server(
                self.__factory.handler.fork,
                self.__host, self.__port)
        else:  # Asyncio/Subrocess
            environ = os.environ.copy()
            environ.update(self.__environ)
            self.__server = subprocess.Popen(
                [self.__python, self.__factory,
                 self.__host, str(self.__port)],
                env=environ)
            time.sleep(1)

    def stop(self):
        if isinstance(self.__factory, Service):
            self.__server.close()
        else:  # Asyncio/Subrocess
            self.__server.terminate()

    def request(self, method, path, **kwargs):
        @asyncio.coroutine
        def coroutine():
            response = yield from aiohttp.request(
                method, self.__make_url(path), **kwargs)
            try:
                response.read = yield from response.read()
                response.text = yield from response.text()
                response.json = yield from response.json()
            except Exception:
                pass
            return response
        response = self.__loop.run_until_complete(coroutine())
        return response

    # Private

    def __make_url(self, path=''):
        template = '{scheme}://{host}:{port}{path}'
        compiled = template.format(
            scheme=self.__scheme,
            host=self.__host,
            port=self.__port,
            path=path)
        return compiled
