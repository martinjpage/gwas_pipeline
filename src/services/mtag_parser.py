import pandas as pd


class MtagParser:

    def read_file(self, filename: str, variant_column: str, chromosome_column: str) -> pd.DataFrame:
        # ToDo: confirm tab-delimited format
        df = pd.read_csv(filename, sep='\t')
        # ToDo: error catching for column names; validation of snp names and chromosome names (esp X chromosome)
        #  check one chromosome per variant
        df = df[[chromosome_column, variant_column]]
        df.columns = ['chromosome_name', 'variant']
        return df.set_index('chromosome_name')
