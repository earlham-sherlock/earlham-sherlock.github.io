CREATE SCHEMA IF NOT EXISTS landing  WITH (location = 's3a://sherlock-korcsmaros-group/landing_zone');
CREATE SCHEMA IF NOT EXISTS master  WITH (location = 's3a://sherlock-korcsmaros-group/master_zone');
CREATE SCHEMA IF NOT EXISTS project  WITH (location = 's3a://sherlock-korcsmaros-group/project_zone');

-- hive
CREATE DATABASE IF NOT EXISTS landing LOCATION 's3a://sherlock/landing_zone';

