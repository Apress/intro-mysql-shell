DROP DATABASE IF EXISTS factory_sensors;
CREATE DATABASE factory_sensors;
USE factory_sensors;
CREATE TABLE `factory_sensors`.`trailer_assembly` (
  `id` int auto_increment,
  `sensor_name` char(30) NOT NULL,
  `sensor_value` float DEFAULT NULL,
  `sensor_event` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sensor_units` char(15) DEFAULT NULL,
  PRIMARY KEY `sensor_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SHOW CREATE TABLE factory_sensors.trailer_assembly \G
INSERT INTO factory_sensors.trailer_assembly (sensor_name, sensor_value, sensor_units) VALUES ('paint_vat_temp', 32.815, 'Celsius');
INSERT INTO factory_sensors.trailer_assembly (sensor_name, sensor_value, sensor_units) VALUES ('tongue_height_variance', 1.52, 'mm'), ('ambient_temperature', 24.5, 'Celsius'), ('gross_weight', 1241.01, 'pounds');
SELECT sensor_name FROM factory_sensors.trailer_assembly;
SELECT sensor_name, sensor_value, sensor_event, sensor_units FROM factory_sensors.trailer_assembly \G
SELECT * FROM factory_sensors.trailer_assembly \G
SELECT sensor_value, sensor_name, sensor_units FROM factory_sensors.trailer_assembly;
DELETE FROM factory_sensors.trailer_assembly WHERE sensor_value > 10;
UPDATE factory_sensors.trailer_assembly SET sensor_units = 'inches' WHERE cast(sensor_value as decimal(5,2)) = 1.52;
