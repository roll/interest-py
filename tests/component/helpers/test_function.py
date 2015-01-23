import unittest
from unittest.mock import Mock
from importlib import import_module
component = import_module('interest.helpers.function')


class FunctionTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.function = self.make_function()

    # Helpers

    def make_function(self):
        class mock_function(component.Function):
            # Public
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            def __call__(self):
                return (self.args, self.kwargs)
        return mock_function

    def make_function_with_protocol_is_method(self):
        class mock_function(component.Function):
            # Public
            @staticmethod
            def protocol(*args, **kwargs):
                assert args == self.args
                assert kwargs == self.kwargs
                return component.Function.CLASS
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            def __call__(self):
                return (self.args, self.kwargs)
        return mock_function

    def make_function_with_protocol_is_class(self):
        class mock_function(component.Function):
            # Public
            protocol = component.Function.CLASS
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            def __call__(self):
                return (self.args, self.kwargs)
        return mock_function

    def make_function_with_protocol_is_function(self):
        class mock_function(component.Function):
            # Public
            protocol = component.Function.FUNCTION
            def __call__(self, *args, **kwargs):
                return (args, kwargs)
        return mock_function

    def make_function_with_protocol_is_decorator(self):
        class mock_function(component.Function):
            # Public
            protocol = component.Function.DECORATOR
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            def __call__(self, target):
                target.args = self.args
                target.kwargs = self.kwargs
                return target
        return mock_function

    def make_function_with_protocol_is_unsupported(self):
        class mock_function(component.Function):
            # Public
            protocol = 'unsupported'
            def __call__(self, *args, **kwargs):
                return (args, kwargs)
        return mock_function

    # Tests

    def test(self):
        self.assertEqual(
            self.function(*self.args, **self.kwargs),
            (self.args, self.kwargs))

    def test_with_protocol_is_method(self):
        self.function = self.make_function_with_protocol_is_method()
        self.assertEqual(
            self.function(*self.args, **self.kwargs),
            (self.args, self.kwargs))

    def test_with_protocol_is_class(self):
        self.function = self.make_function_with_protocol_is_class()
        self.assertEqual(
            self.function(*self.args, **self.kwargs),
            (self.args, self.kwargs))

    def test_with_protocol_is_function(self):
        self.function = self.make_function_with_protocol_is_function()
        self.assertEqual(
            self.function(*self.args, **self.kwargs),
            (self.args, self.kwargs))

    def test_with_protocol_is_decorator(self):
        target = Mock()
        self.function = self.make_function_with_protocol_is_decorator()
        self.decorator = self.function(*self.args, **self.kwargs)
        self.assertEqual(self.decorator(target), target)
        self.assertEqual(target.args, self.args)
        self.assertEqual(target.kwargs, self.kwargs)

    def test_with_protocol_is_unsupported(self):
        self.function = self.make_function_with_protocol_is_unsupported()
        self.assertRaises(ValueError, self.function)

    def test_isinstance(self):
        self.assertIsInstance(self.function, component.Function)
        self.assertIsInstance(self.function, type(component.Function))
        # Python doesn't call __instancecheck__ on most of isinstance
        # calls but we have to test instance check inheritance
        self.assertFalse(self.function.__instancecheck__(Exception))
