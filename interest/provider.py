from abc import ABCMeta, abstractmethod


class Provider(metaclass=ABCMeta):

    # Public

    # Public

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    @property
    @abstractmethod
    def name(self):
        """Provider's name (read-only).
        """
        pass  # pragma: no cover
