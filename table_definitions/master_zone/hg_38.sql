CREATE TABLE IF NOT EXISTS master.hg_38 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['chr']
) AS SELECT * FROM landing.hg_38 ORDER BY start;
