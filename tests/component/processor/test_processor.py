import unittest
from importlib import import_module
component = import_module('interest.processor.processor')


class ProcessorTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.processor = component.Processor('service')

    # Tests

    def test_service(self):
        self.assertEqual(self.processor.service, 'service')
