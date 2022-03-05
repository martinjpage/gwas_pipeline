from src.decorators.loggable import logger
from src.domain.enums.associations_api_type import AssociationsAPIType
from src.domain.enums.ld_api_type import LDAPIType
from src.apis.gwas_catalog_api import GWASCatalogCatalogAPI
from src.data_processors.gwas_data_processor import GWASCatalogDataProcessor
from src.services.csv_report_writer import CSVReportWriter


@logger
class Pipeline:

    def __init__(self, config):
        self._config = config
        self._configure_pipeline()

    def _configure_pipeline(self):
        self._data_exporter = CSVReportWriter()

        if self._config.associations.api.lower() == AssociationsAPIType.gwas_catalog.value.lower():
            self._association_api = GWASCatalogCatalogAPI(self._config.associations)
            self._association_data_processor = GWASCatalogDataProcessor(self._config.associations)

        if self._config.ld.api.lower() == LDAPIType.ld_link.value.lower():
            self._ld_api = None
            self._ld_data_processor = None

    def run(self, id_term, name_term):
        raw_data = self._association_api.retrieve_data(id_term, name_term)
        processed_data, column_names = self._association_data_processor.extract_data(raw_data)
        self._data_exporter.write(processed_data, column_names, self._config.project_paths.association_out_file)
