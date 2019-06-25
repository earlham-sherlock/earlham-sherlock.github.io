CREATE TABLE IF NOT EXISTS landing.bgee_14_0 (
   molecule_id VARCHAR,
   molecule_id_type VARCHAR,
   tissue_uberon_id INT,
   tissue_uberon_name VARCHAR,
   source_db VARCHAR,
   score DECIMAL(18, 8),
   tax_id INT
) WITH (
   format            = ''JSON'',
   partitioned_by    = ARRAY[''tax_id''],
   external_location = ''s3a://sherlock/landing_zone/bgee_14_0'' );

-- don't forget to refresh the partition list!

CREATE TABLE IF NOT EXISTS landing.bgee_14_0_limit_200M WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id'] )
AS SELECT * FROM landing.bgee_14_0 LIMIT 200000000;

CREATE TABLE IF NOT EXISTS landing.bgee_14_0_limit_200M_score_above_1000 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id'] )
AS SELECT * FROM landing.bgee_14_0_limit_200M WHERE score > 1000;
