# Loading Interaction data to sherlock


**STEP 1: store raw files**
copy raw database uniprot files to S3, like:
- `s3://sherlock/raw_zone/uniprot_id_mapping_2018_11/...`

---

**STEP 2: convert to json**

Generate and copy json files to landing zone, partitioned by tax_id, like:
`s3://sherlock/landing_zone/uniprot_id_mapping_2018_11/tax_id=9606/mapping.json`
(the name of the file is arbitrary, presto will read all the files from the directory when it queries the partition)

And in the json we have single json records per line.
Here is an example for one json record (where we put each attribute in separate line for readability, but in the real 
json this is a single line, and the lines are separated by only a new-line character, and no comma).

```
{
   "from_id_type": "ensembl",
   "from_id": "ensg11867234247",
   "to_id_type": "uniprotac",
   "to_id": "q05193",
}
```

Note: you don't need to add the `tax_id` attribute here, as it is already coded to the folder name where the json is placed.

Use the following syntax when crating the values for each attribute:
- from_id: lowercase trimmed string, mandatory
- to_id: lowercase trimmed string, mandatory
- from_id_type: UniProtKB DBref, mandatory
- to_id_type: UniProtKB DBref, mandatory
- tax_id: NCBI TaxID int, mandatory

---

**STEP 3: register landing tables in Presto**

We need to register a table in the landing zone:

```
CREATE TABLE landing.uniprot_id_mapping_2018_11 (
   from_id_type  VARCHAR,
   to_id_type  VARCHAR,
   from_id VARCHAR,
   to_id VARCHAR,
   tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 's3a://sherlock/landing_zone/uniprot_id_mapping_2018_11' );
```

---

**STEP 4:  use hive CLI to refresh the partition list**  

```
msck repair table landing.uniprot_id_mapping_2018_11;
```

---

**STEP 5: convert to ORC in the master zone (+ finer partitioning & total ordering)**

```
CREATE TABLE master.uniprot_id_mapping_2018_11 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id', 'from_id_type']
) AS SELECT from_id, to_id, to_id_type, tax_id, from_id_type FROM landing.uniprot_id_mapping_2018_11 ORDER BY to_id_type, from_id, to_id;

```

In the end we will have the master interaction files in the data lake, like:
`s3://sherlock/master_zone/uniprot_id_mapping_2018_11/tax_id=9606/from_id_type=uniprotac/something.orc`

---
© 2018, 2019 Earlham Institute ([License](../license.md))