import pandas as pd

from src.decorators.loggable import logger


@logger
class GWASCatalogDataExporter:
    # ToDo: add chromosome name to output; variant should be on only one chromosome - can check
    def get_unique_variants(self, data: list, column_names: list) -> list:
        df = self._create_df(data, column_names)
        unique_variant = list(df.variant.unique())
        self.logger.info(f"{len(unique_variant)} unique variants found.")
        return unique_variant

    def write_table(self, data: list, column_names: list, output_path: str) -> None:
        self.logger.info("Writing report to file")
        df = self._create_df(data, column_names)
        # ToDo: catch PermissionError for user to close CSV or auto rename if file name exists; add trait name to file
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved report to {output_path}")

    def _create_df(self, data, column_names):
        return pd.DataFrame(data=data, columns=column_names)
