from abc import ABCMeta, abstractmethod


class Converter(metaclass=ABCMeta):

    # Public

    @property
    @abstractmethod
    def pattern(self):
        pass  # pragma: no cover

    @abstractmethod
    def convert(self, value):
        pass  # pragma: no cover


class StringConverter(Converter):

    # Public

    pattern = r'[^<>/]+'
    convert = str


class IntegerConverter(Converter):

    # Public

    pattern = r'[1-9]+'
    convert = int


class FloatConverter(Converter):

    # Public

    pattern = r'[1-9.]+'
    convert = float


class PathConverter(Converter):

    # Public

    pattern = r'[^<>]+'
    convert = str
