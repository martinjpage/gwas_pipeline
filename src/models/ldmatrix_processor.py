from src.services.mtag_parser import MtagParser
from src.apis.ldmatrix_api import LDMatrixAPI
from src.data_processors.ldmatrix_data_processor import LDMatrixDataProcessor
from src.services.ldmatrix_data_exporter import LDMatrixDataExporter


class LDMatrixProcessor:
    def __init__(self, config):
        self._config = config
        self._mtag_parser = MtagParser()
        self._api = LDMatrixAPI(config)
        self._data_processor = LDMatrixDataProcessor(config)
        self._data_exporter = LDMatrixDataExporter(config)

    def calculate_ld(self, association_variants):
        pass