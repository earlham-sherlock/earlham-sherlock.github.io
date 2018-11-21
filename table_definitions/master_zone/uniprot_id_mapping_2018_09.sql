CREATE TABLE IF NOT EXISTS master.uniprot_id_mapping_2018_09 WITH (
   format = 'ORC',
   partitioned_by = ARRAY['tax_id', 'from_id_type', 'to_id_type']
) AS SELECT * FROM landing.uniprot_id_mapping_2018_09 ORDER BY from_id, to_id;