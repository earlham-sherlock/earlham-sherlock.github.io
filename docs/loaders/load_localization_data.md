# Loading localization data to sherlock

**STEP 1: store raw files**

copy raw tissue database files to S3 for each database.
E.g. for Human Protein Atlas v18, upload it to: `s3://sherlock/raw_zone/hpa_18`

---

**STEP 2: convert to json**

Generate and copy json files to landing zone, like:
`s3://sherlock/landing_zone/hpa_18/tax_id=9606/tissue.json`
(the name of the file is arbitrary, presto will read all the files from the directory when it queries the partition)

And in the json we have single json records per line. The lines are separated by only a new-line character, and no comma).
Note: you don't need to add `tax_id` attribute here, as it is already coded to the folder name where the json is placed.
Where we don't have `score` value, we simply skip the attribute.

```
{ "molecule_id": "ensg11867234247", "molecule_id_type": "Ensembl", "tissue_bto_id": 142, "tissue_bto_name": "brain", "source_db": "HPA", "score": 0.576 }
{ "molecule_id": "ensg11867234247", "molecule_id_type": "Ensembl", "tissue_bto_id": 476, "tissue_bto_name": "foot",  "source_db": "HPA" }
{ "molecule_id": "ensg23829324243", "molecule_id_type": "Ensembl", "tissue_bto_id": 142, "tissue_bto_name": "brain", "source_db": "HPA", "score": 0.983 }
```

Use the following syntax when crating the values for each attribute:
- molecule_id: lowercase trimmed string, mandatory
- molecule_id_type: UniProtKB DBref, mandatory
- tissue_bto_id: BRENDA tissue ID, mandatory
- tissue_bto_name: BRENDA tissue term name, mandatory
- source_db: UniProtKB DBref - if the source db is present in UniProtKB DBref, otherwise just put the database name, mandatory
- score: float value between 0 and 1, optional (just skip the attribute if it is not present)

[This is](https://github.com/NetBiol/sherlock/tree/master/loaders/bgee) our script that makes the database conversion.

---

**STEP 3: register landing tables in Presto**

For each molecular interaction database we need to register a table in the landing zone:

```
CREATE TABLE landing.hpa_18 (
   molecule_id VARCHAR(64) NOT NULL,
   molecule_id_type VARCHAR(25) NOT NULL,
   tax_id INT NOT NULL,
   tissue_bto_id INT NOT NULL,
   tissue_bto_name VARCHAR(64) NOT NULL,
   source_db VARCHAR(25) NOT NULL,
   score DECIMAL(18, 8)
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 'S3://sherlock/landing_zone/hpa_18' );
```

---

**STEP 4:  use hive CLI to refresh the partition list**  

```
msck repair table landing.hpa_18;
```

---

**STEP 5: convert to ORC in the master zone (+ finer partitioning & total ordering)**

```
CREATE TABLE master.hpa_18 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.hpa_18 ORDER BY molecule_id, tissue_bto_id;
```

In the end we will have the master interaction files in the data lake, like:
`s3://sherlock/master_zone/hpa_18/tax_id=9606/something.orc`

---
© 2018, 2019 Earlham Institute ([License](../license.md))