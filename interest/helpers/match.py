class Match(dict):
    """Match is a dictionary which always resolves to True in boolean context.

    .. seealso:: Implements:
        :class:`dict`
    """

    # Public

    def __bool__(self):
        return True

    def __repr__(self):
        template = '<Match data="{dict}">'
        compiled = template.format(dict=super().__repr__())
        return compiled
