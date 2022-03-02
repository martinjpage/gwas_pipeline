from src.decorators.loggable import logger
from src.domain.enums.api_type import APIType
from src.apis.gwas_catalog_api import GWASCatalogCatalogAPI
from src.data_processors.gwas_data_processor import GWASCatalogDataProcessor
from src.services.csv_report_writer import CSVReportWriter


@logger
class Pipeline:

    def __init__(self, config):
        self._config = config
        self._configure_pipeline()

    def _configure_pipeline(self):
        if self._config.api.lower() == APIType.gwas_catalog.value.lower():
            self._api = GWASCatalogCatalogAPI(self._config.url, self._config.key)
            self._data_processor = GWASCatalogDataProcessor(self._config.key)
            self._data_exporter = CSVReportWriter()

    def run(self, id_term, name_term, output_path):
        raw_data = self._api.retrieve_data(id_term, name_term)
        processed_data, column_names = self._data_processor.extract_data(raw_data)
        self._data_exporter.write(processed_data, column_names, output_path)
