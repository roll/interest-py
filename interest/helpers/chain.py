from collections.abc import Iterable, Sized


class Chain(Iterable, Sized):
    """Chain representation.
    """

    # Public

    def __init__(self):
        self.__list = []
        self.__dict = {}

    def __getitem__(self, param):
        if isinstance(param, int):
            return self.__list[param]
        return self.__dict[param]

    def __iter__(self):
        return self.__list.__iter__()

    def __bool__(self):
        return bool(self.__list)

    def __len__(self):
        return len(self.__list)

    # Protected

    def _add(self, item, name=None):
        self.__list.append(item)
        if name is not None:
            self.__dict[name] = item
