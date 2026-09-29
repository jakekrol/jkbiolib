# starfusion

Example cancer cell line data from Cancer Cell Line Encyclopedia

K562 cell line
- https://zenodo.org/records/13363154/files/SRR521460_1.fastq.20M.fq.gz?download=1
- https://zenodo.org/records/13363154/files/SRR521460_2.fastq.20M.fq.gz?download=1

Do not use -J mode. Instead, call fusions on fastq directly
```
# download the genome lib dir (33GB)
# url: https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/GRCh37_gencode_v19_CTAT_lib_Mar012021.STAR_v2.7.11a.plug-n-play.tar.gz
GENOME_LIB_DIR="<path_to_genome_lib_dir>"
STAR-Fusion --genome_lib_dir $GENOME_LIB_DIR \
			--left_fq read_1.fastq \
			--right_fq read_2.fastq \
			--output_dir star_fusion_outdir
```

# fusioninspector

this never ran successfully. received many errors when installed through bioconda
```
# fusions txt has lines of "geneA--geneB"
FusionInspector --fusions fusions.listA.txt \
                --genome_lib /path/to/CTAT_genome_lib \
                --left_fq rnaseq_1.fq --right_fq rnaseq_2.fq \
                --output_dir my_FusionInspector_outdir \
                --out_prefix finspector \
                --vis
```

# fusionannotator

```
# --annotate is a tsv with a column having "geneA--geneB" strings
# --fusion_name_col is 0-indexed column index for fusions
# --genome_lib_dir is the either https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/GRCh37_gencode_v19_CTAT_lib_Mar012021.STAR_v2.7.11a.plug-n-play.tar.gz or https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/GRCh37_gencode_v19_CTAT_lib_Mar012021.plug-n-play.tar.gz. i do not remember which. probably the former
FusionAnnotator --genome_lib_dir $GENOME_LIB_DIR \
    --fusion_name_col 0 \
    --annotate $tmp \
    > <outfile>
```