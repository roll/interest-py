class Config:
    """Config is a interface to fork classes.
    """

    # Public

    @classmethod
    def config(cls, **defaults):
        """Return config with updated defaults.

        Parameters
        ----------
        defaults: dict
            Defaults values.

        Returns
        -------
        :class:`.Config`
            Config with updated defaults.
        """
        return ConfigEdition(cls, **defaults)


class ConfigEdition(Config):
    """Config edition representation.
    """

    # Public

    def __init__(self, factory, **defaults):
        self.__factory = factory
        self.__add_defaults(defaults)

    def __call__(self, *args, **kwargs):
        kwargs = self.__merge_dicts(self.__defaults, kwargs)
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
        defaults = self.__merge_dicts(self.__defaults, defaults)
        return Config(self.__factory, **defaults)

    # Private

    def __add_defaults(self, defaults):
        self.__defaults = defaults
        for key, value in defaults.items():
            setattr(self, key.upper(), value)

    def __merge_dicts(self, dict1, dict2):
        merged = dict1.copy()
        merged.update(dict2)
        return merged
