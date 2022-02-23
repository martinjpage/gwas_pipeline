from src.domain.api_prototype import APIPrototype
from src.domain.enums.gwas_catalog_keys import GWASCatalogKeys
import pandas as pd
import logging
import requests
import dpath.util
import sys
import re

# configure logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class GWASCatalogAPI(APIPrototype):

    def __init__(self):
        self._base_url = GWASCatalogKeys.base_url.value
        self._association_data = []
        self._association_fields = GWASCatalogKeys.field_names.value

    def search_trait_name_for_alleles(self, trait_name: str) -> None:
        """Find variant and risk alleles associated with a disease (trait) label in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_name: trait name to search"""
        logging.info(f"Searching for the trait ID of '{trait_name}'.")
        trait_code = self._find_trait_code(trait_name)
        self._lookup_associations(trait_code)

    def search_trait_code_for_alleles(self, trait_code: str) -> None:
        """Find variant and risk alleles associated with a disease (trait) ID in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_code: trait id to search"""
        self._lookup_associations(trait_code)

    def create_df(self) -> pd.DataFrame:
        """Combine the retrieved association data and the field (column) names into a pandas dataframe"""
        return pd.DataFrame(data=self._association_data, columns=self._association_fields)

    def write_to_csv(self, filename: str) -> None:
        """Combine the retrieved association data and the field (column) names and export data table to CSV
        :param filename: path for CSV file"""
        df = self.create_df()
        df.to_csv(filename, index=False)

    def _find_trait_code(self, trait_name: str) -> str:
        """Find the EFO trait ID of the trait label (disease term)"""
        url = self._base_url + f'efoTraits/search/findByEfoTrait?trait={trait_name}'
        response = self._query_api(url)

        if self._incorrect_entry_size(response, GWASCatalogKeys.efo_traits.value):
            raise ValueError(f'The number of efoTraits at {url} is not one. Inspect URL and check the'
                             'trait name search term.')

        trait_code = dpath.util.get(response, GWASCatalogKeys.trait_code.value)
        logging.info(f"Found the trait ID '{trait_code}' for '{trait_name}'.")
        return trait_code

    # ToDo EFO short names for each study - additional API call
    # ToDo Ancestry and Sample Size - loop to process
    def _lookup_associations(self, trait_code: str) -> None:
        """Retrieve association data for the trait ID and extract the data fields of interest
        :raises ValueError if specific lists within the data response that are assumed to have a length of one
        violate this assumption"""

        url = self._base_url + f'efoTraits/{trait_code}/associations?projection=associationByEfoTrait'
        response = self._query_api(url)
        associations = dpath.util.get(response, GWASCatalogKeys.associations.value)
        associations_length = len(associations)

        for i, entry in enumerate(associations):
            logging.info(f"Processing entry {i+1} of {associations_length}.")

            p_value = dpath.util.get(entry, GWASCatalogKeys.p_value.value)
            p_val_annotation = dpath.util.get(entry, GWASCatalogKeys.p_val_annotation.value)
            OR = dpath.util.get(entry, GWASCatalogKeys.odds_ratio.value)
            CI = dpath.util.get(entry, GWASCatalogKeys.conf_int.value)

            if self._incorrect_entry_size(entry, GWASCatalogKeys.loci.value):
                raise ValueError(f'The number of loci is not one for entry {i+1} at {url}. '
                                 f'Method assumes one locus.')

            if self._incorrect_entry_size(entry, GWASCatalogKeys.risk_alleles.value):
                raise ValueError(f'The number of strongestRiskAlleles for entry {i+1} at {url} is not one. '
                                 f'Method assumes one strongest risk allele.')

            allele = dpath.util.get(entry, GWASCatalogKeys.risk_allele_name.value)
            risk_allele, base_transition = self._clean_allele_name(allele)
            RAF = dpath.util.get(entry, GWASCatalogKeys.raf.value)
            reported_genes = self._get_genes(entry, GWASCatalogKeys.genes.value)

            if self._incorrect_entry_size(entry, GWASCatalogKeys.snps.value):
                raise ValueError(f'The number of snps for entry {i+1} at {url} is not one. '
                                 f'Method assumes one single nucleotide polymorphism.')

            chromosome_name, chromosome_position = self._get_chromosome(entry, GWASCatalogKeys.chromosomes.value)

            if chromosome_name == "" or chromosome_position == "":
                logging.info(f"Entry {i+1} at {url} does not contain information of the chromosome location.")

            study_id = dpath.util.get(entry, GWASCatalogKeys.study_id.value)
            reported_trait = dpath.util.get(entry, GWASCatalogKeys.reported_trait.value)

            self._association_data.append([risk_allele, base_transition, p_value, p_val_annotation, RAF, OR, CI,
                                           reported_genes, chromosome_name, chromosome_position, reported_trait,
                                           study_id])

        logging.info(f"All associations processed.")

    def _query_api(self, url: str, params={}) -> dict:
        """Make an HTTP request on the URL to retrieve data from an endpoint.
        :param url: web endpoint to query
        :param params: additional parameters for the request
        :return:content returned by the request"""
        logging.info(f"Requesting data from '{url}'.")
        response = requests.get(url=url, params=params)
        return response.json()

    def _incorrect_entry_size(self, data: dict, entry_path: str) -> bool:
        """Check if the length of an entry is one for lists nested in the data structure."""
        entry = dpath.util.get(data, entry_path)
        return len(entry) != 1

    def _clean_allele_name(self, allele_name: str) -> (str, str):
        """Parse full allele name to extract risk allele name and base transition
        :raises warning if allele name cannot be matched with regex or if the match does not have two elements"""
        risk_allele = ""
        base_transition = ""

        regex = r'([\w\-\:]+)\-([\w?]+)$'
        matched_groups = re.match(regex, allele_name)
        if not matched_groups:
            logging.warning(f"Allele name '{allele_name}' could not be parsed.")
        elif len(matched_groups.groups()) != 2:
            logging.warning(f"Allele name '{allele_name}' could not be split into a risk allele and base transition.")
        else:
            risk_allele, base_transition = matched_groups.groups()

        if base_transition not in GWASCatalogKeys.valid_bases.value:
            logging.warning(f"'{base_transition}' is not valid base transition.")

        return risk_allele, base_transition

    def _get_genes(self, data: dict, entry_path: str) -> str:
        """Find the gene names for all the gene entries and combine into a comma separated string of genes"""
        genes = dpath.util.get(data, entry_path)

        gene_names = []
        for gene in genes:
            gene_name = dpath.util.get(gene, GWASCatalogKeys.gene_name.value)
            gene_names.append(gene_name)
        return ", ".join(gene_names)

    def _get_chromosome(self, data: dict, entry_path: str) -> (str, str):
        locations = dpath.util.get(data, entry_path)

        chromosome_name = ""
        chromosome_position = ""
        for location in locations:
            if 'CHR' not in dpath.util.get(location, GWASCatalogKeys.chromosome_name.value):
                chromosome_name = dpath.util.get(location, GWASCatalogKeys.chromosome_name.value)
                chromosome_position = dpath.util.get(location, GWASCatalogKeys.chromosome_position.value)
        return chromosome_name, chromosome_position
