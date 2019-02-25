# Genome Annotations Filter script


**Description:**

This script can collect whole genes, exons, introns and micro rnas from a reference annotation .bed file and save that
to an output file, which has single json records. Example:
```
{“entity_type”: "gene", “entity_id_type”: “ensembl", “entity_id": "ensg11867234247", “start”: 12764, “end”: 13264,
   “source_db”: “ucsc“, “genome”: “hg38”}
```
The tool should take the entity_id, start, end, chromosome info from the bed file, the rest of the attributes should be
separate command line parameters. The script make ONE output json file per chromosome.


**Parameters:**

-r, --reference-annotation-bed-file <path>      : path to a reference annotation .bed file [mandatory]

-et, --entity-type <str>                        : MI term name entity type [mandatory]

-eit, --entity-id-type <str>                    : UniProtKB DBref entity id type [mandatory]

-db, --source-db <str>                          : optional text field (can be null, but can not be empty string),
                                                  contains the name version of the database or the experiment ID
                                                  (default = null) [Optional]

-g, --genome <str>                              : genome version [mandatory]

-o, --output-folder <path>                      : path to an output folder [mandatory]


**Exit codes**

Exit code 1: The specified reference annotation .bed file doesn't exists!
Exit code 2: The specified reference annotation file is not a .bed file!
Exit code 3: The specified output folder doesn't exists!
