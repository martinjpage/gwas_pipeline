from abc import abstractmethod


class LDDataProcessorPrototype:
    def __init__(self, config):
        self._config = config
        self._ld_columns = ['mtag_snp', 'high_assoc_snp', 'r_2', 'chromosome']

    def ld_columns(self):
        return self._ld_columns
