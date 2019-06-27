CREATE TABLE IF NOT EXISTS master.dbsnp_2019_06_26 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['chr']
) AS SELECT * FROM landing.dbsnp_2019_06_26 ORDER BY location;
