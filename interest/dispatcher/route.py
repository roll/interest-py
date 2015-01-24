from abc import ABCMeta, abstractmethod


class Route(dict, metaclass=ABCMeta):
    """Route representation.
    """

    # Public

    @abstractmethod
    def __bool__(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def responder(self):
        pass  # pragma: no cover


class ExistentRoute(Route):
    """ExistentRoute representation.
    """

    # Public

    def __init__(self, responder, match):
        self.__responder = responder
        super().__init__(match)

    def __bool__(self):
        return True

    @property
    def responder(self):
        return self.__responder


class NonExistentRoute(Route):
    """NonExistentRoute representation.
    """

    # Public

    def __init__(self, responder, exception):
        self.__responder = responder
        self.__exception = exception

    def __bool__(self):
        return False

    @property
    def responder(self):
        return self.__responder

    @property
    def exception(self):
        return self.__exception
