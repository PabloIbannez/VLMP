import logging

from typing import List

import abc

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self):
        self.logger = logging.getLogger("VLMP")

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'write') and
                callable(subclass.write)   and
                hasattr(subclass, 'selection') and
                callable(subclass.selection)   and
                NotImplemented)

    @abc.abstractmethod
    def selection(self, **kwargs):
        """ Return a index of the particles that are selected """
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, filePath: str):
        """Write model to file using json format"""
        raise NotImplementedError
