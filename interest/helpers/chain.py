from collections.abc import Iterable, Sized


class Chain(Iterable, Sized):
    """Chain is a enhanced sequence.
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

    def __setitem__(self, param, item):
        if isinstance(param, int):
            self.__list.pop(param)
            index = param
        else:
            prev = self.__dict.pop(param)
            index = self.__list.index(prev)
        self.push(item, index=index)

    def __iter__(self):
        return self.__list.__iter__()

    def __bool__(self):
        return bool(self.__list)

    def __len__(self):
        return len(self.__list)

    def push(self, item, *, index=None):
        """Push item to the chain.
        """
        if index is None:
            self.__list.append(item)
        else:
            self.__list.insert(index, item)
        name = getattr(item, 'name', None)
        if name is not None:
            self.__dict[name] = item

    def pull(self, *, index=None):
        """Pull item from the chain.
        """
        item = self.__list.pop(index)
        name = getattr(item, 'name', None)
        if name is not None:
            del self.__dict[name]
        return item
