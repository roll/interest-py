import asyncio
import unittest
from unittest.mock import Mock, patch
from importlib import import_module
component = import_module('interest.processor.processor')


class ProcessorTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.Middleware = self.make_mock_middleware_class()
        self.processor = component.Processor('service')
        self.processor.add_middleware(self.Middleware)
        self.processor.add_middleware(self.Middleware)

    # Helpers

    def make_mock_middleware_class(self):
        class MockMiddleware:
            def __init__(self, service):
                pass
            @asyncio.coroutine
            def process_request(self, request):
                return request + '[*]'
            @asyncio.coroutine
            def process_data(self, request, data):
                return data + '[*]'
            @asyncio.coroutine
            def process_response(self, request, response):
                return response + '[*]'
            @asyncio.coroutine
            def process_exception(self, request, exception):
                return exception + '[*]'
        return MockMiddleware

    def unyield(self, coroutine):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(coroutine)
        return result

    # Tests

    def test_service(self):
        self.assertEqual(self.processor.service, 'service')

    def test_middlewares(self):
        self.assertEqual(len(self.processor.middlewares), 2)

    def test_add_middleware(self):
        Middleware = Mock()
        self.processor = component.Processor('service')
        self.processor.add_middleware(Middleware)
        self.assertEqual(
            self.processor.middlewares,
            [Middleware.return_value])
        # Check Middleware call
        Middleware.assert_called_with('service')

    def test_process_request(self):
        coroutine = self.processor.process_request('request')
        self.assertEqual(self.unyield(coroutine), 'request[*][*]')

    def test_process_reply(self):
        mock_isinstance = lambda obj, cls: '[*]' in obj
        coroutine = self.processor.process_reply('request', 'reply')
        with patch.object(component, 'isinstance', mock_isinstance):
            self.assertEqual(self.unyield(coroutine), 'reply[*]')

    def test_process_reply_no_middlewares(self):
        self.processor = component.Processor('service')
        coroutine = self.processor.process_reply('request', 'reply')
        self.assertRaises(TypeError, self.unyield, coroutine)

    def test_process_response(self):
        coroutine = self.processor.process_response('request', 'response')
        self.assertEqual(self.unyield(coroutine), 'response[*][*]')

    @patch.object(component, 'StreamResponse', str)
    def test_process_exception(self):
        coroutine = self.processor.process_exception('request', 'exception')
        self.assertEqual(self.unyield(coroutine), 'exception[*]')
