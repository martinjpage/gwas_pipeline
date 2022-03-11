# from collections import namedtuple
#
#
# def config():
#     config = {
#         'base_url': 'https://ldlink.nci.nih.gov/LDlinkRest/ldmatrix?',
#         'snps_url': 'snps={}%0A',
#         'params_url': '&pop={}&r2_d={}&genome_build={}&token={}',
#         'ref_pop': 'CEU',
#         'score': 'r',
#         'genome_build': 'grch37',
#         'token': '38b336ccb8fb'}
#
#     return namedtuple('configuration', config.keys())(**config)
#
#
# config = config()
# api = LDMatrixAPI(config)
# raw_data = api.get_ld_score('rs56387622', ['rs56138756', 'rs3821902', 'rs9837602'])
