import unittest
from unittest.mock import Mock, patch
from importlib import import_module
component = import_module('interest.handler.record')


class RecordTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.request = Mock(headers={'key': 'value'})
        self.response = Mock(headers={'key': 'value'})
        self.atoms = patch.object(component, 'atoms').start()
        self.atoms.return_value = {'h': 'host'}
        self.record = component.Record(
            request=self.request, response=self.response,
            transport='transport', duration='duration')

    # Tests

    def test(self):
        # Check atoms call
        self.atoms.assert_called_with(
            self.request, None, self.response, 'transport', 'duration')

    def test_key_existent(self):
        self.assertEqual(self.record['host'], 'host')

    def test_key_extended(self):
        self.assertEqual(self.record['<key:req>'], 'value')
        self.assertEqual(self.record['<key:res>'], 'value')

    def test_key_non_existent(self):
        self.assertEqual(self.record['non_existent'], '-')
