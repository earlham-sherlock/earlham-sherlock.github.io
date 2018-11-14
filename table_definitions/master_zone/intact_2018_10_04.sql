CREATE TABLE master.intact_2018_10_04 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['interactor_a_tax_id']
) AS SELECT * FROM landing.intact_2018_10_04 ORDER BY interactor_a_id, interactor_b_id;