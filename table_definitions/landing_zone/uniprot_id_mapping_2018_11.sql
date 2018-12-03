CREATE TABLE IF NOT EXISTS landing.uniprot_id_mapping_2018_11 (
   from_id_type  VARCHAR,
   to_id_type  VARCHAR,
   from_id VARCHAR,
   to_id VARCHAR,
   tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 's3a://sherlock-korcsmaros-group/landing_zone/uniprot_id_mapping_2018_11' );

-- don't forget to refresh the partition list!