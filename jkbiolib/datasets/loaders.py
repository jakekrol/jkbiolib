import pandas as pd
from importlib.resources import files

def thousg_dna_long_read_samples():
    data_file = files('jkbiolib').joinpath('data/thousg-dna-long_read-samples.tsv.gz')
    with data_file.open('r') as f:
        return pd.read_csv(
            f,
            sep='\t',
            comment=None,
            compression='gzip'
        )

def thousg_rna_short_read_samples():
    data_file = files('jkbiolib').joinpath('data/thousg-rna-short_read-samples.tsv')
    with data_file.open('r') as f:
        return pd.read_csv(
            f,
            sep='\t',
            comment=None,
        )

def thousg_rna_long_read_samples():
    data_file = files('jkbiolib').joinpath('data/thousg-rna-long_read-samples.tsv')
    with data_file.open('r') as f:
        return pd.read_csv(
            f,
            sep='\t',
            comment=None,
        )

def thousg_high_cov_short_read_tsv():
    data_file = files('jkbiolib').joinpath('data/thousg-short_read-high_cov.index.tsv')
    with data_file.open('r') as f:
        return pd.read_csv(
            f,
			sep='\t',
			skiprows=23,
			comment=None,
		)

def grch37_genes_bed():
    data_file = files('jkbiolib').joinpath('data/gencode.v19.annotation.gtf.gene.bed.sorted.gz')
    with data_file.open('rb') as f:
        df = pd.read_csv(
            f,
            sep='\t',
            comment=None,
            compression='gzip'
        )
        return df
    
def grch37_exons_bed():
    data_file = files('jkbiolib').joinpath('data/gencode.v19.annotation.gtf.exons.bed.sorted.gz')
    with data_file.open('rb') as f:
        df = pd.read_csv(
            f,
            sep='\t',
            comment=None,
            compression='gzip'
        )
        return df