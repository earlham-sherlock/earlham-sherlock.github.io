# String Database Loader script

**Description:**

This script takes a String database file, which contains protein-protein
interactions and converts it to Sherlock compatible JSON format.

The downloaded database file does not contain some of the parameters below!
Because of this, the user have to identify these parameters!


**Parameters:**

-i, --input-file <path>                                       : path to an existing String db file [mandatory]

-int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A, default: ensembl [optional]

-int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B, default: ensembl [optional]

-int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

-int_b_tax_id, --interactor-b-tax-id <int>                    : taxonomy ID of interactor B [mandatory]

-int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A, default: 326 [optional]

-int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A, default: protein [optional]

-int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B, default: 326 [optional]

-int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B, default: protein [optional]

-int_det_m, --interaction-detection-method <int>              : the detection methods of the interaction, default: 0045 [optional]

-int_type_id, --interaction-type-mi-id <int>                  : the MI IDs of the interaction type, default: 0190 [optional]

-db, --source-db-mi-id <int>                                  : the MI ID of the database sources, default: 1014 [optional]

-pmid, --pubmed-id <int>                                      : the pubmed IDs of the paper, default: 30476243 [optional]


**Exit codes**

Exit code 1: The specified input file does not exists!


**Notes**

1) The STRING database has MI ID, which is 1014!
2) The interaction detection method is not in the database file, so we defined it according the highest on the tree of the MI IDs! It was 0045, experimental interaction detection!
2) The interaction type is not in the database file, so we defined it according the highest on the tree of the MI IDs! It was 0190, interaction type!
3) The pubmed ID of the published paper for the String database is 30476243!


**Example**

Input example file
```
protein1 protein2 combined_score
9606.ENSP00000000233 9606.ENSP00000272298 490
9606.ENSP00000000233 9606.ENSP00000253401 198
9606.ENSP00000000233 9606.ENSP00000401445 159
9606.ENSP00000000233 9606.ENSP00000418915 606
9606.ENSP00000000233 9606.ENSP00000327801 167
```

Terminal command:
`python3 string_db_loader.py -i example_files/test.txt -int_a_tax_id 9606 -int_b_tax_id 9606`

The output will be:
- output file: interactor_a_tax_id=9606/string_db.json
```
{"interactor_a_id": "ensp00000000233", "interactor_b_id": "ensp00000272298", "interactor_a_id_type": "ensembl", "interactor_b_id_type": "ensembl", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "combined_score": "490", "interaction_detection_methods_mi_id": 45, "interaction_types_mi_id": 190, "source_database_mi_id": 1014, "pmids": 30476243}
{"interactor_a_id": "ensp00000000233", "interactor_b_id": "ensp00000253401", "interactor_a_id_type": "ensembl", "interactor_b_id_type": "ensembl", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "combined_score": "198", "interaction_detection_methods_mi_id": 45, "interaction_types_mi_id": 190, "source_database_mi_id": 1014, "pmids": 30476243}
{"interactor_a_id": "ensp00000000233", "interactor_b_id": "ensp00000401445", "interactor_a_id_type": "ensembl", "interactor_b_id_type": "ensembl", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "combined_score": "159", "interaction_detection_methods_mi_id": 45, "interaction_types_mi_id": 190, "source_database_mi_id": 1014, "pmids": 30476243}
{"interactor_a_id": "ensp00000000233", "interactor_b_id": "ensp00000418915", "interactor_a_id_type": "ensembl", "interactor_b_id_type": "ensembl", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "combined_score": "606", "interaction_detection_methods_mi_id": 45, "interaction_types_mi_id": 190, "source_database_mi_id": 1014, "pmids": 30476243}
{"interactor_a_id": "ensp00000000233", "interactor_b_id": "ensp00000327801", "interactor_a_id_type": "ensembl", "interactor_b_id_type": "ensembl", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "combined_score": "167", "interaction_detection_methods_mi_id": 45, "interaction_types_mi_id": 190, "source_database_mi_id": 1014, "pmids": 30476243}
```
