import requests

from src.decorators.loggable import logger


@logger
class LDMatrixAPI:

    def find_ld_stats(self, snp1, snp2, pop, score='r', build='grch38_high_coverage', token='38b336ccb8fb'):
        base_url = 'https://ldlink.nci.nih.gov/LDlinkRest/ldmatrix?'
        ld_url = f'snps={snp1}%0A{snp2}&pop={pop}&r2_d={score}&genome_build={build}&token={token}'
        url = base_url + ld_url
        raw_data = self._query_api(url)
        return raw_data


    def _query_api(self, url: str, params={}) -> dict:
        """Make an HTTP request on the URL to retrieve data from an endpoint.
        :param url: web endpoint to query
        :param params: additional parameters for the request
        :return:content returned by the request"""
        self.logger.info(f"Requesting data from '{url}'.")
        response = requests.get(url=url, params=params)
        self.logger.info(f"Data retrieved.")
        return response.text


if __name__ == '__main__':
    api = LDMatrixAPI()
    raw_data = api.find_ld_stats('rs11249433', 'rs2290854', pop='CEU')
