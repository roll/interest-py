class Binding:
    """Binding representation.
    """

    # Public

    MARKER = '_interest.binding'

    def __init__(self, responder, *, path=None, methods=None):
        if path is None:
            path = ''
        if methods is None:
            methods = []
        self.__path = path
        self.__methods = methods
        self.__responder = responder

    def __repr__(self):
        template = (
            '<Binding path="{self.path}" methods="{self.methods}" '
            'responder="{self.responder}">')
        compiled = template.format(self=self)
        return compiled

    @property
    def path(self):
        return self.__path

    @property
    def methods(self):
        return self.__methods

    @property
    def responder(self):
        return self.__responder
