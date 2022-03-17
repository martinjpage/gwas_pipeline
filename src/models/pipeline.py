from src.decorators.loggable import logger


@logger
class Pipeline:

    def __init__(self, association_processor, ld_processor):
        # ToDo GWASProc, LDProc - logic to run processor is in order and pass data around
        self._association_processor = association_processor
        self._ld_processor = ld_processor

    def run(self, id_term, name_term):
        association_snps = self._association_processor.find_unique_snps(id_term, name_term)
        self._ld_processor.calculate_highest_ld(association_snps)
