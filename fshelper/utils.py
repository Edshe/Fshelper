from typing import Iterable
from .base import BaseDirectory, BaseFile


def to_json(objects: Iterable) -> Iterable:
    result = []
    for object in objects:
        result.append(object.__repr__())
    return result


def from_json(objects: Iterable) -> Iterable:
    result = []
    for object in objects:
        type, path = object.__repr__().split(' ')
        if type == 'BaseDirectory':
            result.appen(BaseDirectory(path=path))
        elif type == 'BaseFile':
            result.appen(BaseFile(path=path))
        else:
            print('Unknown object type: {}: {}. Skipped.'.format(type, path))
    return result
