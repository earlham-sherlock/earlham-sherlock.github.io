CREATE TABLE IF NOT EXISTS landing.dorothea_2020_10_05 (
   interactor_a_id VARCHAR,
   interactor_b_id VARCHAR,
   interactor_a_id_type VARCHAR,
   interactor_b_id_type VARCHAR,
   interactor_b_tax_id INT,
   confidence_score VARCHAR,
   mor ARRAY<INT> ,
   interactor_a_tax_id INT
) WITH (
   format            = 'JSON',
   partitioned_by    = ARRAY['interactor_a_tax_id'],
   external_location = 's3a://sherlock/landing_zone/dorothea_2020_10_05');

-- don't forget to refresh the partition list!