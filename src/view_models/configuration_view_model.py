import os
import yaml
import logging.config

from src.services.configuration import Configuration


class ConfigurationViewModel:

    def __init__(self):
        self._app_config_path = os.path.join("global_config", "app_config.yml")
        self._log_config_path = os.path.join("global_config", "log_config.yml")

    def application_config(self):
        config = self._get_config_file(self._app_config_path)
        self._validate_config(config)
        config["keys"]["gwas_catalog"] = os.path.join("global_config", "gwas_catalog_config.yml")
        return Configuration(config=config)

    def logger_config(self):
        config = self._get_config_file(self._log_config_path)
        logging.config.dictConfig(config)
        logger = logging.getLogger("gwas_pipeline")
        return logger

    def _get_config_file(self, config_file):
        try:
            with open(config_file) as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {config_file}. Please specify valid application configuration")
        return config

    def _validate_config(self, config):
        if 'api' not in config.keys():
            raise ValueError('Config file must have an entry "api"')
        if 'urls' not in config.keys():
            raise ValueError('Config file must have an entry "urls"')
        if 'keys' not in config.keys():
            raise ValueError('Config file must have an entry "keys"')
