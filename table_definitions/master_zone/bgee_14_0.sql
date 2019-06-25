CREATE TABLE IF NOT EXISTS master.bgee_14_0 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.bgee_14_0_limit_200M_score_above_1000 ORDER BY tissue_uberon_id, score DESC;
