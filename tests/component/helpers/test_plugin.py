import unittest
from importlib import import_module
from unittest.mock import patch
component = import_module('interest.helpers.plugin')


class PluginImporterTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.sys = patch.object(component, 'sys').start()
        self.import_module = patch.object(component, 'import_module').start()
        self.importer = component.PluginImporter(
            virtual='virtual', actual='actual')

    # Tests

    def test___eq__(self):
        importer1 = component.PluginImporter(virtual='s1', actual='t1')
        importer2 = component.PluginImporter(virtual='s1', actual='t1')
        importer3 = component.PluginImporter(virtual='s3', actual='t3')
        self.assertEqual(importer1, importer2)
        self.assertNotEqual(importer1, importer3)

    def test_virtual(self):
        self.assertEqual(self.importer.virtual, 'virtual')

    def test_actual(self):
        self.assertEqual(self.importer.actual, 'actual')

    def test_register(self):
        self.sys.meta_path = []
        self.importer.register()
        self.importer.register()
        # Check just 1 importer added
        self.assertEqual(self.sys.meta_path, [self.importer])

    def test_find_module(self):
        self.assertEqual(
            self.importer.find_module('virtual_name'),
            self.importer)

    def test_find_module_not_match(self):
        self.assertIsNone(self.importer.find_module('not_virtual_name'))

    def test_load_module(self):
        self.sys.modules = {}
        self.assertEqual(
            self.importer.load_module('virtual_name'),
            self.import_module.return_value)
        # Check sys.modules
        self.assertEqual(
            self.sys.modules,
            {'virtual_name': self.import_module.return_value,
             'actual_name': self.import_module.return_value})

    def test_load_module_already_in_sys_modules(self):
        self.sys.modules = {'virtual_name': 'module'}
        self.assertEqual(self.importer.load_module('virtual_name'), 'module')

    def test_load_module_not_match(self):
        self.sys.modules = {'virtual_name': 'module'}
        self.assertRaises(ImportError,
            self.importer.load_module, 'not_virtual_name')
