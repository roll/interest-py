class Match(dict):
    """Match representation.
    """

    # Public

    def __bool__(self):
        return True

    def __repr__(self):
        template = '<Match data="{dict}">'
        compiled = template.format(dict=super().__repr__())
        return compiled
