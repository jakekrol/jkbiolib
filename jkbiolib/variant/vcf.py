from cyvcf2 import VCF, Writer
import pandas as pd
import os

def allele_fraction(vcf_in: str, samples_exclude: list[str] = None) -> tuple[pd.DataFrame, int]:
    # diploid only
    PLOIDY=2
    assert os.path.exists(vcf_in), f"Input VCF file does not exist: {vcf_in}"
    vcf = VCF(vcf_in)
    samples = vcf.samples
    n_samples_include = len(set(samples) - set(samples_exclude)) if samples_exclude else len(samples)
    data =[]
    for i,v in enumerate(vcf):
        svid = v.ID if v.ID is not None else '.'
        alt_alleles = 0
        for j, gt in enumerate(v.genotypes):
            if samples_exclude and samples[j] in samples_exclude:
                continue
            allele1 = gt[0]
            allele2 = gt[1]
            # we don't simply add because the encoding is -1 and 1 not 0 and 1
            if (allele1 == 1):
                alt_alleles+=1
            if (allele2 == 1):
                alt_alleles+=1
        af = alt_alleles / (PLOIDY * n_samples_include)
        data.append((svid, af))
    df_af = pd.DataFrame(data, columns=['SVID', 'Allele_Fraction'])
    df_af = df_af.sort_values(by='Allele_Fraction', ascending=False)
    return df_af, n_samples_include

def count_alt_samples(vcf_in: str, samples_exclude: list[str] = None) -> tuple[pd.DataFrame, int]:
    assert os.path.exists(vcf_in), f"Input VCF file does not exist: {vcf_in}"
    vcf = VCF(vcf_in)
    samples = vcf.samples
    n_samples_include = len(set(samples) - set(samples_exclude)) if samples_exclude else len(samples)
    data =[]
    for i,v in enumerate(vcf):
        svid = v.ID if v.ID is not None else '.'
        alt_count = 0
        for j, gt in enumerate(v.genotypes):
            if samples_exclude and samples[j] in samples_exclude:
                continue
            allele1 = gt[0]
            allele2 = gt[1]
            if (allele1 == 1) or (allele2 == 1):
                alt_count+=1
        data.append((svid, alt_count))
    df = pd.DataFrame(data, columns=['SVID', 'Alt_Sample_Count'])
    df = df.sort_values(by='Alt_Sample_Count', ascending=False)
    return df, n_samples_include

def add_id(vcf_in, vcf_out):
    assert os.path.exists(vcf_in), f"Input VCF file does not exist: {vcf_in}"
    vcf = VCF(vcf_in)
    with Writer(vcf_out, vcf) as w:
        for i, v in enumerate(vcf):
            if v.ID is None:
                v.ID = f"{v.CHROM}_{v.POS}_{i}"
            w.write_record(v)

def split_vcf(vcf_in, dir_out, delimiter='---'):
    assert os.path.exists(vcf_in), f"Input VCF file does not exist: {vcf_in}"
    assert os.path.isdir(dir_out), f"Output directory does not exist: {dir_out}"
    vcf = VCF(vcf_in)
    for i, v in enumerate(vcf):
        id = v.ID if v.ID is not None else ''
        chrom = v.CHROM if v.CHROM is not None else ''
        start = v.POS if v.POS is not None else ''
        end = v.INFO.get('END') if v.INFO.get('END') is not None else ''
        svtype = v.INFO.get('SVTYPE') if v.INFO.get('SVTYPE') is not None else ''
        outfile = f"{i}{delimiter}{id}{delimiter}{chrom}_{start}_{end}_{svtype}.vcf"
        out_path = os.path.join(dir_out, outfile)
        try:
            with Writer(out_path, vcf) as w:
                w.write_record(v)
        except Exception as e:
            print(f"Warning: Could not write record {i} ({chrom}:{start}). Error: {e}")
        