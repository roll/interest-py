import traceback
from aiohttp.helpers import SafeAtoms, atoms


class Logger:

    # Public

    template = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

    def __init__(self, service):
        self.__service = service

    @property
    def service(self):
        return self.__service

    # TODO: reimplement
    def format(self, message, environ, response, transport, time):
        try:
            environ = environ if environ is not None else {}
            safe_atoms = SafeAtoms(
                atoms(message, environ, response, transport, time),
                getattr(message, 'headers', None),
                getattr(response, 'headers', None))
            return self.template % safe_atoms
        except:
            self.error(traceback.format_exc())

    def access(self, message, *, environ, response, transport, time):
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
