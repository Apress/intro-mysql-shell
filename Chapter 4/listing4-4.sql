SHOW CREATE TABLE factory_sensors.trailer_assembly \G
CREATE INDEX sensor_name ON factory_sensors.trailer_assembly (sensor_name);
SHOW CREATE TABLE factory_sensors.trailer_assembly \G
DROP INDEX sensor_name ON factory_sensors.trailer_assembly;
CREATE VIEW list_weights AS SELECT * FROM factory_sensors.trailer_assembly WHERE sensor_units = 'pounds' LIMIT 3;