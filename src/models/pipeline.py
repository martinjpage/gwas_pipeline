from src.decorators.loggable import logger
from src.domain.enums.associations_api_type import AssociationsAPIType
from src.domain.enums.ld_api_type import LDAPIType
from src.apis.gwas_catalog_api import GWASCatalogCatalogAPI
from src.data_processors.gwas_data_processor import GWASCatalogDataProcessor
from src.services.gwas_data_exporter import GWASCatalogDataExporter


@logger
class Pipeline:

    def __init__(self, config):
        self._config = config
        self._configure_pipeline()

    def _configure_pipeline(self):


        if self._config.associations.api.lower() == AssociationsAPIType.gwas_catalog.value.lower():
            self._association_api = GWASCatalogCatalogAPI(self._config.associations)
            self._association_data_processor = GWASCatalogDataProcessor(self._config.associations)
            self._association_data_exporter = GWASCatalogDataExporter()

        if self._config.ld.api.lower() == LDAPIType.ld_link.value.lower():
            self._ld_api = None
            self._ld_data_processor = None

    def run(self, id_term, name_term):
        raw_data = self._association_api.retrieve_data(id_term, name_term)
        processed_data, column_names = self._association_data_processor.extract_data(raw_data)
        unique_variants = self._association_data_exporter.get_unique_variants(processed_data, column_names)
        # ToDo: LD calculations
        self._association_data_exporter.write_table(processed_data, column_names,
                                                    self._config.project_paths.association_out_file)
