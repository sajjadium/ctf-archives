ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'PRIVATE';
CREATE USER 'web'@'localhost' IDENTIFIED WITH mysql_native_password BY 'PRIVATE';
FLUSH PRIVILEGES;

DROP DATABASE IF EXISTS ctf_challenge;
CREATE DATABASE ctf_challenge;
USE ctf_challenge;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    data NVARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users (username, password, data) VALUES ('admin', 'PRIVATE', 'PRIVATE');

GRANT INSERT, SELECT, UPDATE ON ctf_challenge.users TO 'web'@'localhost';
FLUSH PRIVILEGES;