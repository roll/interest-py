class cachedproperty:
    """
    Decorator to implement cached property.

    To cache property value just use cachedproperty decorator
    in class definition instead of regular property decorator::

      class Container:

        @cachedproperty
        def attribute(self):
          return 'value'

        @attribute.setter
        def attribute(self, cache, name, value):
          cache[name] = value

        @attribute.deleter
        def attribute(self, cache, name):
          del cache[name]

    It works for private attributes (__*) and not tested for threads.
    """

    # Public

    def __init__(self, getter=None, setter=None, deleter=None):
        self.getter(getter)
        self.setter(setter)
        self.deleter(deleter)

    def __get__(self, obj, cls):
        if obj is None:
            # To get property from class object
            return self
        if self.__getter is None:
            raise AttributeError('Can\'t get attribute')
        name = self.__get_name(obj)
        cache = self.__get_cache(obj)
        if name not in cache:
            cache[self.__name] = self.__getter(obj)
        return cache[self.__name]

    def __set__(self, obj, value):
        if self.__setter is None:
            raise AttributeError('Can\'t set attribute')
        name = self.__get_name(obj)
        cache = self.__get_cache(obj)
        self.__setter(obj, cache, name, value)

    def __delete__(self, obj):
        if self.__deleter is None:
            raise AttributeError('Can\'t delete attribute')
        name = self.__get_name(obj)
        cache = self.__get_cache(obj)
        self.__deleter(obj, cache, name)

    def getter(self, getter):
        self.__getter = getter
        self.__doc__ = None
        if getter is not None:
            self.__doc__ = getter.__doc__
        return self

    def setter(self, setter):
        self.__setter = setter
        return self

    def deleter(self, deleter):
        self.__deleter = deleter
        return self

    # Private

    __name = None
    __cache = '_cachedproperty'

    def __get_name(self, obj):
        if self.__name is None:
            for cls in type(obj).mro():
                for name, value in vars(cls).items():
                    if self is value:
                        self.__name = name
        return self.__name

    def __get_cache(self, obj):
        return obj.__dict__.setdefault(self.__cache, {})
