# Mentha Database Loader script

**Description:**

This script takes a Mentha database file, which contains protein-protein
interactions and converts it to Sherlock compatible JSON format.

The downloaded database file does not contain some of the parameters below!
Because of this, the user have to identify these parameters!


**Parameters:**

-i, --input-file <path>                                       : path to an existing HINT db file [mandatory]

-int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A [mandatory]

-int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B [mandatory]

-int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

-int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A [mandatory]

-int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A [mandatory]

-int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B [mandatory]

-int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B [mandatory]

-int_det_m, --interaction-detection-method <int>              : comma separated list of the detection methods of the interaction [optional]

-int_type_id, --interaction-type-mi-id <int>                  : comma separated list of MI IDs of the interaction type [optional]

-db, --source-db-mi-id <int>                                  : comma separated list of MI IDs of the database sources [optional]

-pmid, --pubmed-id <int>                                      : comma separated list of pubmed IDs of the paper [optional]


**Exit codes**

Exit code 1: The specified input file doesn't exists!


**Notes**

1) We have to identify just the tax ID of interactor A, because the script make the output folder with this parameter!
The tax id of interactor B is identified from the database file!
2) Mentha database does not have any Uniprot Ref identifier, that is why, we give an unique id for it, 10001!
3) The pubmed ID of the published paper for the HINT database is 23900247!


**Example**

Input example file
```
uniprotkb:P78527	uniprotkb:Q96BW5	-	-	uniprotkb:PRKDC(gene name)	uniprotkb:PTER(gene name)	psi-mi:"MI:0401"(biochemical)	-	pubmed:22939629	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	psi-mi:"MI:0403"(colocalization)	psi-mi:"MI:0463"(biogrid)	biogrid:752699	mentha-score:0.081
uniprotkb:P78527	uniprotkb:Q99708	-	-	uniprotkb:PRKDC(gene name)	uniprotkb:RBBP8(gene name)	psi-mi:"MI:0686"(unspecified method)	-	pubmed:10608806	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	psi-mi:"MI:0407"(direct interaction)	psi-mi:"MI:0463"(biogrid)	biogrid:245147	mentha-score:0.183
uniprotkb:P78527	uniprotkb:Q99759	-	-	uniprotkb:PRKDC(gene name)	uniprotkb:MAP3K3(gene name)	psi-mi:"MI:0676"(tandem affinity purification)	-	pubmed:14743216	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	psi-mi:"MI:0915"(physical association)	psi-mi:"MI:0469"(IntAct)	intact:EBI-362421	mentha-score:0.126
```

Terminal command:
`python3 mentha_db_loader.py -i example_files/test.tsv -int_a_id uniprotac -int_b_id uniprotac -int_a_tax_id 9606 -int_a_m_id 0326 -int_b_m_id 0326 -int_a_m_tn protein -int_b_m_tn protein -pmid 23900247`

The output will be:
- output file: interactor_a_tax_id=9606/mentha_db.json
```
{"interactor_a_id": "p78527", "interactor_b_id": "q96bw5", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [401], "interaction_types_mi_id": [403], "source_database_mi_id": [10001], "pmids": [22939629, 23900247]}
{"interactor_a_id": "p78527", "interactor_b_id": "q99708", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [686], "interaction_types_mi_id": [407], "source_database_mi_id": [10001], "pmids": [10608806, 23900247]}
{"interactor_a_id": "p78527", "interactor_b_id": "q99759", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [676], "interaction_types_mi_id": [915], "source_database_mi_id": [10001], "pmids": [14743216, 23900247]}
```
