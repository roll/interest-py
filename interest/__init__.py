from .dispatcher import Dispatcher, Binding, Converter, Resource, Route, http
from .handler import Handler, Record
from .logger import Logger, SystemLogger
from .processor import Processor, Middleware, FactoryMiddleware
from .service import Service
version = '0.1.0'  # REPLACE: version = '{{ version }}'
