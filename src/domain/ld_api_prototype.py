from abc import abstractmethod
import pandas as pd


class LDAPIPrototype:

    def __init__(self, config):
        self._config = config

    @abstractmethod
    def get_ld_score(self, ref_snp_list: list, association_snp_list: list) -> pd.DataFrame:
        pass
