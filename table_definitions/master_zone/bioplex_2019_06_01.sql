CREATE TABLE IF NOT EXISTS master.bioplex_2019_06_01   WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.bioplex_2019_06_01 ORDER BY interactor_a_id, interactor_b_id;