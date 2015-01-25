from abc import ABCMeta, abstractmethod


class Match(dict, metaclass=ABCMeta):

    # Public

    @abstractmethod
    def __bool__(self):
        pass  # pragma: no cover


class ExistentMatch(Match):

    # Public

    def __bool__(self):
        return True


class NonExistentMatch(Match):

    # Public

    def __bool__(self):
        return False
