import json
import shutil

import pandas as pd
import requests
import os
from datetime import datetime as dt

from libraries.utils.gcs_utils import GCSHelper
from libraries.utils.utils import ConfLoader, Loggable


class Extractor(Loggable):
    """
    Class for extracting data from the public API for “Transport for The Netherlands” which provides information about OVAPI, country-wide public transport
    """

    def __init__(self):
        super().__init__()
        self.gcs_helper = GCSHelper()
        api_params = ConfLoader.load_conf('api')
        file_params = ConfLoader.load_conf('file')
        self.url = f"{api_params['base-url']}{api_params['endpoint']}"
        self.file_name = file_params['name']
        self.extension = file_params['extension']
        self.parent_folder = file_params['parent-folder']
        self.processing_time = dt.strftime(dt.utcnow(), '%Y%m%d')

    def extract_data_from_api(self):
        """
        Method to extract data from the public API for Transport for the Netherlands using the Per Line endpoint
        returns: dict with the list of available transportation lines  
        """
        self.logger.info(f"Fetching data from {self.url}")
        try:
            response = requests.get(self.url)
            raw_data_lines = response.json()
            response.close()
            return raw_data_lines
        except Exception as e:
            self.logger.error(e)

    def download_file_to_local(self, raw_data):
        """

        :param raw_data: response text from the API call
        :return: name of the downloaded file
        """
        self._create_temp_folder()
        output_file = f'{self.file_name}_{self.processing_time}{self.extension}'
        output_file_path = f'{self.parent_folder}/{output_file}'
        with open(output_file_path, 'w') as fp:
            json.dump(raw_data, fp)
        self.logger.info(f"Data downloaded to {output_file_path}")
        return output_file

    def load_to_gcs(self, local_file, prefix):
        """
        Loads the temporary file with API data to a Google Cloud Storage bucket and then deletes the temp folder
        :param prefix: The prefix of the blob to store in the bucket
        :param local_file: temporary file downloded from the API Call
        :return:
        """
        local_file_path = f'{self.parent_folder}/{local_file}'
        self.gcs_helper.upload_blob_to_gcs_bucket(f'{prefix}/{local_file}', local_file_path)
        #shutil.rmtree(self.parent_folder)

    def raw_data_to_staging(self, raw_data):
        """

        :param raw_data:
        :return:
        """
        self._create_temp_folder()
        output_file = f'{self.file_name}_{self.processing_time}.csv'
        output_file_path = f'{self.parent_folder}/{output_file}'
        transformed_data = [{'Line': k, **v} for k, v in raw_data.items()]
        df_transformed_data = pd.json_normalize(transformed_data)
        df_transformed_data.to_csv(output_file_path, sep=';', index=False)
        self.logger.info(f"File transformed to {output_file_path}")
        return output_file

    def run(self):
        raw_data = self.extract_data_from_api()
        local_file = self.download_file_to_local(raw_data)
        prefix_raw = self.gcs_helper.prefixes['raw']
        self.load_to_gcs(local_file, prefix_raw)
        staged_file = self.raw_data_to_staging(raw_data)
        prefix_staging = self.gcs_helper.prefixes['staging']
        self.load_to_gcs(staged_file, prefix_staging)

    def _create_temp_folder(self):
        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)


class Loader(Loggable):
    def __init__(self):
        super().__init__()


class Transformer(Loggable):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    extractor = Extractor()
    extractor.run()
