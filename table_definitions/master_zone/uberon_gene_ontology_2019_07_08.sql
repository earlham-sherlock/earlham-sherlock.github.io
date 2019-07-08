CREATE TABLE IF NOT EXISTS master.uberon_gene_ontology_2019_07_08 WITH (
   format = 'ORC'
) AS SELECT * FROM landing.uberon_gene_ontology_2019_07_08 ORDER BY id;
