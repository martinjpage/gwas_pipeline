from src.domain.associations_processor_prototype import AssociationsProcessorPrototype
from src.apis.gwas_catalog_api import GWASCatalogAPI
from src.data_processors.gwas_data_processor import GWASCatalogDataProcessor
from src.services.gwas_data_exporter import GWASCatalogDataExporter


class GWASCatalogProcessor(AssociationsProcessorPrototype):

    def __init__(self, config):
        self._config = config
        self._api = GWASCatalogAPI(config)
        self._data_processor = GWASCatalogDataProcessor(config)
        self._data_exporter = GWASCatalogDataExporter()

    def find_unique_snps(self, id_term, name_term, include_child):
        association_data = self._api.retrieve_data(id_term, name_term, include_child)
        processed_data, column_names = self._data_processor.extract_data(association_data)
        self._data_exporter.write_table(processed_data, column_names, self._config.association_out_file)
        return self._data_exporter.get_unique_snps(processed_data, column_names)
