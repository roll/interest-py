import asyncio
import unittest
from importlib import import_module
from unittest.mock import Mock, patch
component = import_module('interest.protocol.protocol')


class ProtocolTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.service = Mock()
        self.protocol = component.Protocol(self.service)

    # Tests

    def test_service(self):
        self.assertEqual(self.protocol.service, self.service)

    def test_fork(self):
        fork = self.protocol.fork()
        self.assertEqual(type(self.protocol), type(fork))
        self.assertEqual(self.service, fork.service)

    @patch.object(component, 'Request')
    def test_handle_request(self, Request):
        c = asyncio.coroutine
        match = Mock()
        response = Mock()
        response.write_eof = c(lambda: None)
        match.route.protocol = c(lambda req: req)
        self.protocol.log_access = Mock()
        self.service.loop.time.return_value = 10
        self.service.processor.process = c(lambda request: response)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.protocol.handle_request('message', 'payload'))
        # Check Request call
        Request.assert_called_with(
            None, 'message', 'payload',
            self.protocol.transport, self.protocol.reader, self.protocol.writer)
        # Check log_access call
        self.protocol.log_access.assert_called_with(
            'message', None, response.start.return_value, 0)

    @patch.object(component, 'Interaction')
    def test_log_access(self, Interaction):
        self.protocol.log_access('message', 'environ', 'response', 'time')
        # Check Interaction call
        Interaction.assert_called_with(
            request='message', response='response',
            transport=self.protocol.transport, duration='time')
        # Check service.logger call
        self.service.logger.access.assert_called_with(
            Interaction.return_value)

    @patch.object(component, 'traceback')
    @patch.object(component, 'Interaction')
    def test_log_access_with_error(self, Interaction, traceback):
        Interaction.side_effect = RuntimeError()
        self.protocol.log_access('message', 'environ', 'response', 'time')
        # Check service.logger call
        self.service.logger.error.assert_called_with(
            traceback.format_exc.return_value)

    def test_log_debug(self):
        self.protocol.log_debug('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.logger.debug.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_log_exception(self):
        self.protocol.log_exception('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.logger.exception.assert_called_with(
            'message', *self.args, **self.kwargs)
