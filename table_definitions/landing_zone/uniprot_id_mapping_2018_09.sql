CREATE TABLE landing.uniprot_id_mapping_2018_09 (
   tax_id  INT NOT NULL,
   from_id_type  VARCHAR(25) NOT NULL,
   to_id_type  VARCHAR(25) NOT NULL,
   from_id VARCHAR(64) NOT NULL,
   to_id VARCHAR(64) NOT NULL
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['tax_id'],
   external_location = 'S3://sherlock-korcsmaros-group/landing_zone/uniprot_id_mapping_2018_09' );