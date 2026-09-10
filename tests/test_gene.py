import pytest
from jkbiolib.gene.human import gene2region

def test_pass_gene2region():
    gene = 'PARGP1'
    chrom, start, end, strand = gene2region(gene)
    assert chrom == '10'
    assert start == 51623417
    assert end == 51732824
    assert strand == 1
    gene = 'ERG'
    chrom, start, end, strand = gene2region(gene)
    assert chrom == '21'
    assert start == 39751949
    assert end == 40033704
    assert strand == -1

def test_fail_gene2region():
    gene='notgene'
    # a failure is False, False, False, False
    chrom, start, end, strand = gene2region(gene)
    assert not any((chrom, start, end, strand))
