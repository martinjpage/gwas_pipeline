from src.services.mtag_parser import MtagParser
from src.apis.ldmatrix_api import LDMatrixAPI
from src.data_processors.ldmatrix_data_processor import LDMatrixDataProcessor
from src.services.ldmatrix_data_exporter import LDMatrixDataExporter
from src.decorators.loggable import logger


@logger
class LDMatrixProcessor:
    def __init__(self, config):
        self._config = config
        self._mtag_parser = MtagParser()
        self._api = LDMatrixAPI(config)
        self._data_processor = LDMatrixDataProcessor(config)
        self._data_exporter = LDMatrixDataExporter(config)

    def calculate_highest_ld(self, association_snps):
        # ToDo: note - params from config file but overridden by CL input before python config created
        mtag_snps = self._mtag_parser.read_file(self._config.mtag_in_file, self._config.snp_col, self._config.chr_col)
        batch = self._data_processor.batch_by_chromosome(mtag_snps, association_snps)

        for chromosome, variants in batch.items():
            self.logger.info(f"Processing SNPs on chromosome {chromosome}.")
            ld_matrix = self._api.get_ld_score(variants['variant_mtag'], variants['variant_assoc'])
            print(ld_matrix)

        #       highest_r2 =  self._data_processor._find_highest(ref_snps, assoc_snps, ld_matrix)
        #       highest_score.append(highest_r2)
        # self._data_exporter.write_table(highest_r2)
