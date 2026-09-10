from cyvcf2 import VCF
import subprocess
from jkbiolib.interval.core import compare_intervals

# decompose the region parsing logic for variant type groups
# BND needs to check if "[" or "]" to assign left and right interval
def vcf2stix_queries(path_vcf, path_out, out_header=False, id_fill_prefix="variant_"):
    VALID_SVTYPES = {'DEL', 'DUP', 'INV', 'INS', 'BND'}
    skipped_svs=[]


    def clean_chromosome(s):
        if s.lower().startswith("chr"):
            s = s[3:]
        return s
    
    def pad_confidence_intervals(
        left_start, left_end,
        right_start, right_end,
        cipos_lower=None, cipos_upper=None,
        ciend_lower=None, ciend_upper=None
    ):
        if cipos_lower:
            left_start += cipos_lower
        if cipos_upper:
            left_end += cipos_upper
        if ciend_lower:
            right_start += ciend_lower
        if ciend_upper:
            right_end += ciend_upper
        return left_start, left_end, right_start, right_end
        
    # for most SVs
    def sv2query(vcf_record):
        success=False
        position = vcf_record.POS
        # chromosome
        left_chrom = vcf_record.CHROM
        left_chrom = clean_chromosome(left_chrom)
        right_chrom = left_chrom
        # base pairs
        left_start, left_end = position, position
        end = vcf_record.INFO.get('END')
        right_start, right_end = end, end
        cipos_lower, cipos_upper, ciend_lower, ciend_upper = None, None, None, None
        try:
            cipos_lower, cipos_upper = vcf_record.INFO.get('CIPOS')
            ciend_lower, ciend_upper = vcf_record.INFO.get('CIEND')
        except TypeError as e:
            pass
        left_start, left_end, right_start, right_end = pad_confidence_intervals(
            left_start, left_end,
            right_start, right_end,
            cipos_lower, cipos_upper,
            ciend_lower, ciend_upper
        )
        success=True
        return success, left_chrom, left_start, left_end, right_chrom, right_start, right_end

    def ins2query(vcf_record):
        success = False
        svlen = vcf_record.INFO.get('SVLEN')
        if svlen is None:
            print(f"# unable to parse INS SV '{vcf_record.ID}' due to missing SVLEN")
            return False, None, None, None, None, None, None
        # chromosome
        left_chrom = vcf_record.CHROM
        left_chrom = clean_chromosome(left_chrom)
        right_chrom = left_chrom
        # base pairs
        position = vcf_record.POS
        left_start, left_end = position, position
        right_start = position
        right_end = right_start + svlen
        cipos_lower, cipos_upper, ciend_lower, ciend_upper = None, None, None, None
        try:
            cipos_lower, cipos_upper = vcf_record.INFO.get('CIPOS')
            ciend_lower, ciend_upper = vcf_record.INFO.get('CIEND')
        except TypeError as e:
            pass
        left_start, left_end, right_start, right_end = pad_confidence_intervals(
            left_start, left_end,
            right_start, right_end,
            cipos_lower, cipos_upper,
            ciend_lower, ciend_upper
        )
        success = True
        return success, left_chrom, left_start, left_end, right_chrom, right_start, right_end
    
    def bnd2query(vcf_record):
        success=False
        # try and parse interval from the ALT column
        alt_string = vcf_record.ALT[0]
        if "]" in alt_string:
            chrom_b = alt_string.split("]")[1].split(":")[0]
            position_b = alt_string.split(":")[1].split("]")[0]
        elif "[" in alt_string:
            chrom_b = alt_string.split("[")[1].split(":")[0]
            position_b = alt_string.split(":")[1].split("[")[0]
        else:
            print("# skipping BND variant '{vcf_record.ID}', unable to parse data from alt string")
            return success, None, None, None, None, None, None
        chrom_b = clean_chromosome(chrom_b)
        chrom_a = vcf_record.CHROM
        chrom_a = clean_chromosome(chrom_a)
        position_a = vcf_record.POS
        left_chrom, left_start, left_end, right_chrom, right_start, right_end = compare_intervals(
            chrom_a, position_a, position_a, chrom_b, position_b, position_b
        )
        # we do not use CI
        success = True
        return success, left_chrom, left_start, left_end, right_chrom, right_start, right_end

        

        
        
    vcf = VCF(path_vcf)
    n=0
    n_skipped=0
    with open(path_out, 'w') as f:
        if out_header:
            f.write("ID\tLEFT_CHROM\tLEFT_START\tLEFT_END\tRIGHT_CHROM\tRIGHT_START\tRIGHT_END\tSVTYPE\n")
        for i, variant in enumerate(vcf):
            n+=1
            id = variant.ID if variant.ID is not None else f"{id_fill_prefix}{i}"
            ### svtype
            svtype = variant.INFO.get('SVTYPE')
            if svtype in {"DEL", "DUP", "INV"}:
                success, left_chrom, left_start, left_end, right_chrom, right_start, right_end = sv2query(variant)
            elif svtype == "INS":
                success, left_chrom, left_start, left_end, right_chrom, right_start, right_end = ins2query(variant)
            elif svtype == "BND":
                success, left_chrom, left_start, left_end, right_chrom, right_start, right_end = bnd2query(variant)
            else:
                print(f"# skipping SV '{id}' with unsupported SVTYPE:", svtype)
                skipped_svs.append(id)
                n_skipped+=1
                continue
            if not success:
                print(f"# unsuccessfully converted SV '{id}' to STIX query")
                skipped_svs.append(id)
                n_skipped+=1
                continue
            f.write(f"{id}\t{left_chrom}\t{left_start}\t{left_end}\t{right_chrom}\t{right_start}\t{right_end}\t{svtype}\n")
    print(f"# total SVs: {n}")
    print(f"# skipped SVs: {n_skipped}")
    print(f"# wrote stix queries to {path_out}")
                    
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