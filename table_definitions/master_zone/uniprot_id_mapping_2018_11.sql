CREATE TABLE IF NOT EXISTS master.uniprot_id_mapping_2018_11 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id', 'from_id_type']
) AS SELECT from_id, to_id, to_id_type, tax_id, from_id_type FROM landing.uniprot_id_mapping_2018_11 ORDER BY to_id_type, from_id, to_id;
