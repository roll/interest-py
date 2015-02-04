from ..helpers import ExistentMatch, NonExistentMatch
from .converter import Converter
from .pattern import Pattern
from .router import Router


class SystemRouter(Router):
    """Router implementation.
    """

    # Public

    CONVERTERS = {}

    def __init__(self, service, *, converters=None):
        if converters is None:
            converters = self.CONVERTERS
        self.__service = service
        self.__add_converters(converters)
        self.__patterns = {}

    @property
    def service(self):
        """:class:`.Service` instance (read-only).
        """
        return self.__service

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    def match(self, request, *, root=None, path=None, methods=None):
        """Check if request matchs the given parameters.

        Parameters
        ----------
        request: :class:`.http.Request`
            Request instance.
        root: str
            HTTP path root.
        path: str
            HTTP path.
        methods: list
            HTTP methods.

        Returns
        -------
        :class:`.Match`
            Match instance.
        """
        match = ExistentMatch()
        if path is not None:
            pattern = self.__get_pattern(path)
            match = pattern.match(request.path)
        elif root is not None:
            pattern = self.__get_pattern(root)
            match = pattern.match(request.path, left=True)
        if not match:
            return NonExistentMatch()
        if methods:
            methods = map(str.upper, methods)
            if request.method not in methods:
                return NonExistentMatch()
        return match

    # Private

    __CONVERTERS = {
       'str': Converter.config(
            pattern=r'[^<>/]+', convert=str),
       'int': Converter.config(
            pattern=r'[1-9]+', convert=int),
       'float': Converter.config(
            pattern=r'[1-9.]+', convert=float),
       'path': Converter.config(
            pattern=r'[^<>]+', convert=str)}

    def __add_converters(self, converters):
        self.__converters = {}
        econverters = self.__CONVERTERS.copy()
        econverters.update(converters)
        for key, cls in econverters.items():
            self.__converters[key] = cls(self)

    def __get_pattern(self, path):
        if path not in self.__patterns:
            self.__patterns[path] = Pattern.create(
                path, self.__converters)
        return self.__patterns[path]
