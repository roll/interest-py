from abc import ABCMeta


class Logger(metaclass=ABCMeta):
    """Logger representation.
    """

    # Public

    template = ('%(host)s %(time)s "%(request)s" %(status)s '
                '%(length)s "%(referer)s" "%(agent)s"')

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        return self.__service

    def access(self, interaction):
        pass

    def debug(self, message, *args, **kwargs):
        pass

    def info(self, message, *args, **kwargs):
        pass

    def warning(self, message, *args, **kwargs):
        pass

    def error(self, message, *args, **kwargs):
        pass

    def exception(self, message, *args, **kwargs):
        pass

    def critical(self, message, *args, **kwargs):
        pass
