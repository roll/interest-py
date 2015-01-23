import asyncio
import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.responder.responder')


class ResponderTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.service = Mock()
        self.Middleware = self.make_mock_middleware_class()
        self.responder = component.Responder(self.service)
        self.responder.add_middleware(self.Middleware)
        self.responder.add_middleware(self.Middleware)

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
        self.assertEqual(self.responder.service, self.service)

    def test_middlewares(self):
        self.assertEqual(len(self.responder.middlewares), 2)

    def test_add_middleware(self):
        Middleware = Mock()
        self.responder = component.Responder(self.service)
        self.responder.add_middleware(Middleware)
        self.assertEqual(
            self.responder.middlewares,
            [Middleware.return_value])
        # Check Middleware call
        Middleware.assert_called_with(self.service)
