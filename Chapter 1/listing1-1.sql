\sql
\connect root@localhost:3306
CREATE DATABASE testdb;
CREATE TABLE testdb.t1 (a int auto_increment not null primary key, b timestamp, c char(20));
INSERT INTO testdb.t1 (c) VALUES ('one'), ('two'), ('three');
SELECT * FROM testdb.t1 WHERE c = 'two';