from .dispatcher import (Dispatcher, Resource,
                         Binding, get, post, put, delete, patch, head, options,
                         Route, ExistentRoute, NonExistentRoute)
from .handler import Handler, Record
from .logger import Logger, SystemLogger
from .processor import Processor, Middleware, FactoryMiddleware
from .service import Service
version = '0.1.0'  # REPLACE: version = '{{ version }}'
