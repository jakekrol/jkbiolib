from jkbiolib.variant.convert import vcf2stix_queries, vcf2bed
from jkbiolib.variant.vcf import split_vcf, count_alt_samples, allele_fraction
import os
import pytest
import pandas as pd

def test_allele_fraction():
	samples_exclude=['COLO829SV']
	path_vcf = './data/colo829_somatic_grch38_nogt00.needLR.4.0.intermediate_truvari_collapse_out.vcf'
	df, numsamples = allele_fraction(path_vcf, samples_exclude=samples_exclude)
	df.to_csv('./data/allele_fractions.tsv', sep='\t', index=False)
	assert isinstance(df, pd.DataFrame)
	assert numsamples > 0

def test_count_alt_samples():
	samples_exclude=['COLO829SV']
	path_vcf = './data/colo829_somatic_grch38_nogt00.needLR.4.0.intermediate_truvari_collapse_out.vcf'
	df, numsamples = count_alt_samples(path_vcf, samples_exclude=samples_exclude)
	df.to_csv('./data/alt_sample_counts.tsv', sep='\t', index=False)
	assert isinstance(df, pd.DataFrame)
	assert numsamples > 0

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