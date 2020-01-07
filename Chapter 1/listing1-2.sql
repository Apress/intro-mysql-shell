\sql
\connect root@localhost:3306
DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
CREATE TABLE mydb.customers (id int auto_increment NOT NULL PRIMARY KEY, first_name char(30), last_name char(30));
CREATE TABLE mydb.addresses (id int NOT NULL, caption char(20) NOT NULL, street1 char(100), street2 char(100), city char(50), state_code char(2), zip char(10), PRIMARY KEY(id, caption));
INSERT INTO mydb.customers VALUES (NULL, 'Sam', 'Blastone');
SELECT LAST_INSERT_ID() INTO @last_id;
INSERT INTO mydb.addresses VALUES (@last_id, 'HOME', '9001 Oak Row Road', Null, 'LaPlata', 'MD', '33532');
INSERT INTO mydb.addresses VALUES (@last_id, 'WORK', '123 Main Street', Null, 'White Plains', 'MD', '33560');
SELECT first_name, last_name, addresses.* FROM mydb.customers JOIN mydb.addresses ON customers.id = addresses.id \G
INSERT INTO mydb.addresses VALUES (@last_id, 'WAREHOUSE', Null, Null, 'Carson Creek', 'CO', Null);
