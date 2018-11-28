CREATE TABLE IF NOT EXISTS project.uniprot_id_mapping_2018_11_target_uniprotac WITH (
   format = 'JSON'
) AS
SELECT *
FROM master.uniprot_id_mapping_2018_11
WHERE to_id_type='uniprotac'
ORDER BY from_id_type, from_id, to_id;