CREATE TABLE IF NOT EXISTS master.hint_2019_05_24   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.hint_2019_05_24   ORDER BY interactor_a_id, interactor_b_id;