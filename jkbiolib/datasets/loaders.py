import pandas as pd
from importlib.resources import files

def thougs_high_cov_short_read_tsv():
    """Load the TSV file from package data."""
    data_file = files('jkbiolib').joinpath('data/thousg-short_read-high_cov.index.tsv')
    with data_file.open('r') as f:
        return pd.read_csv(
            f,
			sep='\t',
			skiprows=23,
			comment=None,
		)

def grch37_genes_bed():
    """Load the BED file from package data."""
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
    """Load the BED file from package data."""
    data_file = files('jkbiolib').joinpath('data/gencode.v19.annotation.gtf.exons.bed.sorted.gz')
    with data_file.open('rb') as f:
        df = pd.read_csv(
            f,
            sep='\t',
            comment=None,
            compression='gzip'
        )
        return df