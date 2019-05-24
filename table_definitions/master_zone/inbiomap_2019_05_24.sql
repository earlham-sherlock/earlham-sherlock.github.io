CREATE TABLE IF NOT EXISTS master.inbiomap_2019_05_24   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.inbiomap_2019_05_24   ORDER BY interactor_a_id, interactor_b_id;