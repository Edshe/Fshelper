import abc
from .objectslist import FileSystemObjectsList


class BaseFileSystemObject(metaclass=abc.ABCMeta):
    """
    Abstract class for a Directory object
    """
    _parent = None
    _path = None

    @abc.abstractmethod
    def name(self):
        """
        Method returns a name of an object
        """
        return

    @abc.abstractmethod
    def exists(self) -> bool:
        """
        Method returns True if object exists of False
        """
        return False

    @abc.abstractmethod
    def parent(self):
        """
        Method returns a parent directory
        """
        return

    @property
    def path(self) -> str:
        """
        Method returns current path
        of directory or file
        """
        return self._path or '/'


class BaseDirectory(BaseFileSystemObject):
    """
    Abstract class for a Directory object
    """
    def __init__(self, path: str = '', parent=None):
        if path.endswith('/'):
            self._path = path
        else:
            self._path = '{}/'.format(path)

        self._parent = parent

        self._files = FileSystemObjectsList()  # list of files, empty until ls() called
        self._folders = FileSystemObjectsList()  # list of folders, empty until ls() called
        self.cached = False

    def __repr__(self):
        return 'Directory: {}'.format(self.path or '/')

    def __str__(self):
        return self.path

    def ls(self) -> dict:
        """
        Method returns list of files
        and folders for current directory
        """
        if not self.cached:
            self._get_objects()
            self.cached = True

        return dict(
            files=self._files,
            folders=self._folders
        )

    def ls_files(self) -> list:
        return self.ls().get('files')

    def ls_folders(self) -> list:
        return self.ls().get('folders')

    def cache_all(self):
        """
        Recursively walks in subfolders and
        returns lists for all objects.
        """
        self._get_all_objects()
        self.cached = True

    def cd(self, path: str):
        """
        Method returns a new child directory
        of specified path
        """
        return self._get_child_directory(path)

    def find(self, mask: str = None):
        """
        Method returns a dict with files and folders
        matched with mask.
        Method searches only in current folder.
        Example of usage:
            find(mask='*.jpg')
        """
        if '*' in mask:
            mask = mask.replace('*', '')
            name_filter = lambda x: mask in x if x else False
        else:
            name_filter = lambda x: mask == x if x else False

        return dict(
            files=[file for file in self.ls()['files'] if name_filter(file.name)],
            folders=[folder for folder in self.ls()['files'] if name_filter(folder.name)]
        )

    def find_all(self, mask: str = None):
        """
        Method recursively searches in current folder and
        subfolders and returns a dict with files
        and folders matched with mask.
        Example of usage:
            find(mask='*.jpg')
        """
        all_files = []
        all_folders = []
        for folder in self.ls()['folders']:
            result = folder.find_all(mask=mask)
            all_files.extend(result.get('files'))
            all_folders.extend(result.get('files'))

        result = self.find(mask=mask)
        all_files.extend(result.get('files'))
        all_folders.extend(result.get('folders'))
        return dict(
            files=all_files,
            folders=all_folders
        )

    def save(self, path: str = None):
        """
        Method recursively saves all files
        in current folder and subfolders
        """
        path = (path or self.path).strip('/')
        for folder in self.ls_folders():
            folder_path = '{}/{}'.format(path, folder.name)
            folder.save(path=folder_path)
        for file in self.ls_files():
            file.save(path='{}/{}'.format(path, file.name))

    def convert(self, to: str, path: str):
        """
        Method return new directory of specified type
        with all folders and files that contains current directory
        :param to: str - type of directory
        :param path: str - new path
        """
        if to == 'cloud':
            from .cloud import CloudDirectory, CloudFile
            directory_class = CloudDirectory
            file_class = CloudFile
        elif to == 'local':
            from .local import LocalDirectory, LocalFile
            directory_class = LocalDirectory
            file_class = LocalFile
        else:
            raise Exception("Invalid parameter value (to: {})".format(to))
        return self._convert(directory_class, file_class, path)

    @abc.abstractmethod
    def _get_child_directory(self, path):
        return

    @abc.abstractmethod
    def _get_objects(self):
        return

    @abc.abstractmethod
    def _get_all_objects(self):
        return

    def _convert(self, directory_class, file_class, path):
        path = path.strip('/')

        folder = directory_class(path=path)

        for f in self.ls_folders():
            folder_path = '{}/{}'.format(path, f.name)
            new_folder = f._convert(directory_class, file_class, folder_path)
            folder._folders.append(new_folder)

        for file in self.ls_files():
            new_file = file_class(path='{}/{}'.format(path, file.name))
            new_file._file = file.read()
            folder._files.append(new_file)

        return folder

class BaseFile(BaseFileSystemObject):
    """
    Base class for a File object
    """

    def __init__(self, path: str = '', parent=None):
        self._path = path
        self._parent = parent

    def __repr__(self):
        return 'File: {}'.format(self.path)

    def __str__(self):
        return self.path

    def save(self, path: str = None):
        """
        Method saves a file content
        If path specified - file will be
        saved in new path
        """
        return self._save(path or self.path)

    def read(self):
        """
        Method reads a file contents
        """
        return self._read()

    @abc.abstractmethod
    def _read(self):
        return

    @abc.abstractmethod
    def _save(self, path):
        return
