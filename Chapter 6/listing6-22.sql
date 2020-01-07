DROP TABLE IF EXISTS `testdb_6`.`thermostats`;
CREATE TABLE `testdb_6`.`thermostats` (`model_number` char(20) NOT NULL,`manufacturer` char(30) DEFAULT NULL,`capabilities` json DEFAULT NULL,PRIMARY KEY (`model_number`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO `testdb_6`.`thermostats` VALUES ('ODX-123','Genie','{"rpm": 3000, "color": "white", "modes": ["ac", "furnace"], "voltage": 220, "capability": "fan"}') \G
INSERT INTO `testdb_6`.`thermostats` VALUES ('AB-90125-C1', 'Jasper', '{"rpm": 1500, "color": "beige", "modes": ["ac"], "voltage": 110, "capability": "auto fan"}') \G
ALTER TABLE `testdb_6`.`thermostats` ADD COLUMN color char(20) GENERATED ALWAYS AS (capabilities->'$.color') VIRTUAL;
SELECT model_number, color FROM `testdb_6`.`thermostats` WHERE color = "beige" \G
SELECT model_number, color FROM `testdb_6`.`thermostats` LIMIT 2 \G
ALTER TABLE `testdb_6`.`thermostats` DROP COLUMN color;
ALTER TABLE `testdb_6`.`thermostats` ADD COLUMN color char(20) GENERATED ALWAYS AS (JSON_UNQUOTE(capabilities->'$.color')) VIRTUAL;
SELECT model_number, color FROM `testdb_6`.`thermostats` WHERE color = 'beige' LIMIT 1 \G
