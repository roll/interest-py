import asyncio
import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.service')


class ServiceTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.path = 'path'
        self.loop = Mock()
        self.logger = Mock()
        self.formatter = Mock()
        self.dispatcher = Mock()
        self.processor = Mock()
        self.protocol = Mock()
        self.Logger = Mock(return_value=self.logger)
        self.Formatter = Mock(return_value=self.formatter)
        self.Dispatcher = Mock(return_value=self.dispatcher)
        self.Processor = Mock(return_value=self.processor)
        self.Protocol = Mock(return_value=self.protocol)
        self.service = component.Service(
            path=self.path,
            loop=self.loop,
            logger=self.Logger,
            formatter=self.Formatter,
            dispatcher=self.Dispatcher,
            processor=self.Processor,
            protocol=self.Protocol)

    # Tests

    def test(self):
        # Check class calls
        self.Logger.assert_called_with(self.service)
        self.Formatter.assert_called_with(self.service)
        self.Dispatcher.assert_called_with(self.service)
        self.Processor.assert_called_with(self.service)
        self.Protocol.assert_called_with(self.service)

    def test__bool__(self):
        self.assertTrue(self.service)

    def test_add_middleware(self):
        Middleware = Mock()
        self.service.add_middleware(Middleware)
        # Check processor call
        self.processor.middlewares.append.assert_called_with(
            Middleware.return_value)

    def test_add_resource(self):
        Resource = Mock()
        self.service.add_resource(Resource)
        # Check dispatcher call
        self.dispatcher.resources.append.assert_called_with(
            Resource.return_value)

    def test_listen(self):
        self.service.listen(hostname='hostname', port='port')
        # Check loop calls
        self.loop.create_server.assert_called_with(
            self.protocol.fork, 'hostname', 'port')
        self.loop.run_until_complete.assert_called_with(
            self.loop.create_server.return_value)
        self.loop.run_forever.assert_called_with()

    def test_listen_keyboard_interrupt(self):
        self.loop.run_forever.side_effect = KeyboardInterrupt()
        self.service.listen(hostname='hostname', port='port')

    def test_path(self):
        self.assertEqual(self.service.path, self.path)

    def test_path_default(self):
        self.service = component.Service()
        self.assertEqual(self.service.path, '')

    def test_loop(self):
        self.assertEqual(self.service.loop, self.loop)

    def test_loop_default(self):
        self.service = component.Service()
        self.assertEqual(self.service.loop, asyncio.get_event_loop())

    def test_logger(self):
        self.assertEqual(self.service.logger, self.logger)

    def test_logger_setter(self):
        self.service.logger = 'value'
        self.assertEqual(self.service.logger, 'value')

    def test_formatter(self):
        self.assertEqual(self.service.formatter, self.formatter)

    def test_formatter_setter(self):
        self.service.formatter = 'value'
        self.assertEqual(self.service.formatter, 'value')

    def test_dispatcher(self):
        self.assertEqual(self.service.dispatcher, self.dispatcher)

    def test_dispatcher_setter(self):
        self.service.dispatcher = 'value'
        self.assertEqual(self.service.dispatcher, 'value')

    def test_processor(self):
        self.assertEqual(self.service.processor, self.processor)

    def test_processor_setter(self):
        self.service.processor = 'value'
        self.assertEqual(self.service.processor, 'value')

    def test_protocol(self):
        self.assertEqual(self.service.protocol, self.protocol)

    def test_protocol_setter(self):
        self.service.protocol = 'value'
        self.assertEqual(self.service.protocol, 'value')
