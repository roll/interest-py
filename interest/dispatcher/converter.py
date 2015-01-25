from abc import ABCMeta, abstractmethod


class Converter(metaclass=ABCMeta):

    # Public

    def __init__(self, service):
        self.__service = service

    def __repr__(self):
        template = (
            '<Converter name="{self.name}" pattern="{self.pattern}"'
            'convert="{self.convert}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def service(self):
        return self.__service

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
