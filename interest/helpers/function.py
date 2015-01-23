from abc import ABCMeta, abstractmethod


class Metaclass(ABCMeta):

    # Public

    def __call__(self, *args, **kwargs):
        function = object.__new__(self)
        protocol = function.protocol
        if callable(function.protocol):
            protocol = function.protocol(*args, **kwargs)
        if protocol == self.CLASS:
            function.__init__(*args, **kwargs)
            return function.__call__()
        elif protocol == self.FUNCTION:
            function.__init__()
            return function.__call__(*args, **kwargs)
        elif protocol == self.DECORATOR:
            function.__init__(*args, **kwargs)
            return function
        else:
            raise ValueError(
                'Unsupported protocol "{protocol}"'.
                format(protocol=protocol))

    def __instancecheck__(self, instance):
        result = issubclass(instance, self)
        if not result:
            result = super().__instancecheck__(instance)
        return result


class Function(metaclass=Metaclass):
    """Abstract class-based function representation.

    Designed to implement functions/decorators as classes
    to work with state and inheritance. In this model function will
    have state only for invocation. Main use case is function like
    parse where there is not global state to create Parser class.
    Also supports decorator protocol to create decorators with parameters.
    User have to implement this abstract class. Examples below will
    make it much more clearer.

    Raises
    ------
    ValueError
      If protocol is unsupported.

    Examples
    --------
    Invocation protocols:

    - Function.CLASS (default)

        >>> class echo(Function):
        ...   protocol = Function.CLASS
        ...   def __init__(self, value):
        ...     self.value = value
        ...   def __call__(self):
        ...     return self.value
        >>> echo('Hello World')
        'Hello World!'

    - Function.FUNCTION

        >>> class echo(Function):
        ...   protocol = Function.FUNCTION
        ...   def __call__(self, value):
        ...     return value
        >>> echo('Hello World!')
        'Hello World!'

    - Function.DECORATOR

        >>> class echo(Function):
        ...   protocol = Function.DECORATOR
        ...   def __init__(self, value):
        ...     self.value = value
        ...   def __call__(self, processor):
        ...     return processor(self.value)
        >>> hello('Hello World!')(str.upper)
        'HELLO WORLD!'
    """

    # Public

    CLASS = 'class'
    FUNCTION = 'function'
    DECORATOR = 'decorator'

    protocol = CLASS
    """Invocation protocol.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """Abstract method to implement.
        """
        pass  # pragma: no cover
