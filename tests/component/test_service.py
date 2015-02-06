import asyncio
import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.service')


class ServiceTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.loop = Mock()
        self.logger = Mock()
        self.handler = Mock()
        self.Logger = Mock(return_value=self.logger)
        self.Handler = Mock(return_value=self.handler)
        self.service = component.Service(
            loop=self.loop,
            logger=self.Logger,
            handler=self.Handler)

    # Tests

    def test(self):
        # Check class calls
        self.Logger.assert_called_with(self.service)
        self.Handler.assert_called_with(self.service)

    def test_listen(self):
        self.service.listen(host='host', port='port', forever=True)
        # Check loop calls
        self.loop.create_server.assert_called_with(
            self.handler.fork, 'host', 'port')
        self.loop.run_until_complete.assert_called_with(
            self.loop.create_server.return_value)
        self.loop.run_forever.assert_called_with()

    def test_listen_keyboard_interrupt(self):
        self.loop.run_forever.side_effect = KeyboardInterrupt()
        self.service.listen(host='host', port='port', forever=True)

    def test_loop(self):
        self.assertEqual(self.service.loop, self.loop)

    def test_loop_default(self):
        self.service = component.Service()
        self.assertEqual(self.service.loop, asyncio.get_event_loop())
