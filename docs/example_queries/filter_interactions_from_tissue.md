[BACK](../readme.md) to main page


### Filtering human Intact interactions based on tissue

Here we use the Bgee gene expression database, to filter molecular interactions based on the tissue ID.
In the example we use the UBERON ID 955, which is the brain. Please note, the query will retrun only
the protein interactions where both proteins are exactly specified with UBERON ID 955, and will not 
return any interactions where any protein is assigned to any other tissue, not even the more specific
brain tissues.

In this example we are relying on the fact that both the Human Protein Atlas and both the Intact
database are using the same protein id type. If this would't be the case, then further protein id 
mapping would be needed.

Here we also use the `LIMIT 10` statement to return only the first 10 results (making the example to
run quicker).

```$sql
SELECT intact.interactor_a_id, 
       intact.interactor_b_id, 
       bgee_a.tissue_uberon_id AS tissue_uberon_id, 
       bgee_a.tissue_uberon_name AS tissue_uberon_name, 
       bgee_a.score AS score_a,
       bgee_b.score AS score_b
FROM master.intact_2018_10_04 intact
LEFT JOIN master.bgee_14_0 bgee_a ON 
             intact.interactor_a_tax_id = bgee_a.tax_id AND
             intact.interactor_a_id = bgee_a.molecule_id AND
             intact.interactor_a_id_type = bgee_a.molecule_id_type
LEFT JOIN master.bgee_14_0 bgee_b ON 
             intact.interactor_b_tax_id = bgee_b.tax_id AND
             intact.interactor_b_id = bgee_b.molecule_id AND
             intact.interactor_b_id_type = bgee_b.molecule_id_type
WHERE intact.interactor_a_tax_id = 9606 
  AND intact.interactor_b_tax_id = 9606
  AND bgee_a.tissue_uberon_id = 955
  AND bgee_b.tissue_uberon_id = 955
LIMIT 10;
```

---
© 2018, 2019 Earlham Institute ([License](../sherlock_license.md))