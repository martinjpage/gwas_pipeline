from abc import abstractmethod


class AssociationsProcessorPrototype:

    @abstractmethod
    def find_unique_associations(self, id_term, name_term):
        pass
