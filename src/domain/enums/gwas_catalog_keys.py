from enum import Enum


class GWASCatalogKeys(Enum):
    base_url = 'https://www.ebi.ac.uk/gwas/rest/api/'
    efo_traits = '_embedded/efoTraits'
    trait_code = '_embedded/efoTraits/0/shortForm'
    associations = '_embedded/associations'
    p_value = 'pvalue'
    p_val_annotation = 'pvalueDescription'
    odds_ratio = 'orPerCopyNum'
    conf_int = 'range'
    loci = 'loci'
    risk_alleles = 'loci/0/strongestRiskAlleles'
    risk_allele_name = 'loci/0/strongestRiskAlleles/0/riskAlleleName'
    raf = 'loci/0/strongestRiskAlleles/0/riskFrequency'
    genes = 'loci/0/authorReportedGenes'
    gene_name = 'geneName'
    snps = 'snps'
    chromosomes = 'snps/0/locations'
    chromosome_name = 'chromosomeName'
    chromosome_position = 'chromosomePosition'
    study_id = 'study/accessionId'
    reported_trait = 'study/diseaseTrait/trait'
    field_names = ['risk_allele', 'base_transition', 'p_value', "p_val_annotation",
                   "RAF", "OR", "CI", "reported_genes", "chromosome_name", "chromosome_position",
                   "reported_trait", "study"]
