from collections import namedtuple
import yaml

from src.decorators.loggable import logger
from src.domain.enums.api_type import APIType


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

        self.api = self._config["api"]
        self.url = self._config["urls"][self.api.lower()]
        key = self._get_config_file(self._config["keys"][self.api])
        self.key = self._convert(key)

        if validate:
            self._verify_configuration()

    def _convert(self, dictionary):
        return namedtuple('configuration', dictionary.keys())(**dictionary)

    def _verify_configuration(self):
        if self.api.lower() not in APIType.valid_apis():
            message = f"{self.api} is not a valid database source. Please select from {APIType.valid_apis()}."
            self.logger.error(message)
            raise ValueError(message)

    def _get_config_file(self, config_file):
        try:
            with open(config_file) as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {config_file}. Please specify valid catalogue configuration.")
        return config
