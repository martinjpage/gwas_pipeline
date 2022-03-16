import yaml
from collections import namedtuple

from src.decorators.loggable import logger
from src.domain.enums.associations_api_type import AssociationsAPIType
from src.domain.enums.ld_api_type import LDAPIType


@logger
class Configuration:

    def create_associations_config(self, associations_params, configs_paths):
        self._verify_association_configuration(associations_params)
        return self._create_config(associations_params, configs_paths)

    def create_ld_config(self, ld_parameters, configs_paths):
        self._verify_ld_configuration(ld_parameters)
        return self._create_config(ld_parameters, configs_paths)

    def _create_config(self, parameters, configs_paths):
        config_file = self._select_config(parameters['api'], configs_paths)
        keys = self._get_config_file(config_file)
        return self._convert(parameters | keys)

    def _verify_association_configuration(self, associations_params):
        if associations_params["api"].lower() not in AssociationsAPIType.valid_apis():
            message = f"{associations_params['api']} is not a valid database source. Please select from " \
                      f"{AssociationsAPIType.valid_apis()}."
            self.logger.error(message)
            raise ValueError(message)

        if not isinstance(associations_params["sig_p_value"], float) and \
                not isinstance(associations_params["sig_p_value"], int):
            message = f"{associations_params['sig_p_value']} is not parsed as a number. Please ensure the sig_p_value" \
                      f"for genome-wide significance for associations is numeric."
            self.logger.error(message)
            raise ValueError(message)

    def _verify_ld_configuration(self, ld_parameters):
        if ld_parameters["api"].lower() not in LDAPIType.valid_apis():
            message = f"{ld_parameters['api']} is not a valid database source. Please select from " \
                      f"{LDAPIType.valid_apis()}."
            self.logger.error(message)
            raise ValueError(message)
        # ToDo: check ref_pop, genome_build and score params for the selected LD API

    def _select_config(self, api_name, configs_paths):
        return configs_paths[api_name]

    def _get_config_file(self, config_file):
        try:
            with open(config_file) as file:
                loader = yaml.FullLoader
                config = yaml.load(file, Loader=loader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {config_file}. Please specify valid catalogue configuration.")
        return config

    def _convert(self, dictionary):
        return namedtuple('configuration', dictionary.keys())(**dictionary)
