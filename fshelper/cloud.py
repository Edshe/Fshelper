import os
import tempfile
import boto3
import botocore
import ibm_boto3
from ibm_botocore.client import Config

from .base import BaseDirectory, BaseFile


class CloudObjectMixin:

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str,
                 use_accelerate_endpoint: str, endpoint_url: str = '', cloud='aws',
                 bucket: str = None, **kwargs):

        self.bucket = bucket

        params = dict(
            service_name='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(
                s3={'use_accelerate_endpoint': use_accelerate_endpoint}
            ),
            endpoint_url=endpoint_url
        )
        if cloud == 'aws':
            self._cloud = ibm_boto3.client(params)
        elif cloud == 'ibm':
            self._cloud = boto3.client(params)
        else:
            raise Exception("Unknown cloud type")

        super().__init__(**kwargs)

    @property
    def exists(self) -> bool:
        try:
            if self.path.endswith('/'):
                if len(self._cloud.list_objects_v2(Bucket=self.bucket, Prefix=self.path)) > 0:
                    return True
            else:
                self._cloud.head_object(Bucket=self.bucket, Key=self.path)
                return True
        except Exception as e:
            return False

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


class CloudDirectory(CloudObjectMixin, BaseDirectory):
    """
    Class implements methods to work with Cloud directory
    as with local directory
    """

    def _get_child_directory(self, path):
        """
        Method returns a new CloudDirectory
        object for specified Cloud path
        """
        if not path.endswith('/'):
            path = '{}/'.format(path)

        return CloudDirectory(
            parent=self,
            path=path
        )

    def _get_objects(self):
        paginator = self._cloud.get_paginator('list_objects')
        for page in paginator.paginate(Bucket=self.bucket, Prefix=self.path, Delimiter='/'):
            if page.get('Contents'):
                for content in page.get('Contents'):
                    self._files.append(CloudFile(path=content['Key'], parent=self))
            if page.get('CommonPrefixes'):
                for prefix in page.get('CommonPrefixes'):
                    self._folders.append(CloudDirectory(path=prefix['Prefix'], parent=self))

    def _get_all_objects(self):
        """
        Recommended if many folders
        """
        self._files = []
        self._folders = []
        paginator = self._cloud.get_paginator('list_objects')
        for page in paginator.paginate(Bucket=self.bucket, Prefix=self.path):
            if page.get('Contents'):
                for content in page.get('Contents'):
                    self._files.append(CloudFile(path=content['Key'], parent=self))
        self._sort_files()

    def _sort_files(self):
        i = 0
        while self._files:
            if i >= len(self._files):
                break
            file = self._files[i]
            splited_path = file.path.replace(self.path, '').strip('/').split('/')
            if len(splited_path) == 1:
                i += 1
                continue

            folder_name = splited_path[0]
            if self.parent and folder_name == self.parent.name:
                i += 1
                continue

            folder = self._get_folder_by_name(folder_name)

            if folder is None:
                folder = CloudDirectory(path=self.path+folder_name, parent=self)
                self._folders.append(folder)

            folder._files.append(file)
            self._files.pop(i)

        for folder in self._folders:
            folder._sort_files()

    def _get_folder_by_name(self, name):
        for f in self._folders:
            if f.name == name:
                return f
        return None


class CloudFile(CloudObjectMixin, BaseFile):
    """
    Class implements methods to work with Cloud file
    as with local file object
    """

    def _read(self):
        if not hasattr(self, '_file'):
            with tempfile.TemporaryDirectory() as temp_dir:
                tmp_file = os.path.join(temp_dir, 'tmp')
                self.bucket.download_file(self.path, tmp_file)
                with open(tmp_file, 'r+b') as f:
                    self._file = f.read()
        return self._file

    def _save(self, key: str):
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(self.read())
            tmp_file.flush()
            tmp_file.seek(0)
            self.bucket.upload_file(
                filename=tmp_file.name,
                key=key or self.path
            )
