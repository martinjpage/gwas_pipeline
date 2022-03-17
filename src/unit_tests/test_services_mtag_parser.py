from src.services.mtag_parser import MtagParser


class TestServicesMtagParser:

    def test_func(self):
        filename = 'C:\\Users\\Martin\\OneDrive\\Documents\\Study\\rp1\\mtag.txt'
        snp_col = 'snp_name'
        chr_col = 'chrom_name'

        parser = MtagParser()
        mtag_snps = parser.read_file(filename, snp_col, chr_col)
        print(mtag_snps)
