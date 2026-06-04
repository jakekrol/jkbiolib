import pytest
from jkbiolib.variant.vcf2stix_queries import vcf2stix_queries
import os

def test_vcf2stix_queries():
	path_vcf = './data/genotypes.vcf.gz'
	tmp_path = './data/stix_queries.txt'
	vcf2stix_queries(path_vcf, tmp_path, out_header=True)
	assert os.path.exists(tmp_path)