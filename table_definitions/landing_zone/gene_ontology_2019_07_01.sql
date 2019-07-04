CREATE TABLE IF NOT EXISTS landing.gene_ontology_2019_07_01 (
   id VARCHAR,
   id_type VARCHAR,
   name VARCHAR,
   namespace VARCHAR,
   alt_ids ARRAY<VARCHAR>,
   direct_parents ARRAY<VARCHAR>,
   direct_children ARRAY<VARCHAR>,
   all_parents ARRAY<VARCHAR>,
   all_children ARRAY<VARCHAR>
) WITH (
   format            = 'JSON',
   external_location = 's3a://sherlock/landing_zone/gene_ontology_2019_07_01');

-- don't forget to refresh the partition list!
