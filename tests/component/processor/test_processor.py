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
        self.processor = component.Processor(self.service)
        self.processor.add_middleware(self.Middleware)
        self.processor.add_middleware(self.Middleware)

    # Helpers

    def make_mock_middleware_class(self):
        class MockMiddleware:
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

    def test_add_middleware(self):
        Middleware = Mock()
        self.processor = component.Processor(self.service)
        self.processor.add_middleware(Middleware)
        self.assertEqual(
            self.processor.middlewares,
            [Middleware.return_value])
        # Check Middleware call
        Middleware.assert_called_with(self.service)
