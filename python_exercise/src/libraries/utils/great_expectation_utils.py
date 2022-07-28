import json
import os
import uuid
from pathlib import Path

import pandas as pd
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig

from libraries.conf import CONFIG_PATH
from libraries.utils.utils import Loggable, ConfLoader


class GreatExpectationConfiguration(Loggable):
    """For the configuration of Great Expectations's data context and the batch to run the expectations"""

    def __init__(self):
        super().__init__()
        with open(f'{CONFIG_PATH}/great_expectations.json', 'r') as ge_conf:
            self.conf = json.load(ge_conf)
        self.extra_params = ConfLoader.load_conf('great-expectations')
        data_context = self.init_great_expectations_data_context()
        self.context = BaseDataContext(data_context)

    def init_great_expectations_data_context(self):
        """Initializes the data context from the great_expectation.json file"""
        self.logger.info('Initializing Great Expectations Data Context')
        self._set_environ_variables()
        data_context_config = self.conf['data_context']
        ge_loaded_data_context = DataContextConfig(**data_context_config)
        return ge_loaded_data_context

    def _set_environ_variables(self):
        """Sets the environment variables in order to substitute them when loading the conf/great_expectation.json
          file"""
        os.environ['PLUGINS_DIRECTORY'] = f'{CONFIG_PATH}/plugins/'
        os.environ['CHECKPOINT_STORE'] = f'{CONFIG_PATH}/checkpoints/'
        os.environ['EXPECTATIONS_STORE'] = f'{CONFIG_PATH}/expectations/'
        os.environ['VALIDATIONS_STORE'] = (Path(self.extra_params['validations']['output'])
                                           .resolve().absolute().as_posix())
        os.environ['DOCS_LOCAL_DIR'] = Path(self.extra_params['data-docs']['output']).resolve().absolute().as_posix()
        var_names = ['PLUGINS_DIRECTORY', 'EXPECTATIONS_STORE', 'VALIDATIONS_STORE', 'CHECKPOINT_STORE',
                     'DOCS_LOCAL_DIR']
        env_variables = '\n'.join([f'{var} = {os.environ[var]}' for var in var_names])
        self.logger.info(f"Environment Variables set:\n {env_variables}")

    def run_expectations(self, file: str):
        """Runs the expectations listed in the expectations folder"""
        try:
            df = pd.read_csv(file, sep=";", header=0)
            source = self.extra_params['datasource-name']
            checkpoint = self.get_checkpoint()
            result = checkpoint.run(
                validations=[{"batch_request": {
                    "datasource_name": self.extra_params['datasource-name'],
                    "data_connector_name": "runtime_data_connector",
                    "data_asset_name": source,
                    "runtime_parameters": {"batch_data": df},
                    "batch_identifiers": {"source": source}
                }}],
                expectation_suite_name=source,
                run_name=f"validation__{file.split('/')[-1]}"
            )
            return result
        except AttributeError as e:
            self.logger.error(e)

    def get_checkpoint(self):
        source = self.extra_params['datasource-name']
        checkpoint = self.context.get_checkpoint(f"{source}_checkpoint")
        assert f"{source}_checkpoint" in self.context.list_checkpoints()
        return checkpoint

    def get_html_report_url(self, results):
        data_docs_identifier = self.extra_params['data-docs']['identifier']
        run_results_dict = None
        for k in results['run_results'].keys():
            run_results_dict = results['run_results'][k]
        actions_results = run_results_dict['actions_results']
        data_docs_url = actions_results['update_data_docs'][data_docs_identifier][7:]
        return data_docs_url
