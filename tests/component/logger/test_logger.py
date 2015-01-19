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
            '%(host)s %(time)s "%(request)s" %(status)s '
            '%(length)s "%(referer)s" "%(agent)s"')

    def test_service(self):
        self.assertEqual(self.logger.service, 'service')

    def test_access(self):
        self.logger.access('instance')

    def test_debug(self):
        self.logger.debug('message', *self.args, **self.kwargs)

    def test_info(self):
        self.logger.info('message', *self.args, **self.kwargs)

    def test_warning(self):
        self.logger.warning('message', *self.args, **self.kwargs)

    def test_error(self):
        self.logger.error('message', *self.args, **self.kwargs)

    def test_exception(self):
        self.logger.exception('message', *self.args, **self.kwargs)

    def test_critical(self):
        self.logger.critical('message', *self.args, **self.kwargs)
