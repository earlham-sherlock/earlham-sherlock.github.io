CREATE TABLE IF NOT EXISTS landing.dbsnp_2019_06_26 (
   location INT,
   snp_id VARCHAR,
   reference VARCHAR,
   alt VARCHAR,
   chr VARCHAR
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['chr'],
   external_location = 's3a://sherlock/landing_zone/dbsnp_2019_06_26');

-- don't forget to refresh the partition list!