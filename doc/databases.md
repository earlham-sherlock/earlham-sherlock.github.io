[back to the main page](../readme.md)


# Tables defined in the master zone in Presto

## Molecular interactions

**IntAct**

- Tables (versions): `intact_2018_10_04`
- url: https://www.ebi.ac.uk/intact/
- encoding: ORC
- partitioning: `interactor_a_tax_id`
- ordering: `interactor_a_id`, `interactor_b_id`
- raw data downloaded from: ftp://ftp.ebi.ac.uk/pub/databases/intact/2018-10-04/psimitab/intact-micluster.txt


**Omnipath**

- Tables (versions): `omnipath_??VERSION??`  **TODO**
- url: **TODO**
- encoding: ORC
- partitioning: `interactor_a_tax_id`
- ordering: `interactor_a_id`, `interactor_b_id`
- raw data downloaded from: **TODO**


## ID Mapping

**Uniprot ID mapping**

- Tables (versions): `uniprot_id_mapping_2018_09`
- url: **TODO**
- encoding: ORC
- partitioning: `tax_id`, `from_id_type`, `to_id_type`
- ordering: `from_id`, `to_id`
- raw data downloaded from: **TODO**


## Genomes

**Human Reference Genome 38**

- Tables (versions): `hg_38`
- url: https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/
- encoding: ORC
- partitioning: `chr`
- ordering: `start`
- raw data downloaded from:  http://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/


## Gene expression database

**Bgee**

- Tables (versions): `bgee_14_0`
- url: https://bgee.org
- encoding: ORC
- partitioning: `tax_id`
- ordering: `molecule_id` `tissue_uberon_id`
- raw data downloaded from: ftp://ftp.bgee.org/bgee_v14_0/


