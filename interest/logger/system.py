import logging
from .logger import Logger


class SystemLogger(Logger):
    """SystemLogger representation.
    """

    # Public

    name = 'interest'

    def __init__(self, service):
        super().__init__(service)
        self.__system = logging.getLogger(self.name)

    @property
    def system(self):
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
