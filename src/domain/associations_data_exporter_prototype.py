from abc import abstractmethod


class AssociationsDataExporterPrototype:
    @abstractmethod
    def get_unique_variants(self, data, column_names):
        pass

    @abstractmethod
    def write_table(self, data, column_names, output_path):
        pass
