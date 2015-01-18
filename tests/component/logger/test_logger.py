import unittest
from importlib import import_module
component = import_module('interest.logger.logger')


class LoggerTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.Logger = self.make_mock_logger_class()
        self.logger = self.Logger('service')

    # Helpers

    def make_mock_logger_class(self):
        class MockLogger(component.Logger):
            # Public
            pass
        return MockLogger

    # Tests

    def test_template(self):
        self.assertEqual(
            self.logger.template,
            '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"')

    def test_service(self):
        self.assertEqual(self.logger.service, 'service')

    # TODO: implement
    def test_format(self):
        pass

    def test_access(self):
        self.assertIsNone(
            self.logger.access(
                'message', environ='environ', response='response',
                transport='transport', time='time'))

    def test_debug(self):
        self.assertIsNone(
            self.logger.debug(
                'message', *self.args, **self.kwargs))

    def test_info(self):
        self.assertIsNone(
            self.logger.info(
                'message', *self.args, **self.kwargs))

    def test_warning(self):
        self.assertIsNone(
            self.logger.warning(
                'message', *self.args, **self.kwargs))

    def test_error(self):
        self.assertIsNone(
            self.logger.error(
                'message', *self.args, **self.kwargs))

    def test_exception(self):
        self.assertIsNone(
            self.logger.exception(
                'message', *self.args, **self.kwargs))

    def test_critical(self):
        self.assertIsNone(
            self.logger.critical(
                'message', *self.args, **self.kwargs))
