from abc import ABCMeta
from collections import OrderedDict


class OrderedMetaclass(ABCMeta):

    # Public

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, attrs):
        attrs['__order__'] = tuple(attrs)
        return super().__new__(cls, name, bases, attrs)
