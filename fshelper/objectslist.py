from typing import Iterable


class FileSystemObjectsList(list):
    """
    List for filesystem objects
    to control some behavior
    """

    def __init__(self):
        self._objects = []

    def __get__(self, obj, objtype):
        return self._objects

    def __set__(self, obj, value):
        self._objects = []
        self.append(value)

    def append(self, value):
        # overriding base append method to add validations
        if isinstance(value, Iterable):
            for v in value:
                if self._validate(v):
                    super().append(v)
        elif self._validate(value):
            super().append(value)

    def _validate(self, value):
        from .base import BaseFileSystemObject
        if isinstance(value, BaseFileSystemObject):
            return True
        else:
            raise Exception("Unknown object type. It should be an instance \
                 of list of instances of BaseFileSystemObject.")
