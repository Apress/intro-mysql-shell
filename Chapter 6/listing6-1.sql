CREATE DATABASE `testdb_6`;
USE `testdb_6`;
CREATE TABLE `testdb_6`.`addresses` (`id` int(11) NOT NULL AUTO_INCREMENT, `address` json DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO `testdb_6`.`addresses` VALUES (NULL, '{"address": {"street": "123 Second St","city": "Maynard","state": "CT","zip": "19023"}}');
INSERT INTO `testdb_6`.`addresses` VALUES (NULL, '{"address": {"street":"41 West Hanover","city":"Frederick","state":"Maryland","zip":"20445"}}');
SELECT * FROM `testdb_6`.`addresses` \G
DROP DATABASE `testdb_6`;
