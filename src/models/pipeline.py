from src.decorators.loggable import logger



@logger
class Pipeline:

    def __init__(self, config, association_processor, ld_processor):
        # ToDo GWASProc, LDProc - logic to run processor is in order and pass data around
        self._config = config
        self._association_processor = association_processor
        self._ld_processor = ld_processor

    def run(self, id_term, name_term):
        unique_association_variants = self._association_processor.find_unique_associations(id_term, name_term)
        self._ld_processor.calculate_ld(unique_association_variants)
