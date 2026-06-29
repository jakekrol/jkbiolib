# fastq examples


Downsample fastq to 100k reads
```
# https://onestopdataanalysis.com/subsample-paired-fastq-fasta/
# FASTQ R1
seqtk sample -s 123 read1.fq 100000 > sub_read1.fq
 
# FASTQ R2
seqtk sample -s 123 read2.fq 100000 > sub_read2.fq
```