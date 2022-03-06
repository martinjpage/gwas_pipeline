import re
import dpath.util

from src.domain.data_processor import DataProcessor
from src.decorators.loggable import logger


@logger
class GWASCatalogDataProcessor(DataProcessor):

    def extract_data(self, raw_data):
        association_data = []
        associations = self._get_associations(raw_data)
        associations_length = len(associations) - 1

        for i, entry in enumerate(associations):
            self.logger.info(f"Processing entry {i} of {associations_length}.")
            if self._check_not_single_variant(entry):
                self.logger.info(f'Entry {i} is not a single variant because there is more than one '
                                 f'"strongestRiskAlleles". Skipping entry.')
                continue
            self._check_entry(i, entry)
            full_allele = self._get_allele(entry)
            variant = self._get_variant(full_allele)
            risk_allele = self._get_risk_allele(full_allele)
            # ToDo filter p-value: get value earlier; check if significant; skip entry if not
            p_value = self._get_p_value(entry)
            p_val_annotation = self._get_p_val_annotation(entry)
            raf = self._get_raf(entry)
            odds_ratio = self._get_or(entry)
            conf_interval = self._get_ci(entry)
            reported_genes = self._get_reported_genes(entry)
            chromosome = self._get_chromosome(entry)
            if chromosome is None:
                self.logger.info(f"Entry {i} does not contain information of the chromosome location.")
            chromosome_name = self._get_chromosome_name(chromosome)
            chromosome_position = self._get_chromosome_name(chromosome)
            reported_trait = self._get_reported_trait(entry)
            study_id = self._get_study_id(entry)

            association_data.append([variant, risk_allele, p_value, p_val_annotation, raf, odds_ratio,
                                           conf_interval, reported_genes, chromosome_name, chromosome_position,
                                           reported_trait, study_id])

        self.logger.info("All associations processed.")
        return association_data, self._association_names

    def _get_associations(self, raw_data):
        return dpath.util.get(raw_data, self._key.associations)

    def _check_not_single_variant(self, data):
        if self._incorrect_entry_size(data, self._key.risk_alleles):
            return True
        return False

    def _check_entry(self, i, entry):
        if self._incorrect_entry_size(entry, self._key.loci):
            raise ValueError(f'The number of loci is not one for entry {i}. Method assumes one locus.')

        if self._incorrect_entry_size(entry, self._key.snps):
            raise ValueError(f'The number of snps for entry {i} is not one. Method assumes one single nucleotide '
                             f'polymorphism.')

    def _incorrect_entry_size(self, data: dict, entry_path: str) -> bool:
        """Check if the length of an entry is one for lists nested in the data structure."""
        entry = dpath.util.get(data, entry_path)
        return len(entry) != 1

    def _get_allele(self, data):
        return dpath.util.get(data, self._key.risk_allele_name)

    def _get_variant(self, allele_name):
        variant = ""
        regex = r'([\w\-\:]+)\-[\w?]+$'
        matched_group = re.match(regex, allele_name)
        if self._check_regex_match(matched_group, allele_name):
            variant = matched_group.groups()[0]
        return variant

    def _get_risk_allele(self, allele_name):
        risk_allele = ""
        regex = r'[\w\-\:]+\-([\w?]+)$'
        matched_group = re.match(regex, allele_name)
        if self._check_regex_match(matched_group, allele_name):
            risk_allele = matched_group.groups()[0]
        return risk_allele

    def _check_regex_match(self, matched_group, allele_name):
        if not matched_group:
            self.logger.warning(f"Allele name '{allele_name}' could not be parsed.")
            return False
        elif len(matched_group.groups()) != 1:
            self.logger.warning(f"Allele name '{allele_name}' could not be split into a variant and risk allele.")
            return False
        return True

    def _get_p_value(self, entry):
        return dpath.util.get(entry, self._key.p_value)

    def _get_p_val_annotation(self, entry):
        return dpath.util.get(entry, self._key.p_val_annotation)

    def _get_raf(self, entry):
        return dpath.util.get(entry, self._key.raf)

    def _get_or(self, entry):
        return dpath.util.get(entry, self._key.odds_ratio)

    def _get_ci(self, entry):
        return dpath.util.get(entry, self._key.conf_int)

    def _get_reported_genes(self, entry):
        """Find the gene names for all the gene entries and combine into a comma separated string of genes"""
        genes = dpath.util.get(entry, self._key.genes)

        gene_names = []
        for gene in genes:
            gene_name = dpath.util.get(gene, self._key.gene_name)
            gene_names.append(gene_name)
        return ", ".join(gene_names)

    def _get_chromosome_name(self, entry):
        if entry is None:
            return ""
        return dpath.util.get(entry, self._key.chromosome_name)

    def _get_chromosome_position(self, entry):
        if entry is None:
            return ""
        return dpath.util.get(entry, self._key.chromosome_position)

    def _get_chromosome(self, entry):
        chromosomes = dpath.util.get(entry, self._key.chromosomes)

        for chromosome in chromosomes:
            if 'CHR' not in dpath.util.get(chromosome, self._key.chromosome_name):
                return chromosome
        return None

    def _get_reported_trait(self, data):
        return dpath.util.get(data, self._key.reported_trait)

    def _get_study_id(self, entry):
        return dpath.util.get(entry, self._key.study_id)
