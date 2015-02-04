from functools import partial


class Configurable:
    """Configurable representation.
    """

    # Public

    @classmethod
    def config(cls, **kwargs):
        return partial(cls, **kwargs)

