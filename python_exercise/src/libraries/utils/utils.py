import logging

import yaml

from libraries.conf import CONFIG_PATH


class ConfLoader:

    @classmethod
    def load_conf(cls, key=None):
        with open(f'{CONFIG_PATH}/project_params.yml', 'r') as yaml_conf:
            conf = yaml.load(yaml_conf, Loader=yaml.FullLoader)
        return conf if key is None else conf[key]


class CustomLogger:

    def __init__(self, name=None):
        super().__init__()
        conf = ConfLoader.load_conf(key='logging')
        self.logger = logging.getLogger(conf['name'] if name is None else name)
        self.logger.propagate = False
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.setLevel(conf['level'])


class Loggable:
    def __init__(self):
        super().__init__()
        self.logger = CustomLogger(name=self.__class__.__name__).logger


