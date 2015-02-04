class Configurable:
    """Configurable representation.
    """

    # Public

    @classmethod
    def config(cls, **defaults):
        return Config(cls, **defaults)


class Config(Configurable):
    """Config representation.
    """

    # Public

    def __init__(self, factory, **defaults):
        self.__factory = factory
        self.__defaults = defaults

    def __call__(self, *args, **kwargs):
        kwargs = self.__merge(self.__defaults, kwargs)
        return self.__factory(*args, **kwargs)

    def __repr__(self):
        template = (
            '<{factory.__name__} configuration with '
            'defaults="{defaults}">')
        compiled = template.format(
            factory=self.__factory,
            defaults=self.__defaults)
        return compiled

    def config(self, **defaults):
        defaults = self.__merge(self.__defaults, defaults)
        return Config(self.__factory, **defaults)

    # Private

    def __merge(self, dict1, dict2):
        merged = dict1.copy()
        merged.update(dict2)
        return merged
