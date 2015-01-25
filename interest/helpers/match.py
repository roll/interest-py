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

    def __repr__(self):
        template = '<ExistentMatch data="{dict}">'
        compiled = template.format(dict=super().__repr__())
        return compiled


class NonExistentMatch(Match):

    # Public

    def __bool__(self):
        return False

    def __repr__(self):
        template = '<NonExistentMatch data="{dict}">'
        compiled = template.format(dict=super().__repr__())
        return compiled
