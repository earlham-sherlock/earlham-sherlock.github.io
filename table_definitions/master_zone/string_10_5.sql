CREATE TABLE master.string_10_5 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.string_10_5 ORDER BY interactor_a_id, interactor_b_id;