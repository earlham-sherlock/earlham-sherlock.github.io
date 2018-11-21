CREATE TABLE IF NOT EXISTS landing.hg_38 (
   chr VARCHAR(64) NOT NULL,
   length INT NOT NULL,
   start INT NOT NULL,
   stop INT NOT NULL,
   sequence VARCHAR(1000) NOT NULL,
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['chr'],
   external_location = 'S3://sherlock-korcsmaros-group/landing_zone/hg_38' );
