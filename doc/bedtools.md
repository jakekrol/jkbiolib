# bedtools

convert a bam to fastq

```
# sort by query name
samtools sort -@ <threads> -n -o <output> <input>
# bamtofastq
bedtools bamtofastq \
    -i <input> \
    -fq <output_read_1> \
    -fq2 <output_read_2>
```


report records overlapping A and B. include the info from both A and B (wa,wb)
```
bedtools intersect \
    -a A.bed -b B.bed -u
```
