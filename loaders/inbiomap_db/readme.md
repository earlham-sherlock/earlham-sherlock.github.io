# InBioMap Database Loader script

**Description:**

This script takes an InBioMap database file, which contains protein-protein
interactions and converts it to Sherlock compatible JSON format.

The downloaded database file does not contain some of the parameters below!
Because of this, the user have to identify these parameters!


**Parameters:**

-i, --input-file <path>                                       : path to an existing HINT db file [mandatory]

-int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A, default: uniprotac [optional]

-int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B, default: uniprotac [optional]

-int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

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

1) The InBioMap database does not include the mi identifiers of the interaction types!
2) The interaction type is not in the database file, so we defined it according to the published paper of the database!
It was 0915, physical association!
3) The pubmed ID of the published paper for the InBioMap database is 27892958!
4) We have to identify just the tax ID of interactor A, because the script make the output folder with this parameter!
The tax id of interactor B is identified from the database file!


**Example**

Input example file
```
uniprotkb:A0A5B9	uniprotkb:P01892	uniprotkb:TRBC2_HUMAN	uniprotkb:1A02_HUMAN|ensembl:ENSG00000227715|ensembl:ENSG00000235657|ensembl:ENST00000457879|ensembl:ENST00000547271|ensembl:ENST00000547522|ensembl:ENSP00000403575|ensembl:ENSP00000447962|ensembl:ENSP00000448077	uniprotkb:TRBC2(gene name)|uniprotkb:TRBC2(display_short)	uniprotkb:HLA-A(gene name)|uniprotkb:HLA-A(display_short)	psi-mi:"MI:0045"(experimental interaction detection)	-	-	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	-	psi-mi:"MI:0461"(interaction database)	-	0.417|0.458	-
uniprotkb:A0AUZ9	uniprotkb:Q96CV9	uniprotkb:KAL1L_HUMAN|ensembl:ENSG00000144445|ensembl:ENST00000281772|ensembl:ENST00000418791|ensembl:ENST00000452086|ensembl:ENST00000457374|ensembl:ENSP00000281772|ensembl:ENSP00000393432|ensembl:ENSP00000401408|ensembl:ENSP00000405724	uniprotkb:OPTN_HUMAN|ensembl:ENSG00000123240|ensembl:ENST00000263036|ensembl:ENST00000378747|ensembl:ENST00000378748|ensembl:ENST00000378752|ensembl:ENST00000378757|ensembl:ENST00000378764|ensembl:ENSP00000263036|ensembl:ENSP00000368021|ensembl:ENSP00000368022|ensembl:ENSP00000368027|ensembl:ENSP00000368032|ensembl:ENSP00000368040	uniprotkb:KANSL1L(gene name)|uniprotkb:KANSL1L(display_short)	uniprotkb:OPTN(gene name)|uniprotkb:OPTN(display_short)	psi-mi:"MI:0045"(experimental interaction detection)	-	-	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	-	psi-mi:"MI:0461"(interaction database)	-	0.155|0.0761	-
uniprotkb:A0AV02	uniprotkb:P24941	uniprotkb:S12A8_HUMAN|ensembl:ENSG00000221955|ensembl:ENST00000393469|ensembl:ENST00000430155|ensembl:ENST00000469902|ensembl:ENSP00000377112|ensembl:ENSP00000415713|ensembl:ENSP00000418783	uniprotkb:CDK2_HUMAN|ensembl:ENSG00000123374|ensembl:ENST00000266970|ensembl:ENST00000354056|ensembl:ENSP00000243067|ensembl:ENSP00000266970	uniprotkb:SLC12A8(gene name)|uniprotkb:SLC12A8(display_short)	uniprotkb:CDK2(gene name)|uniprotkb:CDK2(display_short)	psi-mi:"MI:0362"(inference)	-	-	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	-	psi-mi:"MI:0461"(interaction database)	-	0.156|0.0783	-
```

Terminal command:
`python3 inbiomap_db_loader.py -i example_files/core.psimitab -int_a_tax_id 9606 -int_type_id 0915 -pmid 27892958`

The output will be:
- output file: interactor_a_tax_id=9606/inbiomap_db.json
```
{"interactor_a_id": "a0a5b9", "interactor_b_id": "p01892", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [45], "interaction_types_mi_id": [915], "source_database_mi_id": [461], "pmids": [27892958]}
{"interactor_a_id": "a0auz9", "interactor_b_id": "q96cv9", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [45], "interaction_types_mi_id": [915], "source_database_mi_id": [461], "pmids": [27892958]}
{"interactor_a_id": "a0av02", "interactor_b_id": "p24941", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [362], "interaction_types_mi_id": [915], "source_database_mi_id": [461], "pmids": [27892958]}
```
