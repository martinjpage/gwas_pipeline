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
        novel_mtags = list(set(mtag_variants).difference(set(assoc_variants)))
        known_mtags = list(set(mtag_variants).intersection(set(assoc_variants)))

        correlated_snps = []
        self._add_known_mtags(correlated_snps, known_mtags, chromosome)
        ld_matrix = self._filter_matrix(ld_matrix, novel_mtags, assoc_variants)
        self._add_novel_mtags(correlated_snps, ld_matrix, chromosome)
        return correlated_snps

    def _groupby_chromosome(self, df):
        return df.groupby(level=0).agg(list)

    def _merge_snps(self, grouped_mtag_snps, grouped_association_snps):
        grouped_mtag_snps.index = grouped_mtag_snps.index.map(str)
        grouped_association_snps.index = grouped_association_snps.index.map(str)
        merged_df = grouped_mtag_snps.join(grouped_association_snps, how='left', lsuffix='_mtag', rsuffix='_assoc')
        merged_df.variant_assoc = merged_df['variant_assoc'].apply(lambda x: x if isinstance(x, list) else [])
        return merged_df

    def _convert_to_dict(self, merged_df):
        return merged_df.T.to_dict()

    def _add_known_mtags(self, correlated_snps, known_mtags, chromosome):
        if len(known_mtags) == 0:
            return correlated_snps
        for snp in known_mtags:
            correlated_snps.append([snp, snp, 1.0, chromosome])

    def _filter_matrix(self, ld_matrix, mtag_variants, assoc_variants):
        row_filter = ld_matrix.index.isin(mtag_variants)
        col_filter = ld_matrix.columns.isin(assoc_variants)
        return ld_matrix.loc[row_filter, col_filter]

    def _add_novel_mtags(self, correlated_snps, ld_matrix, chromosome):
        highest_correlation = ld_matrix.max(axis="columns")

        for mtag_variant, highest_r in highest_correlation.items():
            assoc_snps = self._find_highest_correlation(ld_matrix, mtag_variant, highest_r)
            self._add_matches(correlated_snps, assoc_snps, mtag_variant, highest_r, chromosome)

    def _find_highest_correlation(self, ld_matrix, variant, highest_r):
        return list(ld_matrix.columns[ld_matrix.loc[variant, :].values == highest_r])

    def _add_matches(self, correlated_snps, assoc_snps, mtag_variant, highest_r, chromosome):
        if len(assoc_snps) == 0:
            correlated_snps.append([mtag_variant, np.nan, np.nan, chromosome])
        else:
            for assoc_snp in assoc_snps:
                correlated_snps.append([mtag_variant, assoc_snp, highest_r, chromosome])
