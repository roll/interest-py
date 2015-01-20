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

    # TODO: implement
    def handle_request(self):
        pass

    @patch.object(component, 'Interaction')
    def test_log_access(self, Interaction):
        self.handler.log_access('message', 'environ', 'response', 'time')
        # Check Interaction call
        Interaction.assert_called_with(
            request='message', response='response',
            transport=self.handler.transport, duration='time')
        # Check service.logger call
        self.service.logger.access.assert_called_with(
            Interaction.return_value)

    @patch.object(component, 'traceback')
    @patch.object(component, 'Interaction')
    def test_log_access_with_error(self, Interaction, traceback):
        Interaction.side_effect = RuntimeError()
        self.handler.log_access('message', 'environ', 'response', 'time')
        # Check service.logger call
        self.service.logger.error.assert_called_with(
            traceback.format_exc.return_value)

    def test_log_debug(self):
        self.handler.log_debug('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.logger.debug.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_log_exception(self):
        self.handler.log_exception('message', *self.args, **self.kwargs)
        # Check service.logger call
        self.service.logger.exception.assert_called_with(
            'message', *self.args, **self.kwargs)
