from collections.abc import Iterable, Sized


class Chain(Iterable, Sized):

    # Public

    def __init__(self, listener=None):
        self.__listener = listener
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

    def __repr__(self):
        template = '<Chain elements="{list}">'
        compiled = template.format(list=self.__list)
        return compiled

    def add(self, value, place=None):
        if place is None:
            self.__list.append(value)
        else:
            self.__list.insert(place, value)
        self.__dict[value.name] = value
        if self.__listener is not None:
            self.__listener()
