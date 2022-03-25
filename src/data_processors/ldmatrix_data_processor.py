import pandas as pd
import numpy as np

from src.domain.ld_data_processor_prototype import LDDataProcessorPrototype


class LDMatrixDataProcessor(LDDataProcessorPrototype):

    def batch_by_chromosome(self, mtag_snps: pd.DataFrame, association_snps: pd.DataFrame):
        grouped_mtag_snps = self._groupby_chromosome(mtag_snps)
        grouped_association_snps = self._groupby_chromosome(association_snps)
        merged_snps = self._merge_snps(grouped_mtag_snps, grouped_association_snps)
        return self._convert_to_dict(merged_snps)

    def find_novel_snps(self, mtag_variants, assoc_variants):
        duplicated = np.isin(np.array(mtag_variants), np.array(assoc_variants))
        novel_mtag = mtag_variants[~duplicated]
        duplicated_mtag = mtag_variants[duplicated]
        return list(novel_mtag), list(duplicated_mtag)

    def find_correlated_snps(self, chromosome, ld_matrix, mtag_variants, assoc_variants):
        ld_matrix = self._filter_matrix(ld_matrix, mtag_variants, assoc_variants)
        highest_correlation = ld_matrix.max(axis="columns")

        correlated_snps = []
        for mtag_variant, highest_r in highest_correlation.items():
            assoc_snps = self._find_highest_correlation(ld_matrix, mtag_variant, highest_r)
            correlated_snps.append([mtag_variant, assoc_snps, highest_r, chromosome])
        return correlated_snps

    def _groupby_chromosome(self, df):
        return df.groupby(level=0).agg(list)

    def _merge_snps(self, grouped_mtag_snps, grouped_association_snps):
        return grouped_mtag_snps.join(grouped_association_snps, how='left', lsuffix='_mtag', rsuffix='_assoc')

    def _convert_to_dict(self, merged_df):
        return merged_df.T.to_dict()

    def _filter_matrix(self, ld_matrix, mtag_variants, assoc_variants):
        row_filter = ld_matrix.index.isin(mtag_variants)
        col_filter = ld_matrix.columns.isin(assoc_variants)
        return ld_matrix.loc[row_filter, col_filter]

    def _find_highest_correlation(self, ld_matrix, variant, highest_r):
        return ", ".join(list(ld_matrix.columns[ld_matrix.loc[variant, :].values == highest_r]))
