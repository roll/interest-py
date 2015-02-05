import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.logger.logger')


class LoggerTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.system = Mock()
        self.logger = component.Logger('service', system=self.system)

    # Helpers

    def make_mock_record_class(self):
        class MockRecord(dict):
            # Public
            def __getitem__(self, key):
                return key
        return MockRecord

    # Tests

    def test_access(self):
        record = self.make_mock_record_class()()
        self.assertIsNone(self.logger.access(record))
        # Check system.info call
        self.system.info.assert_called_with(
            'host time "request" status length "referer" "agent"')

    def test_debug(self):
        self.logger.debug('message', *self.args, **self.kwargs)
        # Check system.debug call
        self.system.debug.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_info(self):
        self.logger.info('message', *self.args, **self.kwargs)
        # Check system.info call
        self.logger.system.info.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_warning(self):
        self.logger.warning('message', *self.args, **self.kwargs)
        # Check system.warning call
        self.system.warning.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_error(self):
        self.logger.error('message', *self.args, **self.kwargs)
        # Check system.error call
        self.system.error.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_exception(self):
        self.logger.exception('message', *self.args, **self.kwargs)
        # Check system.exception call
        self.system.exception.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_critical(self):
        self.logger.critical('message', *self.args, **self.kwargs)
        # Check system.critical call
        self.system.critical.assert_called_with(
            'message', *self.args, **self.kwargs)
