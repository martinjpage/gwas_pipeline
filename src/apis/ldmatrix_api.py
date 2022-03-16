import requests
import pandas as pd
from io import StringIO

from src.decorators.loggable import logger
from src.domain.ld_api_prototype import LDAPIPrototype


# ToDo: Error handling for bad requests; no data return
@logger
class LDMatrixAPI(LDAPIPrototype):

    def get_ld_score(self, ref_snp: str, snp_list: list) -> pd.DataFrame:
        snp_request = self._create_snp_request(ref_snp, snp_list)
        url = self._config.base_url + snp_request + \
              self._config.params_url.format(self._config.ref_pop, self._config.score, self._config.genome_build,
                                             self._config.token)
        data_string = self._query_api(url)
        return self._parse_response(data_string)

    def _create_snp_request(self, ref_snp, snp_list):
        snp_request_reference = self._config.snps_url.format(ref_snp)
        snp_request_queries = '%0A'.join(snp_list)
        return snp_request_reference + snp_request_queries

    def _query_api(self, url: str, params={}) -> dict:
        """Make an HTTP request on the URL to retrieve data from an endpoint.
        :param url: web endpoint to query
        :param params: additional parameters for the request
        :return:content returned by the request"""
        self.logger.info(f"Requesting data from '{url}'.")
        response = requests.get(url=url, params=params)
        self.logger.info(f"Data retrieved.")
        return response.text

    def _parse_response(self, data_string):
        return pd.read_csv(StringIO(data_string), sep='\t', header=0, index_col=0)
