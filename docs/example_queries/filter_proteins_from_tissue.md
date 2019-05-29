
### Select proteins from a given human tissue

This query only use the Bgee gene expression database, filtering it based on tax id and a given tissue ID.
In the example we use the UBERON ID 955, which is the brain. Please note, the query will retrun only
the proteins which are exactly specified with UBERON ID 955, and will not return the proteins assigned
to a more specific brain tissue.

Here we also use the `LIMIT 10` statement to return only the first 10 results (making the example to
run quicker).

```$sql
SELECT molecule_id, 
       molecule_id_type, 
       tissue_uberon_id, 
       tissue_uberon_name, 
       score
FROM master.bgee_14_0
WHERE tax_id = 9606 AND tissue_uberon_id = 955
LIMIT 10;
```

---
© 2018, 2019 Earlham Institute ([License](../license.md))