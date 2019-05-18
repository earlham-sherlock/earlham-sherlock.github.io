# iRefIndex Database Loader script

**Description:**

This script takes an InBioMap database file, which contains protein-protein
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

1) In the iRefIndex database not all of the interaction has interaction type, detection method, source database or pubmed id! We have to identify these parameters if we want!
2) iRefIndex database has an Uniprot Ref identifier, that is 0923!
3) The pubmed ID of the published paper for the iRefIndex database is 18823568!
4) We have to identify just the tax ID of interactor A, because the script make the output folder with this parameter!
The tax id of interactor B is identified from the database file!


**Example**

Input example file
```
#uidA	uidB	altA	altB	aliasA	aliasB	method	author	pmids	taxa	taxb	interactionType	sourcedb	interactionIdentifier	confidence	expansion	biological_role_A	biological_role_B	experimental_role_A	experimental_role_B	interactor_type_A	interactor_type_B	xrefs_A	xrefs_B	xrefs_Interaction	Annotations_A	Annotations_B	Annotations_Interaction	Host_organism_taxid	parameters_Interaction	Creation_date	Update_date	Checksum_A	Checksum_B	Checksum_Interaction	Negative	OriginalReferenceA	OriginalReferenceB	FinalReferenceA	FinalReferenceB	MappingScoreA	MappingScoreB	irogida	irogidb	irigid	crogida	crogidb	crigid	icrogida	icrogidb	icrigid	imex_id	edgetype	numParticipants
uniprotkb:A0A024RB96	uniprotkb:A0A024RA90	entrezgene/locuslink:196403|refseq:NP_001273175|refseq:NP_848597|rogid:Ma7JBhgMdFofCeWESbf8h1iLAHY9606|irogid:3006542	entrezgene/locuslink:51619|refseq:NP_057067|uniprotkb:A0A024RA90|rogid:xc+Dyvh3gHK14B0RxgVqoToxbTI9606|irogid:4831700	hgnc:DTX3|uniprotkb:A0A024RB96_HUMAN|uniprotkb:DTX3_HUMAN|crogid:Ma7JBhgMdFofCeWESbf8h1iLAHY9606|icrogid:3006542	hgnc:UBE2D4|uniprotkb:A0A024RA90_HUMAN|uniprotkb:UB2D4_HUMAN|crogid:xc+Dyvh3gHK14B0RxgVqoToxbTI9606|icrogid:4831700	psi-mi:"MI:0018"(two hybrid)	Markson G (2009)	pubmed:19549727	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	MI:0407(direct interaction)	MI:0463(biogrid)	biogrid:441059|rigid:+4O62gRrUCSHLPbxlq5d/Xm4zU0|edgetype:X	hpr:1149|lpr:1149|np:1	none	MI:0499(unspecified role)	MI:0499(unspecified role)	MI:0498(prey)	MI:0496(bait)	MI:0326(protein)	MI:0326(protein)	-	-	-	-	-	-	taxid:32644(unidentified)	-	2018-01-22	2018-01-22	rogid:Ma7JBhgMdFofCeWESbf8h1iLAHY9606	rogid:xc+Dyvh3gHK14B0RxgVqoToxbTI9606	rigid:+4O62gRrUCSHLPbxlq5d/Xm4zU0	false	refseq:XP_005268760	refseq:NP_057067	refseq:XP_005268760	refseq:NP_057067	P	P	3006542	4831700	617977	Ma7JBhgMdFofCeWESbf8h1iLAHY9606	xc+Dyvh3gHK14B0RxgVqoToxbTI9606	+4O62gRrUCSHLPbxlq5d/Xm4zU0	3006542	4831700	617977	-	X	2
uniprotkb:P40616	uniprotkb:Q9UIL1-2	entrezgene/locuslink:400|refseq:NP_001168|uniprotkb:ARL1_HUMAN|rogid:4sRUSYrH1mt5ol85HlMNSEn1j9M9606|irogid:558453	entrezgene/locuslink:60592|refseq:NP_001146918|refseq:NP_001147057|rogid:J6BwjLyIzafohUuZewMZO3NT8f49606|irogid:32118164	hgnc:ARL1|uniprotkb:ARL1_HUMAN|crogid:4sRUSYrH1mt5ol85HlMNSEn1j9M9606|icrogid:558453	hgnc:SCOC|crogid:l1hHXnWtTNJbZZBNyDtExzt5SSQ9606|icrogid:5395936	psi-mi:"MI:0492"(in vitro)	-	pubmed:11303027	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	-	MI:0468(hprd)	hprd:-|rigid:wGTGILr2tn1jwk4RKkITMG6T12E|edgetype:X	hpr:8|lpr:8|np:1	none	MI:0000(unspecified)	MI:0000(unspecified)	MI:0000(unspecified)	MI:0000(unspecified)	MI:0326(protein)	MI:0326(protein)	-	-	-	-	-	-	-	-	2018-01-22	2018-01-22	rogid:4sRUSYrH1mt5ol85HlMNSEn1j9M9606	rogid:J6BwjLyIzafohUuZewMZO3NT8f49606	rigid:wGTGILr2tn1jwk4RKkITMG6T12E	false	entrezgene:400	entrezgene:60592	refseq:NP_001168	refseq:NP_001146918	STGD+O	STGD+O	558453	32118164	1514720	4sRUSYrH1mt5ol85HlMNSEn1j9M9606	l1hHXnWtTNJbZZBNyDtExzt5SSQ9606	pEOI8NHQpRSHSaiogtQzM4jSoyY	558453	5395936	1758703	-	X	2
uniprotkb:Q9NVH1	refseq:XP_006723867	entrezgene/locuslink:55735|refseq:NP_060668|uniprotkb:Q9NVH1|rogid:+I9CW/QUSn5NIkn2CRTFzq50c/I9606|irogid:37096	refseq:XP_006723867|rogid:XY2wCI5qF5xEvEYXhpWx2cJ24+E9606|irogid:190808543	hgnc:DNAJC11|uniprotkb:DJC11_HUMAN|crogid:+I9CW/QUSn5NIkn2CRTFzq50c/I9606|icrogid:37096	crogid:XY2wCI5qF5xEvEYXhpWx2cJ24+E9606|icrogid:190808543	psi-mi:"MI:0004"(affinity chromatography technology)	Huttlin EL (2015)	pubmed:26186194	taxid:9606(Homo sapiens)	taxid:9606(Homo sapiens)	MI:0915(physical association)	MI:0463(biogrid)	biogrid:1192996|rigid:cvpWdNNtOPN9WvxQvyZ/+mZS+Io|edgetype:X	hpr:23471|lpr:23471|np:1	none	MI:0499(unspecified role)	MI:0499(unspecified role)	MI:0498(prey)	MI:0496(bait)	MI:0326(protein)	MI:0326(protein)	-	-	-	-	-	-	taxid:32644(unidentified)	-	2018-01-22	2018-01-22	rogid:+I9CW/QUSn5NIkn2CRTFzq50c/I9606	rogid:XY2wCI5qF5xEvEYXhpWx2cJ24+E9606	rigid:cvpWdNNtOPN9WvxQvyZ/+mZS+Io	false	refseq:NP_060668	refseq:XP_006723867	refseq:NP_060668	refseq:XP_006723867	P	P	37096	190808543	2278160	+I9CW/QUSn5NIkn2CRTFzq50c/I9606	XY2wCI5qF5xEvEYXhpWx2cJ24+E9606	cvpWdNNtOPN9WvxQvyZ/+mZS+Io	37096	190808543	2278160	-	X	2
```

Terminal command:
`python3 irefindex_db_loader.py -i example_files/9606.mitab.01-22-2018.txt -int_a_id uniprotac -int_b_id uniprotac -int_a_tax_id 9606 -int_a_m_id 0326 -int_b_m_id 0326 -int_a_m_tn protein -int_b_m_tn protein -int_det_m 0001 -int_type_id 0915 -pmid 18823568`

The output will be:
- output file: interactor_a_tax_id=9606/irefindex_db.json
```
{"interactor_a_id": "a0a024rb96", "interactor_b_id": "a0a024ra90", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [18], "interaction_types_mi_id": [407], "source_database_mi_id": [463, 923], "pmids": [19549727, 18823568]}
{"interactor_a_id": "p40616", "interactor_b_id": "q9uil1-2", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [492], "interaction_types_mi_id": [915], "source_database_mi_id": [468, 923], "pmids": [11303027, 18823568]}
{"interactor_a_id": "q9nvh1", "interactor_b_id": "xp_006723867", "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac", "interactor_b_tax_id": 9606, "interactor_a_molecule_type_mi_id": 326, "interactor_b_molecule_type_mi_id": 326, "interactor_a_molecule_type_name": "protein", "interactor_b_molecule_type_name": "protein", "interaction_detection_methods_mi_id": [4], "interaction_types_mi_id": [915], "source_database_mi_id": [463, 923], "pmids": [26186194, 18823568]}
```
