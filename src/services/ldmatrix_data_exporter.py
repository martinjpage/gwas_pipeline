import pandas as pd

from src.domain.ld_data_exporter_protoype import LDDataExporterPrototype
from src.decorators.loggable import logger


@logger
class LDMatrixDataExporter(LDDataExporterPrototype):

    def write_table(self, data: list, column_names: list, output_path: str):
        self.logger.info("Writing ld matrix to file")
        df = self._create_df(data, column_names)
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved ld matrix to {output_path}")

    def _create_df(self, data, column_names) -> pd.DataFrame:
        return pd.DataFrame(data=data, columns=column_names)
