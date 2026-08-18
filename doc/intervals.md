# stix

```
# query vcf mode sharded
# <shardfile>: path to 2-column tsv. col 1 is giggle index path (dir) and col 2 is stix index path (.db)
# <min_reads>: positive integer of minimum supporting reads for sample to be counted
# <slop>: non-negative integer of padding around the left and right interval queries (typically, we use slop=500)
stix -B shardfile.txt -s <slop> -f <vcf> -T <min_reads> > $outfile
```

# giggle

```
# index (create db)
# <s>: indicatest the bedpe files are pre-sorted
giggle index -s -i "beds/*.gz" -o liver_sort_b -f
```

# bed

sorting for giggle/stix
```
# column 1 sort lexicographic
# columns 2 and 3 sort numeric
sort --buffer-size 3G -k1,1 -k2,2n -k3,3n 
```
