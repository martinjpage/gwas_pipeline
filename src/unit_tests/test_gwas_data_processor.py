# import json
# from collections import namedtuple
#
# from src.data_processors.gwas_data_processor import GWASCatalogDataProcessor
#
#
# class TestGWASCatalogDataProcessor:
#
#     def setup(self):
#         with open('gwas_catalog_EFO_0000685_associations_by_trait.txt') as f:
#             self._json_data = json.load(f)
#
#         config = {
#             'efo_traits': '_embedded/efoTraits',
#             'trait_code':' _embedded/efoTraits/0/shortForm',
#             'associations': '_embedded/associations',
#             'p_value': 'pvalue',
#             'p_val_annotation': 'pvalueDescription',
#             'odds_ratio': 'orPerCopyNum',
#             'conf_int': 'range',
#             'loci_description': 'loci/0/description',
#             'loci_single_variant': 'Single variant',
#             'loci': 'loci',
#             'risk_alleles': 'loci/0/strongestRiskAlleles',
#             'risk_allele_name': 'loci/0/strongestRiskAlleles/0/riskAlleleName',
#             'raf': 'loci/0/strongestRiskAlleles/0/riskFrequency',
#             'genes': 'loci/0/authorReportedGenes',
#             'gene_name': 'geneName',
#             'snps': 'snps',
#             'chromosomes': 'snps/0/locations',
#             'chromosome_name': 'chromosomeName',
#             'chromosome_position': 'chromosomePosition',
#             'study_id': 'study/accessionId',
#             'reported_trait': 'study/diseaseTrait/trait',
#             'sig_p_value': 0.000001}
#
#         self._config = namedtuple('configuration', config.keys())(**config)
#
#     def test_extract_data(self):
#         processor = GWASCatalogDataProcessor(self._config)
#         processed_data, column_names = processor.extract_data(self._json_data)
