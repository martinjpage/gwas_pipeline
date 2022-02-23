from abc import ABC, abstractmethod
import pandas as pd


class APIPrototype(ABC):

    @abstractmethod
    def search_trait_name_for_alleles(self, trait_name: str) -> None:
        """Find variant and risk alleles associated with a disease (trait) label
        :param trait_name: trait name to search"""
        pass

    @abstractmethod
    def search_trait_code_for_alleles(self, trait_code: str) -> None:
        """Find variant and risk alleles associated with a disease (trait) id
        :param trait_code: trait id to search"""
        pass

    @abstractmethod
    def create_df(self) -> pd.DataFrame:
        """Combine retrieved data and field names (column headers) into a pandas dataframe"""
        pass

    @abstractmethod
    def write_to_csv(self, filename: str) -> None:
        """Combine data and column headers and exported to CSV
        :param filename: output path for CSV"""
        pass
