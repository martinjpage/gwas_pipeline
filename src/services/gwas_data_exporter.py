import pandas as pd

from src.domain.associations_data_exporter_prototype import AssociationsDataExporterPrototype
from src.decorators.loggable import logger


@logger
class GWASCatalogDataExporter(AssociationsDataExporterPrototype):
    # ToDo: add chromosome name to output; variant should be on only one chromosome - can check
    def get_unique_variants(self, data: list, column_names: list) -> pd.Series:
        df = self._create_df(data, column_names)
        unique_variants = df.groupby('variant').agg({'chromosome_name': ['nunique', 'unique']})
        unique_variants = self._exclude_variants_multi_chromosome(unique_variants)
        unique_variants = self._extract_listed_chromosomes(unique_variants)
        self.logger.info(f"{len(unique_variants)} unique variants found.")
        return unique_variants

    def write_table(self, data: list, column_names: list, output_path: str) -> None:
        self.logger.info("Writing report to file")
        df = self._create_df(data, column_names)
        # ToDo: catch PermissionError for user to close CSV or auto rename if file name exists; add trait name to file
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved report to {output_path}")

    def _create_df(self, data, column_names):
        return pd.DataFrame(data=data, columns=column_names)

    def _exclude_variants_multi_chromosome(self, df):
        df.columns = df.columns.get_level_values(1)
        df = df[df['nunique'] == 1]
        return df.drop('nunique', axis=1)

    def _extract_listed_chromosomes(self, df):
        return df['unique'].apply(lambda x: x[0]).rename('chromosome_name')
