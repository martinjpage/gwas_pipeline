import time

from src.decorators.loggable import logger


@logger
class Pipeline:

    def __init__(self, association_processor, ld_processor):
        self._association_processor = association_processor
        self._ld_processor = ld_processor

    def run(self, id_term, name_term, include_child):
        association_start = time.time()
        association_snps = self._association_processor.find_unique_snps(id_term, name_term, include_child)
        association_duration = time.time() - association_start
        self.logger.info(f"Successfully run association processor in {association_duration:0.3f}s")
        ls_start = time.time()
        self._ld_processor.calculate_highest_ld(association_snps)
        ld_duration = time.time() - ls_start
        self.logger.info(f"Successfully run ld processor in {ld_duration:0.3f}s")
