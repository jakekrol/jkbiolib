def compare_intervals(a_chrom, a_left, a_right, b_chrom, b_left, b_right):
    if a_chrom < b_chrom:
        return a_chrom, a_left, a_right, b_chrom, b_left, b_right

    if a_chrom > b_chrom:
        return b_chrom, b_left, b_right, a_chrom, a_left, a_right

    # chromosomes are tied
    if a_left < b_left:
        return a_chrom, a_left, a_right, b_chrom, b_left, b_right

    if a_left > b_left:
        return b_chrom, b_left, b_right, a_chrom, a_left, a_right

    # chromosomes and starts are tied
    if a_right <= b_right:
        return a_chrom, a_left, a_right, b_chrom, b_left, b_right

    return b_chrom, b_left, b_right, a_chrom, a_left, a_right

    