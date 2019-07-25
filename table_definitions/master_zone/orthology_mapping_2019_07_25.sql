CREATE TABLE IF NOT EXISTS master.orthology_mapping_2019_07_25   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['from_tax_id']
) AS SELECT * FROM landing.orthology_mapping_2019_07_25   ORDER BY from_id;