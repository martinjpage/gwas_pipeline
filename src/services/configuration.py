import yaml
from collections import namedtuple

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
        associations['sig_p_value'] = self._convert_scientific_to_float(associations['sig_p_value'])
        associations_keys = self._get_config_file(self._config["project_paths"][associations['api']])
        self.associations = self._convert(associations | associations_keys)
        ld = self._config["ld"]
        ld_key = self._get_config_file(self._config["project_paths"][ld['api']])
        self.ld = self._convert(ld | ld_key)

        if validate:
            self._verify_configuration()

    def _convert(self, dictionary):
        return namedtuple('configuration', dictionary.keys())(**dictionary)

    def _convert_scientific_to_float(self, value):
        if isinstance(value, float):
            return value
        if value is None or value == 'None' or value == '':
            raise ValueError(f'Cannot convert {value} to a float. Check p_value in config file.')
        return float(value)

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
                loader = yaml.FullLoader
                config = yaml.load(file, Loader=loader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {config_file}. Please specify valid catalogue configuration.")
        return config
