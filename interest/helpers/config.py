from functools import partial


class Configurable:

    # Public

    @classmethod
    def config(cls, **kwargs):
        return partial(cls, **kwargs)

