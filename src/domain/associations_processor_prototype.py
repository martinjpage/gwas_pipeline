from abc import abstractmethod


class AssociationsProcessorPrototype:

    @abstractmethod
    def find_unique_snps(self, id_term, name_term, include_child):
        pass
