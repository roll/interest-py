class Responder:

    # Public

    def __init__(self, respond, *, name, path, methods):
        self.respond = respond
        self.__name = name
        self.__path = path
        self.__methods = methods

    def __repr__(self):
        template = (
            '<Responder name="{self.name}" path="{self.path}" '
            'methods="{self.methods}">')
        compiled = template.format(self=self)
        return compiled

    def respond(self, request, **match):
        pass  # pragma: no cover

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def methods(self):
        return self.__methods
