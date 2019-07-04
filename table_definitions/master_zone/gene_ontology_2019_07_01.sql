CREATE TABLE IF NOT EXISTS master.gene_ontology_2019_07_01 WITH (
   format = 'ORC'
) AS SELECT * FROM landing.gene_ontology_2019_07_01 ORDER BY id;
