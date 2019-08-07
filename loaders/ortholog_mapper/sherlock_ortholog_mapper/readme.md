# Sherlock Ortholog Mapper Loader script


**Description:**

This script takes a TSV file, which contains protein orthologes
between species and converts it to Sherlock compatible JSON format.


**Parameters:**

-i, --input-file-list <list>          : comma separated paths to existing files [mandatory]

-f, --from-tax-id <int>               : taxonomy identifier of source [mandatory]

-t, --to-tax-ids <list>               : comma separated taxonomy identifiers of targets [mandatory]

-o, --output-folder <path>            : path to an output folder [mandatory]


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: The number of the input files and the number of the to taxonomy IDs must be equal!


**Example:**

Input example file
```
Q8NH21	Q8VF49_MOUSE	n:m
Q8NH21	MOUSE27312	n:m	297630
Q8NH21	F6T8U6_MOUSE	n:m
HUMAN00003	Q8VDD8	n:1	573349
Q6IEY1	A2AVW1_MOUSE	n:1
Q6IEY1	A2AVW1_MOUSE	n:1
A0A087WYW1_HUMAN	Q1RNF8	1:1	898150
```

Terminal command:
`python3 sherlock_ortholog_mapper.py -i example_files/human_to_mouse_orthology.tsv -f 9606 -t 10090 -o orthology_mapping_2019_07_25/`

The output will be:
- output file: from_tax_id=9606/ortholog_mapping.json

```
{"to_tax_id": 10090, "from_id": "q8nh21", "to_id": "mouse27312", "orthology_type": "n:m", "oma_group": 297630}
{"to_tax_id": 10090, "from_id": "human00003", "to_id": "q8vdd8", "orthology_type": "n:1", "oma_group": 573349}
{"to_tax_id": 10090, "from_id": "a0a087wyw1", "to_id": "q1rnf8", "orthology_type": "1:1", "oma_group": 898150}
```