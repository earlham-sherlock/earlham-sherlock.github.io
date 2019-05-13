# HINT Database Loader script

**Description:**

This script takes a HINT database file, which contains protein-protein
interactions and converts it to Sherlock compatible JSON format.

The downloaded database file does not contain the parameters below!
Because of this, the user have to identify these mandatory parameters!


**Parameters:**

-i, --input-file <path>                                       : path to an existing HINT db file [mandatory]

-int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A [mandatory]

-int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B [mandatory]

-int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

-int_b_tax_id, --interactor-b-tax-id <int>                    : taxonomy ID of interactor B [mandatory]

-int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A [mandatory]

-int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A [mandatory]

-int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B [mandatory]

-int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B [mandatory]

-int_type_id, --interaction_type_mi_id <int>                  : MI ID of the interaction type [optional]


**Exit codes**

Exit code 1: The specified input file doesn't exists!


**Notes**

1) The HINT database does not include the mi identifiers of the interaction types!


**Example**

Input example file
```
Uniprot_A	Uniprot_B	Gene_A	Gene_B	ORF_A	ORF_B	Alias_A	Alias_B	pmid:method:quality
A0A024QYV7	A0A024QYV7	A0A024QYV7	A0A024QYV7	HCG_1994130	HCG_1994130			14667819:0018:HT
A0A024QYV7	Q01844	A0A024QYV7	EWSR1	HCG_1994130			HGNC:3508	16189514:0398:HT|16189514:0018:HT
A0A024QYV7	Q13838	A0A024QYV7	DDX39B	HCG_1994130			HGNC:13917	14667819:0018:HT
```

Terminal command:
python3 hint_db_loader.py -i example_files/HomoSapiens_binary_hq.txt -int_a_id uniprotac -int_b_id uniprotac -int_a_tax_id 9606 -int_b_tax_id 9606 -int_a_m_id 0326 -int_b_m_id 0326 -int_a_m_tn protein -int_b_m_tn protein

The output will be:
- output file: interactor_a_tax_id=9606/hint_db.json
```
{"interactor_a_id": "a0a024qyv7", "interactor_b_id": "a0a024qyv7", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [18], "interaction_types_mi_id": [], "source_database_mi_id": [10000], "pmids": ["14667819"]}
{"interactor_a_id": "a0a024qyv7", "interactor_b_id": "q01844", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [398, 18], "interaction_types_mi_id": [], "source_database_mi_id": [10000], "pmids": ["16189514", "16189514"]}
{"interactor_a_id": "a0a024qyv7", "interactor_b_id": "q13838", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [18], "interaction_types_mi_id": [], "source_database_mi_id": [10000], "pmids": ["14667819"]}
```
