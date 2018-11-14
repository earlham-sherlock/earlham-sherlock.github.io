CREATE TABLE master.hpa_18 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.hpa_18 ORDER BY molecule_id, tissue_bto_id;