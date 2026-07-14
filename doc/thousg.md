# 1000 Genomes


## RNA-seq

hg00100 mage rna-seq, paired-end

``` python
host='ftp.sra.ebi.ac.uk'
remote_file='/vol1/fastq/SRR197/065/SRR19762765/SRR19762765_2.fastq.gz'
local_file='hg00100.mage.rna.fastq2.gz'
start_byte=0
bytes_to_get=int(1e6)
download_ftp_chunk(host,remote_file, local_file,start_byte,bytes_to_get)
```
