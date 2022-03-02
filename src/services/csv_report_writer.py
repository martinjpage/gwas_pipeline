import pandas as pd

from src.decorators.loggable import logger


@logger
class CSVReportWriter:
    def write(self, data, column_names, output_path) -> None:
        self.logger.info("Writing report to file")
        df = pd.DataFrame(data=data, columns=column_names)
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved report to {output_path}")
