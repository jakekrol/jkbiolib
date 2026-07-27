import pytest
from jkbiolib.variant.convert import vcf2stix_queries, vcf2bed
from jkbiolib.variant.vcf import split_vcf
import os

def test_vcf2stix_queries():
	path_vcf = './data/genotypes.vcf.gz'
	tmp_path = './data/stix_queries.txt'
	vcf2stix_queries(path_vcf, tmp_path, out_header=True)
	assert os.path.exists(tmp_path)

def test_vcf2bed():
	path_vcf = './data/genotypes.vcf.gz'
	tmp_path = './data/variants.bed'
	vcf2bed(path_vcf, tmp_path, out_header=True)
	assert os.path.exists(tmp_path)

def test_split_vcf():
	path_vcf = './data/genotypes.vcf.gz'
	tmp_dir = './data/split'
	os.makedirs(tmp_dir, exist_ok=True)
	split_vcf(path_vcf, tmp_dir)
	assert os.path.exists(tmp_dir)