import os
import time
import asyncio
import aiohttp
import unittest
import subprocess


class ExampleTest(unittest.TestCase):

    # Actions

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.env = os.environ.copy()
        cls.env['PYTHONPATH'] = cls.root
        cls.process = subprocess.Popen(
            [cls.python, cls.script, cls.port], env=cls.env)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    # Helpers

    python = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'python3')
    root = os.path.join(os.path.dirname(__file__), '..', '..')
    script = os.path.join('demo', 'example.py')
    hostname = '127.0.0.1'
    port = '5467'

    def make_request(self, method, path):
        @asyncio.coroutine
        def coroutine():
            url = 'http://{hostname}:{port}{path}'.format(
                hostname=self.hostname, port=self.port, path=path)
            response = yield from aiohttp.request(method, url)
            try:
                response.text = yield from response.text()
                response.json = yield from response.json()
            except Exception:
                pass
            return response
        response = self.loop.run_until_complete(coroutine())
        return response

    # Tests

    def test(self):
        response = self.make_request('GET', '/api/v1/comment/7')
        self.assertEqual(response.json, {'id': '7'})
