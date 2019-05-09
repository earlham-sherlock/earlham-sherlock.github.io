# Loading Interaction data to sherlock


###STEP 1: store raw files
copy raw database files to S3 for each database, like:
- `s3://sherlock-korcsmaros-group/raw_zone/intact_2018_10_04`
- `s3://sherlock-korcsmaros-group/raw_zone/string_10_5`

---

###STEP 2: convert to json

Generate and copy json files to landing zone, partitioned by interactor_a_tax_id, like:
`s3://sherlock-korcsmaros-group/landing_zone/intact_2018_10_04/interactor_a_tax_id=9606/intact.json`
(the name of the file is arbitrary, presto will read all the files from the directory when it queries the partition)

And in the json we have single json records per line.
Here is an example for one json record (where we put each attribute in separate line for readability, but in the real json this is a single
line, and the lines are separated by only a new-line character, and no comma).

```
{
   "interactor_a_id": "ensg11867234247",
   "interactor_b_id": "ensg98236453842",
   "interactor_a_id_type": "Ensembl",
   "interactor_b_id_type": "Ensembl",
   "interactor_b_tax_id": 9606,
   "interactor_a_molecula_type_mi_id": 250,
   "interactor_b_molecula_type_mi_id": 250,
   "interactor_a_molecula_type_name": gene,
   "interactor_b_molecula_type_name": gene,
   "interaction_detection_methods_mi_id": [401, 58],
   "interaction_types_mi_id": [208],
   "source_databases_mi_id": [469],
   "pmids": [14847410, 9368760]
}
```

Note: you don't need to add `interactor_a_tax_id` attribute here, as it is already coded to the folder name where the json is placed.

Use the following syntax when crating the values for each attribute:
- interactor_a_id: lowercase trimmed string, mandatory
- interactor_b_id: lowercase trimmed string, mandatory
- interactor_a_id_type: UniProtKB DBref, mandatory
- interactor_b_id_type: UniProtKB DBref, mandatory
- interactor_a_tax_id: NCBI TaxID int, mandatory
- interactor_b_tax_id: NCBI TaxID int, mandatory
- interactor_a_molecula_type_mi_id: mi_id int, mandatory
- interactor_b_molecula_type_mi_id: mi_id int, mandatory
- interactor_a_molecula_type_name: lowercase trimmed string (mi term name), mandatory
- interactor_b_molecula_type_name: lowercase trimmed string (mi term name), mandatory
- interaction_detection_methods_mi_id: [mi_id int, ...], optional, default: empty list
- interaction_types_mi_id: [mi_id int, ...], optional, default: empty list
- source_databases_mi_id: [mi_id int, ...], optional, default: empty list
- pmids: [ pmid int, ...], optional, default: empty list


---

###STEP 3: register landing tables in Presto:

For each molecular interaction database we need to register a table in the landing zone:

```
CREATE TABLE landing.intact_2018_10_04 (
   interactor_a_id VARCHAR(64) NOT NULL,
   interactor_b_id VARCHAR(64) NOT NULL,
   interactor_a_id_type VARCHAR(25) NOT NULL,
   interactor_b_id_type VARCHAR(25) NOT NULL,
   interactor_a_tax_id INT NOT NULL,
   interactor_b_tax_id INT NOT NULL,
   interactor_a_molecula_type_mi_id INT NOT NULL,
   interactor_b_molecula_type_mi_id INT NOT NULL,
   interactor_a_molecula_type_name VARCHAR(25) NOT NULL,
   interactor_b_molecula_type_name VARCHAR(25) NOT NULL,
   interaction_detection_methods_mi_id ARRAY<INT> NOT NULL,
   interaction_types_mi_id ARRAY<INT> NOT NULL,
   source_databases_mi_id ARRAY<INT> NOT NULL,
   pmids ARRAY<INT>  NOT NULL
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['interactor_a_tax_id'],
   external_location = 'S3://sherlock-korcsmaros-group/landing_zone/intact_2018_10_04' );
```

---

###STEP 4: convert to ORC in the master zone (+ finer partitioning & total ordering):

```
CREATE TABLE master.intact_2018_10_04 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.intact_2018_10_04 ORDER BY interactor_a_id, interactor_b_id;
```

In the end we will have the master interaction files in the data lake, like:
`s3://sherlock-korcsmaros-group/master_zone/intact_2018_10_04/interactor_a_tax_id=9606/something.orc`
