CREATE TABLE IF NOT EXISTS master.uniprot_id_mapping_2019_06 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id']
) AS SELECT * FROM landing.uniprot_id_mapping_2019_06 ORDER BY from_id_type, to_id_type, from_id, to_id;
