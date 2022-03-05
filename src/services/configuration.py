import os.path
from collections import namedtuple
import yaml

from src.decorators.loggable import logger
from src.domain.enums.associations_api_type import AssociationsAPIType
from src.domain.enums.ld_api_type import LDAPIType


@logger
class Configuration:

    def __init__(self, config_file=None, config=None, validate=True):

        if config_file is not None:
            with open(config_file) as in_file:
                self._config = yaml.load(in_file, Loader=yaml.FullLoader)
        elif config is not None:
            self._config = config
        else:
            raise ValueError("Could not create configuration. Must pass either location of config file or valid config.")

        self.project_folder = self._config["project_paths"]["project_folder"]
        self.project_paths = self._convert(self._config["project_paths"])
        associations = self._config["associations"]
        associations_keys = self._get_config_file(self._config["project_paths"][associations['api']])
        self.associations = self._convert(associations | associations_keys)
        ld = self._config["ld"]
        ld_key = self._get_config_file(self._config["project_paths"][ld['api']])
        self.ld = self._convert(ld | ld_key)

        if validate:
            self._verify_configuration()

    def _convert(self, dictionary):
        return namedtuple('configuration', dictionary.keys())(**dictionary)

    def _verify_configuration(self):
        if self.associations.api.lower() not in AssociationsAPIType.valid_apis():
            message = f"{self.associations.api} is not a valid database source. Please select " \
                      f"from {AssociationsAPIType.valid_apis()}."
            self.logger.error(message)
            raise ValueError(message)

        if self.ld.api.lower() not in LDAPIType.valid_apis():
            message = f"{self.ld.api} is not a valid database source. Please select " \
                      f"from {LDAPIType.valid_apis()}."
            self.logger.error(message)
            raise ValueError(message)

    def _get_config_file(self, config_file):
        try:
            with open(config_file) as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {config_file}. Please specify valid catalogue configuration.")
        return config
