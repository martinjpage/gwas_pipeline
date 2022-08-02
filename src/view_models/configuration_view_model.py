import os
import yaml
import logging.config

from src.services.configuration import Configuration
from src.decorators.loggable import logger


@logger
class ConfigurationViewModel:

    def __init__(self, user_project_folder):
        self._user_project_folder = user_project_folder
        self._project_folder = None
        self._app_config_path = os.path.join("global_config", "app_config.yml")
        self._log_config_path = os.path.join("global_config", "log_config.yml")
        self._configurator = Configuration()

    def associations_config(self):
        config_params = self._get_config_file(self._app_config_path)
        self._validate_associations_config(config_params)
        project_folder = self._get_project_folder(config_params["project_folder"])
        associations = config_params["associations"]
        associations["association_out_file"] = self._create_full_path(project_folder,
                                                                      associations["association_out_file"])
        associations['sig_p_value'] = self._convert_scientific_to_float(associations['sig_p_value'])

        association_configs = {"gwas_catalog": os.path.join("global_config", "gwas_catalog_config.yml")}

        return self._configurator.create_associations_config(config_params["associations"], association_configs)

    def ld_config(self):
        config_params = self._get_config_file(self._app_config_path)
        self._validate_ld_config(config_params)
        project_folder = self._get_project_folder(config_params["project_folder"])
        config_params["ld"]["mtag_in_file"] = self._create_full_path(project_folder, config_params["ld"]["mtag_in_file"])
        config_params["ld"]["ld_out_file"] = self._create_full_path(project_folder, config_params["ld"]["ld_out_file"])

        ld_configs = {"ld_matrix": os.path.join("global_config", "ld_matrix_config.yml")}
        return self._configurator.create_ld_config(config_params["ld"], ld_configs)

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

    def _validate_associations_config(self, config):
        if 'project_folder' not in config.keys():
            raise ValueError('Config file must have an entry "project_folder"')
        if 'associations' not in config.keys():
            raise ValueError('Config file must have an entry "associations"')
        if "api" not in config['associations'].keys():
            raise ValueError('Config file must have an entry "associations::api"')
        if "sig_p_value" not in config['associations'].keys():
            raise ValueError('Config file must have an entry "associations::p_value"')
        if "association_out_file" not in config['associations'].keys():
            raise ValueError('Config file must have an entry "associations::association_out_file"')

    def _validate_ld_config(self, config):
        if 'project_folder' not in config.keys():
            raise ValueError('Config file must have an entry "project_folder"')
        if 'ld' not in config.keys():
            raise ValueError('Config file must have an entry "ld"')
        if "api" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::api"')
        if "ref_pop" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::ref_pop"')
        if "genome_build" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::genome_build"')
        if "score" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::score"')
        if "mtag_in_file" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::mtag_in_file"')
        if "snp_col" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::snp_col"')
        if "chr_col" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::chr_col"')
        if "ld_out_file" not in config['ld'].keys():
            raise ValueError('Config file must have an entry "ld::ld_out_file"')

    def _get_project_folder(self, config_project_folder):
        # ToDo: check if folder exits otherwise create it
        if self._project_folder_is_set():
            return self._project_folder
        if self._no_user_or_config_project(config_project_folder):
            self.logger.info(
                "No project folder specified by user or config file. Default project folder will be created.")
            self._project_folder = os.path.join("default_project")
        else:
            self._project_folder = self._project_folder_preference(config_project_folder)
        return self._project_folder

    def _project_folder_is_set(self):
        return self._project_folder is not None

    def _no_user_or_config_project(self, config_project_folder):
        return self._user_project_folder == "" and \
               config_project_folder is None or \
               config_project_folder == 'None' or \
               config_project_folder == ""

    def _project_folder_preference(self, config_project_folder):
        if self._user_project_folder != "":
            self.logger.info(f"A project folder was supplied in the command line execution. Using user-provided project "
                             f"folder: {self._user_project_folder}.")
            return self._user_project_folder
        self.logger.info(f"No project folder was supplied in the command line execution. Using project folder from app"
                         f"config: {config_project_folder}.")
        return config_project_folder

    def _create_full_path(self, project_folder, file_name):
        return os.path.join(project_folder, file_name)

    def _convert_scientific_to_float(self, value):
        if isinstance(value, float):
            return value
        if value is None or value == 'None' or value == '':
            raise ValueError(f'Cannot convert {value} to a float. Check p_value in config file.')
        return float(value)
