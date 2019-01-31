CREATE TABLE IF NOT EXISTS landing.bgee_14_0_limit_200M WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id'] )
AS SELECT * FROM landing.bgee_14_0 LIMIT 200000000;

 CREATE TABLE IF NOT EXISTS landing.bgee_14_0_limit_200M_score_above_1000 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id'] )
AS SELECT * FROM landing.bgee_14_0_limit_200M WHERE score > 1000;

CREATE TABLE IF NOT EXISTS master.bgee_14_0 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.bgee_14_0_limit_200M_score_above_1000 ORDER BY tissue_uberon_id, score DESC;
