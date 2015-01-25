from abc import ABCMeta, abstractmethod


class Converter(metaclass=ABCMeta):

    # Public

    @property
    @abstractmethod
    def name(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def pattern(self):
        pass  # pragma: no cover

    @abstractmethod
    def convert(self, value):
        pass  # pragma: no cover


class StringConverter(Converter):

    # Public

    name = 'str'
    pattern = r'[^<>/]+'
    convert = str


class IntegerConverter(Converter):

    # Public

    name = 'int'
    pattern = r'[1-9]+'
    convert = int


class FloatConverter(Converter):

    # Public

    name = 'float'
    pattern = r'[1-9.]+'
    convert = float


class PathConverter(Converter):

    # Public

    name = 'path'
    pattern = r'[^<>]+'
    convert = str
