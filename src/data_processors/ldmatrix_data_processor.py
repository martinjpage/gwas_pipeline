import pandas as pd

from src.domain.ld_data_processor_prototype import LDDataProcessorPrototype


class LDMatrixDataProcessor(LDDataProcessorPrototype):

    def batch_by_chromosome(self, mtag_snps: pd.DataFrame, association_snps: pd.DataFrame):
        grouped_mtag_snps = self._groupby_chromosome(mtag_snps)
        grouped_association_snps = self._groupby_chromosome(association_snps)
        merged_snps = self._merge_snps(grouped_mtag_snps, grouped_association_snps)
        return self._convert_to_dict(merged_snps)

    def find_highest(self):
        pass

    def _groupby_chromosome(self, df):
        return df.groupby(level=0).agg(list)

    def _merge_snps(self, grouped_mtag_snps, grouped_association_snps):
        return grouped_mtag_snps.join(grouped_association_snps, how='left', lsuffix='_mtag', rsuffix='_assoc')

    def _convert_to_dict(self, merged_df):
        return merged_df.T.to_dict()
