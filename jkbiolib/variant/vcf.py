from cyvcf2 import VCF, Writer
import os

def split_vcf(vcf_in, dir_out):
    assert os.path.exists(vcf_in), f"Input VCF file does not exist: {vcf_in}"
    assert os.path.isdir(dir_out), f"Output directory does not exist: {dir_out}"
    vcf = VCF(vcf_in)
    for i, v in enumerate(vcf):
        id = v.ID if v.ID is not None else f"var_{i}"
        out_path = os.path.join(dir_out, f"{id}.vcf")
        with Writer(out_path, vcf) as w:
            w.write_record(v)
        