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