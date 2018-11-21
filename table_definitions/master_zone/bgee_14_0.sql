CREATE TABLE IF NOT EXISTS master.bgee_14_0 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.bgee_14_0 ORDER BY molecule_id, tissue_bto_id;