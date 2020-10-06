CREATE TABLE IF NOT EXISTS master.dorothea_2020_10_05   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.dorothea_2020_10_05 ORDER BY interactor_a_id, interactor_b_id;