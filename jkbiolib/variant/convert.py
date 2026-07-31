from cyvcf2 import VCF
import subprocess

def vcf2stix_queries(path_vcf, path_out, out_header=False):
    VALID_SVTYPES = {'DEL', 'DUP', 'INV', 'INS', 'BND'}
    vcf = VCF(path_vcf)
    with open(path_out, 'w') as f:
        if out_header:
            f.write("ID\tCHROM\tLEFT_START\tLEFT_END\tRIGHT_START\tRIGHT_END\tSVTYPE\n")
        for i, variant in enumerate(vcf):
            id = variant.ID if variant.ID is not None else f"var_{i}"
            ### svtype
            svtype = variant.INFO.get('SVTYPE')
            if svtype not in VALID_SVTYPES:
                print("# warning: skipping variant with unsupported SVTYPE:", svtype)
                continue
            ### coordinates
            position = variant.POS
            left_start, left_end = position, position
            if svtype != 'INS':
                end = variant.INFO.get('END')
                right_start, right_end = end, end
                # confidence intervals are optional
                cipos = None
                ciend = None
                try:
                    cipos_lower, cipos_upper = variant.INFO.get('CIPOS')
                    left_start += cipos_lower
                    left_end += cipos_upper
                except TypeError:
                    pass
                try:
                    ciend_lower, ciend_upper = variant.INFO.get('CIEND')
                    right_start += ciend_lower
                    right_end += ciend_upper
                except TypeError:
                    pass
            else:
                svlen = variant.INFO.get('SVLEN')
                if svlen is None:
                    print("# warning: skipping INS variant with missing SVLEN:", id)
                    continue
                right_start = position
                right_end = position + svlen
            f.write(f"{id}\t{variant.CHROM}\t{left_start}\t{left_end}\t{right_start}\t{right_end}\t{svtype}\n")
            
                    
def vcf2bed(path_vcf, path_out, out_header=False):
    cmd = [
        "bcftools",
        "query",
        "-f",
        "%CHROM\t%POS0\t%END\t%ID\n",
        path_vcf
    ]
    if out_header:
        with open(path_out, "w") as f:
            f.write("CHROM\tSTART\tEND\tID\n")
    with open(path_out, "a") as f:
        subprocess.run(cmd, stdout=f)
    # VALID_SVTYPES = {'DEL', 'DUP', 'INV', 'INS', 'BND'}
    # vcf = VCF(path_vcf)
    # with open(path_out, 'w') as f:
    #     if out_header:
    #         f.write("CHROM\tSTART\tEND\tID\tSVTYPE\n")
    #     for i, variant in enumerate(vcf):
    #         id = variant.ID if variant.ID is not None else f"var_{i}"
    #         ### svtype
    #         svtype = variant.INFO.get('SVTYPE')
    #         if svtype not in VALID_SVTYPES:
    #             print("# warning: skipping variant with unsupported SVTYPE:", svtype)
    #             continue
    #         ### coordinates
    #         start = variant.POS
    #         # left_start, left_end = position, position
    #         if svtype != 'INS':
    #             end = variant.INFO.get('END')
    #         else:
    #             svlen = variant.INFO.get('SVLEN')
    #             if svlen is None:
    #                 print("# warning: skipping INS variant with missing SVLEN:", id)
    #                 continue
    #             end = start + svlen
    #         f.write(f"{id}\t{variant.CHROM}\t{start}\t{end}\t{id}\t{svtype}\n")