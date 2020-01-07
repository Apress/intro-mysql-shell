\sql
\connect root@localhost:3306
DROP DATABASE IF EXISTS mydb_json;
CREATE DATABASE mydb_json;
CREATE TABLE mydb_json.customers (id int auto_increment NOT NULL PRIMARY KEY, first_name char(30), last_name char(30), addresses JSON);
INSERT INTO mydb_json.customers VALUES (NULL, 'Sam', 'Blastone', '{"addresses":[
    {"caption":"HOME","street1":"9001 Oak Row Road","city":"LaPlata","state_code":"MD","zip":"33532"},
    {"caption":"WORK","street1":"123 Main Street","city":"White Plains","state_code":"MD","zip":"33560"},
    {"caption":"WAREHOUSE","city":"Carson Creek","state_code":"CO"}
]}');
SELECT first_name, last_name, JSON_PRETTY(addresses) FROM mydb_json.customers \G
