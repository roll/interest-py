import asyncio
import unittest
from importlib import import_module
from unittest.mock import Mock, patch
component = import_module('interest.handler.handler')


class HandlerTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.service = Mock()
        self.handler = component.Handler(self.service)

    # Tests

    def test_service(self):
        self.assertEqual(self.handler.service, self.service)

    def test_fork(self):
        fork = self.handler.fork()
        self.assertEqual(type(self.handler), type(fork))
        self.assertEqual(self.service, fork.service)

    @unittest.skip
    @patch.object(component.http, 'Request')
    def test_handle_request(self, Request):
        c = asyncio.coroutine
        match = Mock()
        response = Mock()
        response.write_eof = c(lambda: None)
        match.route.handler = c(lambda req: req)
        self.handler.log_access = Mock()
        self.service.loop.time.return_value = 10
        self.service.process = c(lambda request: response)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.handler.handle_request('message', 'payload'))
        # Check Request call
        Request.assert_called_with(
            None, 'message', 'payload',
            self.handler.transport, self.handler.reader, self.handler.writer)
        # Check log_access call
        self.handler.log_access.assert_called_with(
            'message', None, response.start.return_value, 0)

    @patch.object(component, 'Record')
    def test_log_access(self, Record):
        self.handler.log_access('message', 'environ', 'response', 'time')
        # Check Record call
        Record.assert_called_with(
            request='message', response='response',
            transport=self.handler.transport, duration='time')
        # Check service.logger call
        self.service.log.assert_called_with(
            'access', Record.return_value)

    @patch.object(component, 'traceback')
    @patch.object(component, 'Record')
    def test_log_access_with_error(self, Record, traceback):
        Record.side_effect = RuntimeError()
        self.handler.log_access('message', 'environ', 'response', 'time')
        # Check service.logger call
        self.service.log.assert_called_with(
            'error', traceback.format_exc.return_value)

    def test_log_debug(self):
        self.handler.log_debug('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.log.assert_called_with(
            'debug', 'message', *self.args, **self.kwargs)

    def test_log_exception(self):
        self.handler.log_exception('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.log.assert_called_with(
            'exception', 'message', *self.args, **self.kwargs)
