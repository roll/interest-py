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

            def access(self, interaction):
                print(self.template % interaction)

            def debug(self, message, *args, **kwargs):
                pass

        service = Service(path='/api/v1', logger=ProductionLogger)

    .. seealso:: API: :class:`.Logger`
    """

    # Public

    name = 'interest'
    """System logger name.
    """

    def __init__(self, service):
        super().__init__(service)
        self.__system = logging.getLogger(self.name)

    @property
    def system(self):
        """System logger instanse.
        """
        return self.__system

    def access(self, interaction):
        self.info(self.template % interaction)

    def debug(self, message, *args, **kwargs):
        self.system.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.system.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.system.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.system.error(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.system.exception(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.system.critical(message, *args, **kwargs)
