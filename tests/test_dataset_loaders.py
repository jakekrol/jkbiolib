import pytest
from jkbiolib.datasets.loaders import *

def test_getters():
    df1 = thousg_rna_short_read_samples()
    assert isinstance(df1, pd.DataFrame)
    df2 = thousg_rna_long_read_samples()
    assert isinstance(df2, pd.DataFrame)
    df3 = thousg_high_cov_short_read_tsv()
    assert isinstance(df3, pd.DataFrame)
    df4 = grch37_genes_bed()
    assert isinstance(df4, pd.DataFrame)
    df5 = grch37_exons_bed()
    assert isinstance(df5, pd.DataFrame)
