from collections.abc import Iterable


class Chain(Iterable):

    # Public

    def __init__(self, listener):
        self.__listener = listener
        self.__list = []

    def __getitem__(self, key):
        for value in self.__list:
            if value.name == key:
                return value
        raise KeyError(key)

    def __iter__(self):
        return self.__list.__iter__()

    def add(self, value, *, place=None):
        if place is None:
            self.__list.append(value)
        else:
            self.__list.insert(place, value)
        self.listener()
