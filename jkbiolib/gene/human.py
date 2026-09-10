import requests

def gene2region(gene: str):
    # grch37 support only
    url="https://grch37.rest.ensembl.org/lookup/symbol/homo_sapiens"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"symbols": [gene]}, # symbol here means gene name
    )
    try:
        data = response.json()
        data = data[gene]
        chrom = data['seq_region_name']
        start = data['start']
        end = data['end']
        strand = data['strand']
        return chrom, start, end, strand
    except:
        return False, False, False, False
    