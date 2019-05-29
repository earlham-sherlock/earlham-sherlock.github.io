[BACK](../readme.md) to main page

# Loading gene annotation data to sherlock

**STEP 1: store raw files**
copy raw bed files to S3 for each database, like:
- `s3://sherlock/raw_zone/annotations_hg38_gene_intron`
- `s3://sherlock/raw_zone/annotations_hg38_gene_exon`
...

**STEP2: convert to json**

Generate and copy json files to landing zone, partitioned by chromosome, like:
`s3://sherlock/landing_zone/annotations_hg38_gene_intron/chromosome=chr13/intron.json`
(the name of the file is arbitrary, presto will read all the files from the directory when it queries the partition)

And in the json we have single json records per line.
Here is an example for one json record (where we put each attribute in separate line for readability, but in the real json this is a single
line, and the lines are separated by only a new-line character, and no comma).

Note: you don't need to add `chromosome` attribute here, as it is already coded to the folder name where the json is placed.

```
{
   “entity_type”: "gene",
   “entity_id_type”: “ensembl",
   “entity_id": "ensg11867234247",
   “start”: 12764,
   “end”: 13264,
   “source_db”: “ucsc“,
   “genome”: “hg38”,
}
```

Use the following syntax when crating the values for each attribute:
- chromosome: mandatory lowercase trimmed string, starting with 'chr'
- entity_type: MI term name, mandatory
- entity_id_type: UniProtKB DBref, mandatory
- entity_id: lowercase trimmed string, mandatory
- genome: lowercase trimmed string, mandatory
- start: positive integer, mandatory (not necessarily smaller than 'end')
- end: positive integer, mandatory (not necessarily larger than 'end')
- strand: single character ( '+' or '-' ), can be NULL (if there is no strand info in the bed file, or there was a '.') 
- source_db: optional text field (can be null, but can not be empty string), contains the name / version of the database or the experiment ID


[This is](https://github.com/NetBiol/sherlock/tree/master/loaders/hg38_human_annotation_filter) our script that makes 
the annotation file -> json conversion.

---

**STEP 3:  register landing tables in Presto: **

For each annotation file we need to register a table in the landing zone:

```
CREATE TABLE IF NOT EXISTS landing.annotations_hg38_gene_intron (
   entity_type VARCHAR,
   entity_id_type VARCHAR,
   entity_id VARCHAR,
   genome VARCHAR,
   start INT,
   end INT,
   strand VARCHAR,
   source_db VARCHAR,
   chromosome VARCHAR
) WITH (
   format            = ''JSON'',
   partitioned_by    = ARRAY[''chromosome''],
   external_location = ''s3a://sherlock/landing_zone/annotations_hg38_gene_intron'' );

```

---

**STEP 4:  use hive CLI to refresh the partition list**  

```
msck repair table landing.annotations_hg38_gene_intron;
```


---

**STEP 5:  convert to ORC in the master zone (+ total ordering)**

```
CREATE TABLE master.annotations_hg38_gene_intron WITH (
   format = 'ORC',
   partitioned_by = ARRAY['chromosome']
) AS SELECT * FROM landing.annotations_hg38_gene_intron ORDER BY start;
```

In the end we will have the master annotation files in the data lake, like:
`s3://sherlock/master_zone/annotations_hg38_gene_intron/chromosome=chr13/something.orc`

---
© 2018, 2019 Earlham Institute ([License](../sherlock_license.md))