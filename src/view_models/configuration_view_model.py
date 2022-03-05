import os
import yaml
import logging.config

from src.services.configuration import Configuration
from src.decorators.loggable import logger


@logger
class ConfigurationViewModel:

    def __init__(self, user_project_folder):
        self.user_project_folder = user_project_folder
        self._app_config_path = os.path.join("global_config", "app_config.yml")
        self._log_config_path = os.path.join("global_config", "log_config.yml")

    def application_config(self):
        config = self._get_config_file(self._app_config_path)
        self._validate_config(config)
        config["project_paths"]["project_folder"] = self._set_project_folder(config["project_paths"]["project_folder"])
        config["project_paths"]["gwas_catalog"] = os.path.join("global_config", "gwas_catalog_config.yml")
        config["project_paths"]["ld_link"] = os.path.join("global_config", "ld_link_config.yml")
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
        if 'project_paths' not in config.keys():
            raise ValueError('Config file must have an entry "project_paths"')
        if "association_file" not in config['project_paths'].keys():
            raise ValueError('Config file must have an entry "project_paths::association_file"')
        if "ld_file" not in config['project_paths'].keys():
            raise ValueError('Config file must have an entry "project_paths::ld_file"')
        if 'associations' not in config.keys():
            raise ValueError('Config file must have an entry "associations"')
        if "api" not in config['associations'].keys():
            raise ValueError('Config file must have an entry "associations::api"')
        if "p_value" not in config['associations'].keys():
            raise ValueError('Config file must have an entry "associations::p_value"')
        if 'ld' not in config.keys():
            raise ValueError('Config file must have an entry "keys"')
        if "api" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::api"')
        if "ref_pop" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::ref_pop"')

    def _set_project_folder(self, config_project_folder):
        if self.user_project_folder == "" and config_project_folder is None:
            self.logger.info("No project folder specified by user or config file. Default project folder will be created.")
            return os.path.join("default_project")
        return self.user_project_folder if self.user_project_folder != "" else config_project_folder
