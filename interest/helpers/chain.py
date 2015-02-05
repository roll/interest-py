from collections.abc import Iterable, Sized


class Chain(Iterable, Sized):
    """Chain representation.
    """

    # Public

    def __init__(self, *args, **kwargs):
        self.__list = []
        self.__dict = {}
        super().__init__(*args, **kwargs)

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

    def push(self, item, place=None):
        """Push item to the chain.
        """
        if place is None:
            self.__list.append(item)
        else:
            self.__list.insert(place, item)
        name = getattr(item, 'name', None)
        if name is not None:
            self.__dict[name] = item

    def pull(self, place=None):
        """Pull item from the chain.
        """
        item = self.__list.pop(place)
        name = getattr(item, 'name', None)
        if name is not None:
            del self.__dict[name]
