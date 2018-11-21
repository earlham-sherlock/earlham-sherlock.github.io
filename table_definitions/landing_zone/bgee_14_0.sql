CREATE TABLE IF NOT EXISTS landing.bgee_14_0 (
   molecule_id VARCHAR(64) NOT NULL,
   molecule_id_type VARCHAR(25) NOT NULL,
   tax_id INT NOT NULL,
   tissue_bto_id INT NOT NULL,
   tissue_bto_name VARCHAR(64) NOT NULL,
   source_db VARCHAR(25) NOT NULL,
   score DECIMAL(18, 8)
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 'S3://sherlock-korcsmaros-group/landing_zone/bgee_14_0' );