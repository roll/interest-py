import unittest
from importlib import import_module
component = import_module('interest.helpers.cachedproperty')


class cachedpropertyTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.Consumer = self.make_consumer_class()
        self.consumer = self.Consumer()
        self.consumer.default_prop_value = 'old_value'

    # Helpers

    def make_consumer_class(self):
        class Consumer:
            # Public
            def __init__(self):
                self.default_prop_value = {}
            prop = component.cachedproperty()
            @prop.getter
            def prop(self):
                """docstring"""
                return self.default_prop_value
            @prop.setter
            def prop(self, cache, name, value):
                cache[name] = value
            @prop.deleter
            def prop(self, cache, name):
                del cache[name]
            no_property = component.cachedproperty()
        return Consumer

    # Tests

    def test___doc___(self):
        self.assertEqual(self.Consumer.prop.__doc__, 'docstring')

    def test___get__(self):
        self.assertEqual(self.consumer.prop, 'old_value')
        self.consumer.default_prop_value = 'new_value'
        self.assertEqual(self.consumer.prop, 'old_value')

    def test___get___with_no_property(self):
        self.assertRaises(
            AttributeError, getattr, self.consumer, 'no_property')

    def test___set__(self):
        self.assertEqual(self.consumer.prop, 'old_value')
        self.consumer.prop = 'new_value'
        self.assertEqual(self.consumer.prop, 'new_value')

    def test___set___with_no_property(self):
        self.assertRaises(
            AttributeError, setattr, self.consumer, 'no_property', 'value')

    def test___delete__(self):
        self.assertEqual(self.consumer.prop, 'old_value')
        self.consumer.prop = 'new_value'
        del self.consumer.prop
        self.assertEqual(self.consumer.prop, 'old_value')

    def test___delete___with_no_property(self):
        self.assertRaises(
            AttributeError, delattr, self.consumer, 'no_property')
