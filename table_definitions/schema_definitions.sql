CREATE SCHEMA IF NOT EXISTS landing  WITH (location = 's3a://sherlock/landing_zone');
CREATE SCHEMA IF NOT EXISTS master  WITH (location = 's3a://sherlock/master_zone');
CREATE SCHEMA IF NOT EXISTS project  WITH (location = 's3a://sherlock/project_zone');

-- hive example
CREATE DATABASE IF NOT EXISTS landing LOCATION 's3a://sherlock/landing_zone';

