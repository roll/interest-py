from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    """Formatter representation.
    """

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        return self.__service

    @property
    @abstractmethod
    def content_type(self):
        pass  # pragma: no cover

    @abstractmethod
    def decode(self, text):
        pass  # pragma: no cover

    @abstractmethod
    def encode(self, data):
        pass  # pragma: no cover
