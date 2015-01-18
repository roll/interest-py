import unittest
from unittest.mock import Mock, patch
from importlib import import_module
component = import_module('interest.logger.system')


class SystemLoggerTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.addCleanup(patch.stopall)
        self.logging = patch.object(component, 'logging').start()
        self.Logger = self.make_mock_logger_class()
        self.logger = self.Logger('service')

    # Helpers

    def make_mock_logger_class(self):
        class MockLogger(component.SystemLogger):
            # Public
            name = 'name'
            format = Mock()
        return MockLogger

    # Tests

    def test_system(self):
        self.assertEqual(
            self.logger.system,
            self.logging.getLogger.return_value)
        # Check logging.getLogger call
        self.logging.getLogger.assert_called_with(self.logger.name)

    def test_access(self):
        self.assertIsNone(
            self.logger.access(
                'message', environ='environ', response='response',
                transport='transport', time='time'))
        # Check system.info call
        self.logger.system.info.assert_called_with(
            self.logger.format.return_value)

    def test_debug(self):
        self.assertIsNone(
            self.logger.debug(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.debug.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_info(self):
        self.assertIsNone(
            self.logger.info(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.info.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_warning(self):
        self.assertIsNone(
            self.logger.warning(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.warning.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_error(self):
        self.assertIsNone(
            self.logger.error(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.error.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_exception(self):
        self.assertIsNone(
            self.logger.exception(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.exception.assert_called_with(
            'message', *self.args, **self.kwargs)

    def test_critical(self):
        self.assertIsNone(
            self.logger.critical(
                'message', *self.args, **self.kwargs))
        # Check system.debug call
        self.logger.system.critical.assert_called_with(
            'message', *self.args, **self.kwargs)
