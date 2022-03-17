from collections import namedtuple

from src.apis.ldmatrix_api import LDMatrixAPI

class TestLDMatrixAPI:

    def test_get_ld_score(self):

        config = {
            'base_url': 'https://ldlink.nci.nih.gov/LDlinkRest/ldmatrix?',
            'query_url': 'snps={}&pop={}&r2_d={}&genome_build={}&token={}',
            'ref_pop': 'CEU',
            'score': 'r',
            'genome_build': 'grch37',
            'token': '38b336ccb8fb'}

        config = namedtuple('configuration', config.keys())(**config)

        api = LDMatrixAPI(config)
        mtag_snps = ['rs2240335', 'rs2476601', 'rs2476601', 'rs2240335']
        association_snps = ['rs1057941', 'rs10796944', 'rs10864459', 'rs10923574', 'rs11117758', 'rs11119434',
                            'rs11119608', 'rs11161996', 'rs11205303']

        raw_data = api.get_ld_score(mtag_snps, association_snps)
