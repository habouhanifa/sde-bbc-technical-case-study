from typing import List

from google.cloud import storage

from libraries.utils.utils import Loggable, ConfLoader
from libraries.conf import CONFIG_PATH


class GCSHelper(Loggable):

    def __init__(self):
        super().__init__()
        conf = ConfLoader.load_conf('gcs')
        self.bucket_name = conf['bucket-name']
        self.prefixes = conf['prefixes']
        self.storage_client = storage.Client.from_service_account_json(f'{CONFIG_PATH}/credentials.json')

    def upload_blob_to_gcs_bucket(self, blob_name: str, local_file_path: str):
        """Uploads a file to the bucket."""

        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_file_path)
        self.logger.info(f"{local_file_path} uploaded to {self.bucket_name}.")
        return blob.public_url
