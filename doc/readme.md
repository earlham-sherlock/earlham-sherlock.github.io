# Sherlock

Sherlock is a data platform used by EI researchers, collaborators and services developed in the 
KorcsmarosLab.

Features:
* **store** all datasets in a redundant, organized  storage
* **convert** all datasets to common, query compatible file format
* **execute** analytical queries on top of data files
* **share** datasets among different teams / projects
* **generate** operational datasets for certain services or collaborators


## Tables defined in the master zone in Presto


| Table Name                 | Description                                     |
| -------------------------- | ----------------------------------------------- | 
| intact_2018_10_04          | Intact molecule interaction database            | 
| string_10_05               | String molecule interaction database            | 
| uniprot_id_mapping_2018_09 | Id mapping data from Uniprot                    | 
| hpa_18                     | Tissue identifiers from the Human Protein Atlas |


## Example queries
In the following we will show different example queries, relying on the data already loaded into the 
data lake.
 

### Query Intact protein interactions and mapping them to uniprot IDs

This query will select 10 interaction from the `intact` table, then converts them to uniprot, using the 
`uniprot_id_mapping` table. If you need more than 10 interactions, then of course you can add your own 
filtering criteria and delete `LIMIT 10`.

Please note, the ID mapping is not necessarily unambiguous. If there is no uniprot mapping, or there is 
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

### Select proteins from a given human tissue

This query only use the Human Protein Atlas, filtering it based on tax id and a given tissue ID.
In the example we use the BTO ID 142, which is the brain. Please note, the query will retrun only
the proteins which are exactly specified with BTO ID 142, and will not return the proteins assigned
to a more specific brain tissue.

Here we also use the `LIMIT 10` statement to return only the first 10 results (making the example to
run quicker).

```$sql
SELECT molecule_id, 
       molecule_id_type, 
       tissue_bto_id, 
       tissue_bto_name, 
       score
FROM master.hpa_18
WHERE tax_id = 9606 AND tissue_bto_id = 142
LIMIT 10;
```


### Filtering human Intact interactions based on tissue

This query use the Human Protein Atlas, to filter molecular interactions based on the tissue ID.
In the example we use the BTO ID 142, which is the brain. Please note, the query will retrun only
the protein interactions where both proteins are exactly specified with BTO ID 142, and will not 
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
       hpa_a.tissue_bto_id AS tissue_bto_id, 
       hpa_a.tissue_bto_name AS tissue_bto_name, 
       hpa_a.score AS score_a,
       hpa_b.score AS score_b
FROM master.intact_2018_10_04 intact
LEFT JOIN master.hpa_18 hpa_a ON 
             intact.interactor_a_tax_id = hpa_a.tax_id AND
             intact.interactor_a_id = hpa_a.molecule_id AND
             intact.interactor_a_id_type = hpa_a.molecule_id_type
LEFT JOIN master.hpa_18 hpa_b ON 
             intact.interactor_b_tax_id = hpa_b.tax_id AND
             intact.interactor_b_id = hpa_b.molecule_id AND
             intact.interactor_b_id_type = hpa_b.molecule_id_type
WHERE intact.interactor_a_tax_id = 9606 
  AND intact.interactor_b_tax_id = 9606
  AND hpa_a.tissue_bto_id = 142
  AND hpa_b.tissue_bto_id = 142
LIMIT 10;
```


### Enrich protein list with internal interactions

TODO


### Enrich interaction list with first neighbours

TODO

