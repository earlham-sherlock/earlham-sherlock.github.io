CREATE TABLE IF NOT EXISTS landing.uberon_gene_ontology_2019_07_08 (
   id VARCHAR,
   name VARCHAR,
   alt_ids ARRAY<VARCHAR>,
   direct_parents ARRAY<VARCHAR>,
   direct_children ARRAY<VARCHAR>,
   all_parents ARRAY<VARCHAR>,
   all_children ARRAY<VARCHAR>
) WITH (
   format            = 'JSON',
   external_location = 's3a://sherlock/landing_zone/uberon_gene_ontology_2019_07_08');

-- don't forget to refresh the partition list!
