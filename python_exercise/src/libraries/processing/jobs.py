import json
import shutil

import pandas as pd
import requests

from libraries.utils.great_expectation_utils import GreatExpectationConfiguration
from libraries.utils.job import Job
from libraries.utils.utils import ConfLoader


class Extractor(Job):
    """
    Class for extracting data from the public API for “Transport for The Netherlands” which provides information about
    OVAPI, country-wide public transport
    """

    def __init__(self):
        super().__init__()
        api_params = ConfLoader.load_conf('api')
        self.url = f"{api_params['base-url']}{api_params['endpoint']}"

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
        return staged_file


class Validator(Job):
    """ Class for validating data using great expectation tool (verifying conditions on columns)
    :attribute staged_file: file to validate
    """

    def __init__(self, staged_file: str):
        super().__init__()
        self.staged_file = staged_file
        self.ge_conf = GreatExpectationConfiguration()

    def run(self):
        staged_file_path = f'{self.parent_folder}/{self.staged_file}'
        result = self.ge_conf.run_expectations(staged_file_path)
        if result['success']:
            prefix_ready = self.gcs_helper.prefixes['ready']
            self.load_to_gcs(self.staged_file, prefix_ready)
        else:
            prefix_rejected = self.gcs_helper.prefixes['rejected']
            self.load_to_gcs(self.staged_file, prefix_rejected)
        return result['success']


class Cleaner(Job):
    """
    Class used for cleaning the temporary folders
    """

    def __init__(self):
        super().__init__()

    def clean_temporary_files(self):
        """
        Deletes the temporary folder with temporary files created from the python jobs
        :return:
        """
        shutil.rmtree(self.parent_folder)

    def run(self):
        self.clean_temporary_files()
