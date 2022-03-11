from abc import abstractmethod
import pandas as pd

class LDAPI:

    def __init__(self, config):
        self._config = config

    @abstractmethod
    def get_ld_score(self, ref_snp: str, snp_list: list) -> pd.DataFrame:
        pass
