from abc import abstractmethod


class AssociationsAPIPrototype:

    def __init__(self, config):
        self._config = config

    def retrieve_data(self, id_term, name_term, include_child):
        if id_term is None:
            return self._search_trait_name_for_alleles(name_term, include_child)
        else:
            return self._search_trait_code_for_alleles(id_term, include_child)

    @abstractmethod
    def _search_trait_name_for_alleles(self, trait_name: str, include_child: bool) -> None:
        """Find variant and risk alleles associated with a disease (trait) label
        :param trait_name: trait name to search"""
        pass

    @abstractmethod
    def _search_trait_code_for_alleles(self, trait_code: str, include_child: bool) -> None:
        """Find variant and risk alleles associated with a disease (trait) id
        :param trait_code: trait id to search"""
        pass
