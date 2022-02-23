from src.apis.gwas_catalog_api import GWASCatalogAPI
import time

if __name__ == '__main__':
    api = GWASCatalogAPI()
    t0 = time.time()
    # api.search_trait_code_for_alleles("EFO_0000685")
    api.search_trait_name_for_alleles("rheumatoid arthritis")
    t1 = time.time()
    print("Elapsed time during the whole program in seconds:", t1 - t0)
    api.write_to_csv("ra_assoc.csv")
