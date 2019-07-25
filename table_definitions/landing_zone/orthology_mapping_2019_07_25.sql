CREATE TABLE IF NOT EXISTS landing.orthology_mapping_2019_07_25 (
   to_tax_id INT,
   from_id VARCHAR,
   to_id VARCHAR,
   orthology_type VARCHAR,
   oma_group VARCHAR,
   from_tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['from_tax_id'],
   external_location = 's3a://sherlock/landing_zone/orthology_mapping_2019_07_25');

-- don't forget to refresh the partition list!