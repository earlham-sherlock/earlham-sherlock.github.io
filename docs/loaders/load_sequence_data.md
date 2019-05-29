[BACK](../../readme.md) to main page

# Loading gene/protein sequence data to sherlock

**STEP 1: store raw files**

copy raw human genome (hg38p12) files to: `s3://sherlock/raw_zone/hg_38_p12`

---

**STEP 2: convert to json**

Generate and copy json files to landing zone, like:
`s3://sherlock/landing_zone/hg_38_p12/chr=chr11/chromosome.json`

And in the json we have single json records per line, like:

```
{"length": 1000, "start": 123001, "stop": 124000, "sequence": "actg.....ccta"}
{"length": 1000, "start": 124001, "stop": 125000, "sequence": "actg.....ccta"}
{"length": 1000, "start": 125001, "stop": 126000, "sequence": "actg.....ccta"}
{"length": 1000, "start": 126001, "stop": 127000, "sequence": "actg.....ccta"}
{"length": 1000, "start": 127001, "stop": 128000, "sequence": "actg.....ccta"}
```
Note: you don't need to add `chr` attribute here, as it is already coded to the folder name where the json is placed.

Note: you can split the output files into many parts, if they are too large for some reason. The only important thing is to write full son objects (don’t split the file in the middle of the lines) and place all the files for a given chromosome into the same folder. (The file names don’t matter, only the folder name is important.)

Note: use the following syntaxes:
- length: integer, larger than zero
- start: integer, larger than zero, smaller or equal to stop
- stop: integer, larger than zero, larger or equal to start
- sequence: small case string, exactly as long as the length attribute 

[This is](https://github.com/NetBiol/sherlock/tree/master/loaders/hg38_human_genome) our script that makes the fasta -> json conversion.

---

**STEP 3:  register landing table in Presto  **


```
CREATE TABLE landing.hg_38_p12 (
   chr VARCHAR(64) NOT NULL,
   length INT NOT NULL,
   start INT NOT NULL,
   stop INT NOT NULL,
   sequence VARCHAR(1000) NOT NULL,
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['chr'],
   external_location = 'S3://sherlock/landing_zone/hg_38_p12' );
```

---

**STEP 4:  use hive CLI to refresh the partition list**  

```
msck repair table landing.hg_38_p12;
```

---

**STEP 5:  convert to ORC in the master zone (+ finer partitioning & total ordering)**

```
CREATE TABLE master.hg_38_p12 WITH (
   format = 'ORC',
   partitioned_by = ARRAY[′chr′]
) AS SELECT * FROM landing.hg_38_p12 ORDER BY start;
```

In the end we will have the genome files in the data lake, like:
`s3://sherlock/master_zone/hg_38_p12/chr=chr11/chromosome.orc`


---
© 2018, 2019 Earlham Institute ([License](../sherlock_license.md))
