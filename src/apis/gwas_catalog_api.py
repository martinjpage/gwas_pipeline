import requests
import dpath.util

from src.decorators.loggable import logger
from src.domain.associations_api import AssociationsAPI


@logger
class GWASCatalogAPI(AssociationsAPI):

    def _search_trait_name_for_alleles(self, trait_name: str) -> dict:
        """Find variant and risk alleles associated with a disease (trait) label in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_name: trait name to search"""
        self.logger.info(f"Searching for the trait ID of '{trait_name}'.")
        trait_code = self._find_trait_code(trait_name)
        return self._get_raw_data(trait_code)

    def _search_trait_code_for_alleles(self, trait_code: str) -> dict:
        """Find variant and risk alleles associated with a disease (trait) ID in the GWAS Catalog Experimental
        Factor Ontology (excluding child trait data)
        :param trait_code: trait id to search"""
        return self._get_raw_data(trait_code)

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

    def _get_raw_data(self, trait_code):
        url = self._config.base_url + self._config.associations_url.format(trait_code)
        return self._query_api(url)

    def _query_api(self, url: str, params={}) -> dict:
        """Make an HTTP request on the URL to retrieve data from an endpoint.
        :param url: web endpoint to query
        :param params: additional parameters for the request
        :return:content returned by the request"""
        self.logger.info(f"Requesting data from '{url}'.")
        response = requests.get(url=url, params=params)
        self.logger.info(f"Data retrieved.")
        return response.json()

    def _incorrect_entry_size(self, data: dict, entry_path: str) -> bool:
        """Check if the length of an entry is one for lists nested in the data structure."""
        entry = dpath.util.get(data, entry_path)
        return len(entry) != 1
