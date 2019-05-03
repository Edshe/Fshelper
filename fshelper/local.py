import os
import abc
from .base import BaseDirectory, BaseFile


class LocalObjectMixin(metaclass=abc.ABCMeta):

    _parent = None

    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @property
    def name(self) -> str:
        """
        Method returns a name of an object
        """
        if not hasattr(self, '_name'):
            self._name = self.path.strip('/').split('/')[-1]
        return self._name

    @property
    def parent(self):
        """
        Method returns a parent directory
        """
        return self._parent


class LocalDirectory(LocalObjectMixin, BaseDirectory):

    def _get_child_directory(self, path):
        """
        Method returns a new LocalDirectory
        object for specified path
        """
        return LocalDirectory(
            parent=self,
            path=path
        )

    def _get_objects(self):
        for p in os.listdir(self.path):
            p = os.path.join(self.path, p)
            if os.path.isfile(p):
                self._files.append(LocalFile(path=p))
            elif os.path.isdir(p):
                self._folders.append(LocalDirectory(path=p))

    def _get_all_objects(self):
        raise NotImplementedError


class LocalFile(LocalObjectMixin, BaseFile):
    """
    Class implements methods to work with S3 file
    as with local file object
    """

    def _read(self):
        if self.exists:
            with open(self.path, 'r+b') as temp_file:
                self._file = temp_file.read()
            return self._file
        return None

    def _save(self, path):
        with open(path, 'w') as tmp_file:
            tmp_file.write(self.read())
