[BACK](../../readme.md) to main page


### Query Intact protein interactions and mapping them to uniprot IDs

This query will select 10 interaction from the `intact` table, then converts them to uniprot, using the 
`uniprot_id_mapping` table. If you need more than 10 interactions, then of course you can add your own 
filtering criteria and delete `LIMIT 10`.

Please note, the ID mapping is not necessarily unambiguous. If there is no uniprot mapping, or there are 
more than one uniprot mapping for the given protein, then it can skip or return with multiple uniprot
interactions for a single original interaction defined in the Intact database.


```$sql
SELECT mapper_a.to_id AS uniprot_a,
       mapper_b.to_id AS uniprot_b
FROM master.intact_2018_10_04 intact
LEFT JOIN master.uniprot_id_mapping_2018_09 mapper_a ON 
             intact.interactor_a_tax_id = mapper_a.tax_id AND
             intact.interactor_a_id = mapper_a.from_id AND
             intact.interactor_a_id_type = mapper_a.from_id_type
LEFT JOIN master.uniprot_id_mapping_2018_09 mapper_b ON 
             intact.interactor_b_tax_id = mapper_b.tax_id AND
             intact.interactor_b_id = mapper_b.from_id AND
             intact.interactor_b_id_type = mapper_b.from_id_type
WHERE mapper_a.to_id_type = "uniprot" AND mapper_b.to_id_type = "uniprot"
LIMIT 10;
```

---
© 2018, 2019 Earlham Institute ([License](../sherlock_license.md))