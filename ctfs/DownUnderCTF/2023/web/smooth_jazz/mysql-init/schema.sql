CREATE DATABASE challenge;

USE challenge;

CREATE TABLE IF NOT EXISTS users (
	username TEXT NOT NULL,
	password TEXT NOT NULL
);

INSERT INTO users VALUES ('admin', SHA1(RANDOM_BYTES(32)));

CREATE USER 'challuser'@'%' IDENTIFIED BY 'challpass';
GRANT SELECT ON challenge.* TO 'challuser'@'%';