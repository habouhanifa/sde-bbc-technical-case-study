import os
import shutil

from libraries.utils.gcs_utils import GCSHelper
from libraries.utils.utils import Loggable, ConfLoader
from abc import ABC, abstractmethod
from datetime import datetime as dt


class Job(Loggable, ABC):
    """
    Generic class representing a job that would be run on Airflow as a Python task
    """

    def __init__(self):
        super().__init__()
        self.gcs_helper = GCSHelper()
        file_params = ConfLoader.load_conf('file')
        self.file_name = file_params['name']
        self.extension = file_params['extension']
        self.parent_folder = file_params['parent-folder']
        self.processing_time = dt.strftime(dt.utcnow(), '%Y%m%d')

    @abstractmethod
    def run(self):
        """
        method called to run the job on Airflow (to be wrapped inside a python callable)
        :return:
        """

    def load_to_gcs(self, local_file, prefix):
        """
        Loads the temporary file with API data to a Google Cloud Storage bucket and then deletes the temp folder
        :param prefix: The prefix of the blob to store in the bucket
        :param local_file: temporary file downloded from the API Call
        :return:
        """
        local_file_path = f'{self.parent_folder}/{local_file}'
        self.gcs_helper.upload_blob_to_gcs_bucket(f'{prefix}/{local_file}', local_file_path)

    def _create_temp_folder(self):
        """
        Create a temporary folder used for storing the temporary files containing data from the API
        :return:
        """
        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)

