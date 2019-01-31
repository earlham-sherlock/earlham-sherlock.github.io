CREATE TABLE IF NOT EXISTS landing.hg_38 (
   length INT,
   start INT,
   stop INT,
   sequence VARCHAR,
   chr VARCHAR
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['chr'],
   external_location = 's3a://sherlock-korcsmaros-group/landing_zone/hg_38' );

-- don't forget to refresh the partition list!
