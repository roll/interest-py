from abc import ABCMeta, abstractmethod


class Match(dict, metaclass=ABCMeta):
    """Match representation.
    """

    # Public

    @abstractmethod
    def __bool__(self):
        pass  # pragma: no cover


class ExistentMatch(Match):
    """ExistentMatch representation.
    """

    # Public

    def __init__(self, route, *, groups):
        self.__route = route
        super().__init__(groups)

    def __bool__(self):
        return True

    @property
    def route(self):
        return self.__route


class NonExistentMatch(Match):
    """NonExistentMatch representation.
    """

    # Public

    def __init__(self, exception):
        self.__exception = exception

    def __bool__(self):
        return False

    @property
    def exception(self):
        return self.__exception
