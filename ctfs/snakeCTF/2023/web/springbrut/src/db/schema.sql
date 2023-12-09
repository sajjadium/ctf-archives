
CREATE USER "superuser"@"%" IDENTIFIED BY "REDACTED";
CREATE DATABASE IF NOT EXISTS springbrut;

USE springbrut;

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users
(
        id int AUTO_INCREMENT,
        username varchar(255),
        password varchar(255),
        PRIMARY KEY(id)
);

INSERT INTO users(username, password) VALUES ("admin","$2a$10$TNoo6JxBs46vgH5fDbE4R.4zb.im8t83L6tDRppx34/FjicQBBGT2");
GRANT ALL ON springbrut.* TO "superuser"@"%";
CREATE USER "app"@"%" IDENTIFIED BY "REDACTED";
CREATE DATABASE IF NOT EXISTS photatopower;
USE photatopower;

