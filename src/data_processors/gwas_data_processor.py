import re
import dpath.util

from src.domain.associations_data_processor_prototype import AssociationsDataProcessorPrototype
from src.decorators.loggable import logger


# ToDo: exception handling if path does not work (key errors)
@logger
class GWASCatalogDataProcessor(AssociationsDataProcessorPrototype):

    def extract_data(self, raw_data):
        association_data = []
        associations = self._get_associations(raw_data)
        associations_length = len(associations) - 1

        for i, entry in enumerate(associations):
            self.logger.info(f"Processing entry {i} of {associations_length}.")
            if self._not_single_variant(entry):
                self.logger.info(f'Entry {i} is not a single variant because there is more than one '
                                 f'"strongestRiskAlleles". Skipping entry.')
                continue

            p_value = self._get_p_value(entry)
            if self._not_genome_wide_significant(p_value):
                self.logger.info(f'Entry {i} has a p-value ({p_value}) less than the threshold for genome-wide '
                                 f'significance ({self._config.sig_p_value}). Skipping entry.')
                continue

            if self._too_many_loci(entry):
                self.logger.info(f'Entry {i} has one than one locus. Method assumes one locus. Skipping entry.')
                continue

            if self._too_many_snps(entry):
                self.logger.info(f'Entry {i} has one than one snp. Method assumes one single nucleotide '
                                 f'polymorphism. Skipping entry.')
                continue

            chromosome = self._get_chromosome(entry)
            chromosome_name = self._get_chromosome_name(chromosome)

            if self._no_chromosome_name(chromosome_name):
                self.logger.info(f"Entry {i} does not contain information of the chromosome name. Skipping entry.")
                continue

            chromosome_position = self._get_chromosome_position(chromosome)

            full_allele = self._get_allele(entry)
            variant = self._get_variant(full_allele)

            if self._no_variant_name(variant):
                self.logger.info(f"Entry {i} does not contain a variant name that can be parsed. Skipping entry.")
                continue

            risk_allele = self._get_risk_allele(full_allele)

            p_val_annotation = self._get_p_val_annotation(entry)
            raf = self._get_raf(entry)
            odds_ratio = self._get_or(entry)
            conf_interval = self._get_ci(entry)

            reported_genes = self._get_reported_genes(entry)
            reported_trait = self._get_reported_trait(entry)
            study_id = self._get_study_id(entry)

            association_data.append([variant, risk_allele, p_value, p_val_annotation, raf, odds_ratio,
                                     conf_interval, reported_genes, chromosome_name, chromosome_position,
                                     reported_trait, study_id])

        self.logger.info("All associations processed.")
        return association_data, self._association_names

    def _get_associations(self, raw_data):
        return dpath.util.get(raw_data, self._config.associations)

    def _not_single_variant(self, data):
        return self._incorrect_entry_size(data, self._config.risk_alleles)

    def _not_genome_wide_significant(self, p_value):
        return p_value > self._config.sig_p_value

    def _too_many_loci(self, entry):
        return self._incorrect_entry_size(entry, self._config.loci)

    def _too_many_snps(self, entry):
        return self._incorrect_entry_size(entry, self._config.snps)

    def _incorrect_entry_size(self, data: dict, entry_path: str) -> bool:
        """Check if the length of an entry is one for lists nested in the data structure."""
        entry = dpath.util.get(data, entry_path)
        return len(entry) != 1

    def _no_chromosome_name(self, chromosome_name):
        return chromosome_name == ""

    def _no_variant_name(self, variant):
        return variant == ""

    def _get_p_value(self, entry):
        return dpath.util.get(entry, self._config.p_value)

    def _get_chromosome_name(self, entry):
        if entry is None:
            return ""
        return dpath.util.get(entry, self._config.chromosome_name)

    def _get_chromosome_position(self, entry):
        if entry is None:
            return ""
        return dpath.util.get(entry, self._config.chromosome_position)

    def _get_chromosome(self, entry):
        chromosomes = dpath.util.get(entry, self._config.chromosomes)

        for chromosome in chromosomes:
            if 'CHR' not in dpath.util.get(chromosome, self._config.chromosome_name):
                return chromosome
        return None

    def _get_allele(self, data):
        return dpath.util.get(data, self._config.risk_allele_name)

    def _get_variant(self, allele_name):
        allele_name = self._clean_allele_name(allele_name)
        variant = ""
        regex = r'([\w\-\:]+)\-[\w?]+$'
        matched_group = re.match(regex, allele_name)
        if self._check_regex_match(matched_group, allele_name):
            variant = matched_group.groups()[0]
        return variant

    def _clean_allele_name(self, allele_name):
        """Remove non-ASCII characters like unicode"""
        string_encode = allele_name.encode("ascii", "ignore")
        return string_encode.decode()

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

    def _get_p_val_annotation(self, entry):
        return dpath.util.get(entry, self._config.p_val_annotation)

    def _get_raf(self, entry):
        return dpath.util.get(entry, self._config.raf)

    def _get_or(self, entry):
        return dpath.util.get(entry, self._config.odds_ratio)

    def _get_ci(self, entry):
        return dpath.util.get(entry, self._config.conf_int)

    def _get_reported_genes(self, entry):
        """Find the gene names for all the gene entries and combine into a comma separated string of genes"""
        genes = dpath.util.get(entry, self._config.genes)

        gene_names = []
        for gene in genes:
            gene_name = dpath.util.get(gene, self._config.gene_name)
            gene_names.append(gene_name)
        return ", ".join(gene_names)

    def _get_reported_trait(self, data):
        return dpath.util.get(data, self._config.reported_trait)

    def _get_study_id(self, entry):
        return dpath.util.get(entry, self._config.study_id)
