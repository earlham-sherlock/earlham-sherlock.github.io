CREATE TABLE IF NOT EXISTS landing.go_annotations_2019_07_04 (
   id VARCHAR,
   id_type VARCHAR,
   go_id VARCHAR,
   evidence VARCHAR,
   tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 's3a://sherlock/landing_zone/go_annotations_2019_07_04');

-- don't forget to refresh the partition list!