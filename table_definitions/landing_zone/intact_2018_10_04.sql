CREATE TABLE IF NOT EXISTS landing.intact_2018_10_04 (
   interactor_a_id VARCHAR(64) NOT NULL,
   interactor_b_id VARCHAR(64) NOT NULL,
   interactor_a_id_type VARCHAR(25) NOT NULL,
   interactor_b_id_type VARCHAR(25) NOT NULL,
   interactor_a_tax_id INT NOT NULL,
   interactor_b_tax_id INT NOT NULL,
   interactor_a_molecula_type_mi_id INT NOT NULL,
   interactor_b_molecula_type_mi_id INT NOT NULL,
   interactor_a_molecula_type_name VARCHAR(25) NOT NULL,
   interactor_b_molecula_type_name VARCHAR(25) NOT NULL,
   interaction_detection_methods_mi_id ARRAY<INT> NOT NULL,
   interaction_types_mi_id ARRAY<INT> NOT NULL,
   source_databases_mi_id ARRAY<INT> NOT NULL,
   pmids ARRAY<INT>  NOT NULL
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['interactor_a_tax_id'],
   external_location = 'S3://sherlock-korcsmaros-group/landing_zone/intact_2018_10_04' );