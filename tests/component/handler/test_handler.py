import unittest
from unittest.mock import Mock
from importlib import import_module
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

    # TODO: implement
    def test_log_access(self):
        pass

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
