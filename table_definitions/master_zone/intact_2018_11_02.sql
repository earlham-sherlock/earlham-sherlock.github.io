CREATE TABLE IF NOT EXISTS master.intact_2018_11_02 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.intact_2018_11_02 ORDER BY interactor_a_id, interactor_b_id;