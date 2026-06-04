#!/usr/bin/env bash


url_1000g_vcf='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/integrated_sv_map/ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz'
tabix -fh \
	"$url_1000g_vcf" \
	22:1-17000000 | \
	bgzip -c > genotypes.vcf.gz
tabix -p vcf genotypes.vcf.gz

