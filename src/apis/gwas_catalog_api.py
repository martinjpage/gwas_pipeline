import requests
import dpath.util

from src.decorators.loggable import logger
from src.domain.associations_api_prototype import AssociationsAPIPrototype


@logger
class GWASCatalogAPI(AssociationsAPIPrototype):

    def _search_trait_name_for_alleles(self, trait_name: str, include_child: bool) -> list:
        """Find variant and risk alleles associated with a disease (trait) label in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_name: trait name to search"""
        self.logger.info(f"Searching for the trait ID of '{trait_name}'.")
        trait_code = self._find_trait_code(trait_name)
        return self._get_raw_data(trait_code, include_child)

    def _search_trait_code_for_alleles(self, trait_code: str, include_child: bool) -> list:
        """Find variant and risk alleles associated with a disease (trait) ID in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_code: trait id to search"""
        return self._get_raw_data(trait_code, include_child)

    def _find_trait_code(self, trait_name: str) -> str:
        """Find the EFO trait ID of the trait label (disease term)"""
        url = self._config.base_url + self._config.trait_code_url.format(trait_name)
        response = self._query_api(url)

        if self._incorrect_entry_size(response, self._config.efo_traits):
            raise ValueError(f'The number of efoTraits at {url} is not one. Inspect URL and check the'
                             'trait name search term.')

        trait_code = dpath.util.get(response, self._config.trait_code)
        self.logger.info(f"Found the trait ID '{trait_code}' for '{trait_name}'.")
        return trait_code

    def _get_raw_data(self, trait_code, include_child):
        # ToDo: move _get_associations processing to GWASCatalogDataProcessor class
        if include_child:
            trait_codes = self._add_child_traits(trait_code)
        else:
            trait_codes = [trait_code]

        association_data = []
        for trait in trait_codes:
            url = self._config.base_url + self._config.associations_url.format(trait)
            raw_trait_data = self._query_api(url)
            trait_associations = self._get_associations(raw_trait_data)
            association_data.extend(trait_associations)
        return association_data

    # ToDo: move child trait processing to GWASCatalogDataProcessor class
    def _add_child_traits(self, trait_code):
        trait_codes = [trait_code]

        url = self._config.childen_url.format(trait_code)
        raw_data = self._query_api(url)
        try:
            child_trait_data = dpath.util.get(raw_data, self._config.child_terms)
        except KeyError:
            self.logger.info("No child traits.")
            return trait_codes

        for child_trait in child_trait_data:
            child_code = dpath.util.get(child_trait, self._config.child_efo)
            child_label = dpath.util.get(child_trait, self._config.child_name)
            self.logger.info(f'Adding child trait {child_label} with id {child_code}')
            trait_codes.append(child_code)
        return trait_codes

    def _get_associations(self, raw_data):
        try:
            return dpath.util.get(raw_data, self._config.associations)
        except KeyError:
            self.logger.info("No association data found for entry.")
            return []

    def _query_api(self, url: str, params={}) -> dict:
        """Make an HTTP request on the URL to retrieve data from an endpoint.
        :param url: web endpoint to query
        :param params: additional parameters for the request
        :return:content returned by the request"""
        self.logger.info(f"Requesting data from '{url}'.")
        response = requests.get(url=url, params=params)
        self.logger.info(f"API request complete. Response {response.status_code}.")
        if response.status_code == 404:
            return {}
        return response.json()

    def _incorrect_entry_size(self, data: dict, entry_path: str) -> bool:
        """Check if the length of an entry is one for lists nested in the data structure."""
        entry = dpath.util.get(data, entry_path)
        return len(entry) != 1
