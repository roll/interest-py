import sys
from .logger import Logger


# TODO: reimplement
class StreamLogger(Logger):

    # Public

    def write(self, message, *, stream=sys.stdout, flush=True):
        stream.write(message + '\n')
        if flush:
            stream.flush()

    def access(self, message, *, environ, response, transport, time):
        message = self.format(message,
            environ=environ, response=response,
            transport=transport, time=time)
        self.write(message)

    def debug(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)

    def info(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)

    def warning(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)

    def error(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)

    def exception(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)

    def critical(self, message, *args, **kwargs):
        message = ' '.join([message, str(args), str(kwargs)])
        self.write(message, stream=sys.stderr)
