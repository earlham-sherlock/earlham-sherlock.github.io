CREATE TABLE IF NOT EXISTS landing.mentha_2019_05_24 (
   interactor_a_id VARCHAR,
   interactor_b_id VARCHAR,
   interactor_a_id_type VARCHAR,
   interactor_b_id_type VARCHAR,
   interactor_b_tax_id INT,
   interactor_a_molecule_type_mi_id INT,
   interactor_b_molecule_type_mi_id INT,
   interactor_a_molecule_type_name VARCHAR,
   interactor_b_molecule_type_name VARCHAR,
   interaction_detection_methods_mi_id ARRAY<INT>,
   interaction_types_mi_id ARRAY<INT>,
   source_database_mi_id ARRAY<INT> ,
   pmids ARRAY<BIGINT>,
   interactor_a_tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['interactor_a_tax_id'],
   external_location = 's3a://sherlock/landing_zone/mentha_2019_05_24');

-- don't forget to refresh the partition list!