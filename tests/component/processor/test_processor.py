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

    def make_mock_middleware_class(self, instance=None):
        class MockMiddleware(component.Middleware):
            # Public
            if instance:
                def __new__(cls, service):
                    if instance is not None:
                        return instance
            def process_request(self, request):
                return request + '[*]'
            def process_data(self, request, data):
                return data + '[*]'
            def process_response(self, request, response):
                return response + '[*]'
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
        M1 = self.make_mock_middleware_class('m1')
        M2 = self.make_mock_middleware_class('m2')
        source = Mock()
        source.M3 = self.make_mock_middleware_class('m3')
        self.processor = component.Processor('service')
        self.processor.add_middleware(M1, M2, source=source)
        self.assertEqual(self.processor.middlewares, ['m1', 'm2', 'm3'])

    def test_process_request(self):
        coroutine = self.processor.process_request('request')
        self.assertEqual(self.unyield(coroutine), 'request[*][*]')

    def test_process_result(self):
        mock_isinstance = lambda obj, cls: '[*]' in obj
        coroutine = self.processor.process_result('request', 'result')
        with patch.object(component, 'isinstance', mock_isinstance):
            self.assertEqual(self.unyield(coroutine), 'result[*]')

    def test_process_result_no_middlewares(self):
        self.processor = component.Processor('service')
        coroutine = self.processor.process_result('request', 'result')
        self.assertRaises(RuntimeError, self.unyield, coroutine)

    def test_process_response(self):
        coroutine = self.processor.process_response('request', 'response')
        self.assertEqual(self.unyield(coroutine), 'response[*][*]')

    def test_process_exception(self):
        coroutine = self.processor.process_exception('request', 'exception')
        self.assertEqual(self.unyield(coroutine), 'exception[*][*]')
