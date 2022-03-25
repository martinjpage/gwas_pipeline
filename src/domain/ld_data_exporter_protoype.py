from abc import abstractmethod


class LDDataExporterPrototype:
    @abstractmethod
    def write_table(self, data, column_names, output_path):
        pass
