# BioPlex Database Loader script

**Description:**

This script takes a HINT database file, which contains protein-protein
interactions and converts it to Sherlock compatible JSON format.

The downloaded database file does not contain some of the parameters below!
Because of this, the user have to identify these parameters, if it needed!


**Parameters:**

-i, --input-file <path>                                       : path to an existing HINT db file [mandatory]

-int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A, default: uniprotac [optional]

-int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B, default: uniprotac [optional]

-int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

-int_b_tax_id, --interactor-b-tax-id <int>                    : taxonomy ID of interactor B [mandatory]

-int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A, default: 326 [optional]

-int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A, default: protein [optional]

-int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B, default: 326 [optional]

-int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B, default: protein [optional]

-int_det_m, --interaction-detection-method <int>              : comma separated list of the detection methods of the interaction [optional]

-int_type_id, --interaction-type-mi-id <int>                  : comma separated list of MI IDs of the interaction type [optional]

-db, --source-db-mi-id <int>                                  : comma separated list of MI IDs of the database sources [optional]

-pmid, --pubmed-id <int>                                      : comma separated list of pubmed IDs of the paper [optional]


**Exit codes**

Exit code 1: The specified input file does not exists!


**Notes**

1) The BioPlex database does not include the mi identifiers of the interaction types, interaction detection methods!
2) The interaction type is not in the database file, so we defined it according to the highest MI id in this category! It was 0001!
3) The interaction detection method is not in the database file, so we defined it according to the highest MI id in this category! It was 0190!
4) BioPlex database has not an Uniprot Ref identifier!
5) The pubmed ID of the published paper for the BioPlex database is 28514442!
6) Tha BioPlex database has only interactions from human data!


**Example**

Input example file
```
GeneA	GeneB	UniprotA	UniprotB	SymbolA	SymbolB	p(Wrong)	p(No Interaction)	p(Interaction)
100	728378	P00813	A5A3E0	ADA	POTEF	2.38085788908859e-9	0.000331855941652957	0.999668141677489
100	345651	P00813	Q562R1	ADA	ACTBL2	9.78643725788521e-18	0.211914436568748	0.788085563431252
222389	708	Q8N7W2	Q07021	BEND7	C1QBP	2.96221526059856e-17	0.00564451180569955	0.994355488194301
```

Terminal command:
`python3 bioplex_db_loader.py -i example_files/test.tsv -int_a_tax_id 9606 -int_b_tax_id 9606`

The output will be:
- output file: interactor_a_tax_id=9606/bioplex_db.json
```
{"interactor_a_id": "p00813", "interactor_b_id": "a5a3e0", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "p_wrong_score": 2.38085788908859e-09, "p_no_interaction_score": 0.000331855941652957, "p_interaction_score": 0.999668141677489, "interaction_detection_methods_mi_id": [1], "interaction_types_mi_id": [190], "source_database_mi_id": [], "pmids": [28514442]}
{"interactor_a_id": "p00813", "interactor_b_id": "q562r1", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "p_wrong_score": 9.78643725788521e-18, "p_no_interaction_score": 0.211914436568748, "p_interaction_score": 0.788085563431252, "interaction_detection_methods_mi_id": [1], "interaction_types_mi_id": [190], "source_database_mi_id": [], "pmids": [28514442]}
{"interactor_a_id": "q8n7w2", "interactor_b_id": "q07021", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "p_wrong_score": 2.96221526059856e-17, "p_no_interaction_score": 0.00564451180569955, "p_interaction_score": 0.994355488194301, "interaction_detection_methods_mi_id": [1], "interaction_types_mi_id": [190], "source_database_mi_id": [], "pmids": [28514442]}
```
