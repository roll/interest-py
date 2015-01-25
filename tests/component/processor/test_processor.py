import asyncio
import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.processor.processor')


class ProcessorTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.service = Mock()
        self.Middleware = self.make_mock_middleware_class()
        self.middleware = self.Middleware(self.service)
        self.processor = component.Processor(self.service)
        self.processor.middlewares.add(self.middleware)
        self.processor.middlewares.add(self.middleware)

    # Helpers

    def make_mock_middleware_class(self):
        class MockMiddleware:
            # Public
            name = 'middleware'
            def __init__(self, service):
                pass
            @asyncio.coroutine
            def process_handler(self, handler):
                return handler + '[*]'
            @asyncio.coroutine
            def process_request(self, request):
                return request + '[*]'
        return MockMiddleware

    def unyield(self, coroutine):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(coroutine)
        return result

    # Tests

    def test_service(self):
        self.assertEqual(self.processor.service, self.service)

    def test_middlewares(self):
        self.assertEqual(len(self.processor.middlewares), 2)
