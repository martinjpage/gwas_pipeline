from gwas_api import GwasAPI


class TestGwasAPI:

    def test_search_trait_name_for_alleles_valid_string(self):
        api = GwasAPI()
        df_trait_name = api.search_trait_name_for_alleles("rheumatoid arthritis")
        df_trait_code = api.search_trait_code_for_alleles("EFO_0000685")
        assert df_trait_name.equals(df_trait_code)
