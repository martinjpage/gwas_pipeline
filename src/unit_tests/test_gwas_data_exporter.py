import pandas as pd

from src.services.gwas_data_exporter import GWASCatalogDataExporter


class TestGWASCatalogDataExporter:
    def setup(self):
        df = pd.read_csv('associations.csv')
        self._column_names = df.columns
        self._data = df.values.tolist()

    def test_get_unique_variants(self):
        exporter = GWASCatalogDataExporter()
        unique_variants = exporter.get_unique_variants(self._data, self._column_names)
        print(unique_variants)