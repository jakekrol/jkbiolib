import pandas as pd
from importlib.resources import files

def thousg_dna_long_read_samples():
    f = files('jkbiolib').joinpath('data/thousg-dna-long_read-samples.tsv.gz')
    return pd.read_csv(
        f,
        sep='\t',
        comment=None
    )

def thousg_rna_short_read_samples():
    f = files('jkbiolib').joinpath('data/thousg-rna-short_read-samples.tsv')
    return pd.read_csv(
        f,
        sep='\t',
        comment=None
    )

def thousg_rna_long_read_samples():
    f = files('jkbiolib').joinpath('data/thousg-rna-long_read-samples.tsv')
    return pd.read_csv(
        f,
        sep='\t',
        comment=None
    )

def thousg_high_cov_short_read_tsv():
    f = files('jkbiolib').joinpath('data/thousg-short_read-high_cov.index.tsv')
    return pd.read_csv(
        f,
        sep='\t',
        skiprows=23,
        comment=None
    )

def grch37_genes_bed():
    f = files('jkbiolib').joinpath('data/gencode.v19.annotation.gtf.gene.bed.sorted.gz')
    return pd.read_csv(
        f,
        sep='\t',
        comment=None
    )
    
def grch37_exons_bed():
    f = files('jkbiolib').joinpath('data/gencode.v19.annotation.gtf.exons.bed.sorted.gz')
    return pd.read_csv(
        f,
        sep='\t',
        comment=None
    )