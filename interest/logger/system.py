import logging
from .logger import Logger


class SystemLogger(Logger):
    """Logger implementation on top of logging module.

    Instead of all base Logger no-ops SystemLogger proxyings log calls
    to python's system logger. Access data go to logger with info level.

    Example
    -------
    Obvious improvment of this logger for production use will be
    printing access log to stdout and skipping debug log at all::

        class ProductionLogger(SystemLogger):

            # Public

            name = 'myapp'

            def access(self, record):
                print(self.template % record)

            def debug(self, message, *args, **kwargs):
                pass

        service = Service(path='/api/v1', logger=ProductionLogger)

    .. seealso:: API: :class:`.Logger`
    """

    # Public

    NAME = 'interest'
    """System logger name (default).
    """

    def __init__(self, service, *, template=None, name=None):
        if name is None:
            name = self.NAME
        super().__init__(service, template=template)
        self.__instance = logging.getLogger(name)

    @property
    def instance(self):
        """System logger instanse (read-only).
        """
        return self.__instance

    def access(self, record):
        self.info(self.template % record)

    def debug(self, message, *args, **kwargs):
        self.instance.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.instance.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.instance.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.instance.error(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.instance.exception(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.instance.critical(message, *args, **kwargs)
