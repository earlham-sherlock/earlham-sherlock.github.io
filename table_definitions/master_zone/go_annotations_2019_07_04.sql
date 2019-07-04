CREATE TABLE IF NOT EXISTS master.go_annotations_2019_07_04   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.go_annotations_2019_07_04   ORDER BY id;