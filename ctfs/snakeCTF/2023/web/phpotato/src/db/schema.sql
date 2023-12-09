
CREATE USER 'app'@'%' IDENTIFIED BY 'REDACTED';
CREATE DATABASE IF NOT EXISTS photatopower;
USE photatopower;

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username varchar(255) UNIQUE,
        password varchar(255),
        is_admin boolean
);

DROP TABLE IF EXISTS numbers;

CREATE TABLE numbers
(
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        num varchar(255) NOT NULL,
        pipeline varchar(255),
        user_id int NOT NULL REFERENCES users(id),
        processed boolean,
        processed_date DATETIME
);
CREATE INDEX number_user_id ON numbers (user_id);

INSERT INTO users(id, username, password, is_admin) VALUES (1, 'admin','REDACTED', true);
INSERT INTO numbers(num, user_id, processed, processed_date) VALUES ('E', 1, true, '1970-01-01 00:00:01');
INSERT INTO numbers(num, user_id, processed, pipeline) VALUES ('2.65', 1, false, ' *= PI');
INSERT INTO numbers(num, user_id, processed, processed_date) VALUES ('3.33', 1, true, '1970-01-01 00:00:01');

GRANT SELECT,INSERT ON photatopower.users TO 'app'@'%';
GRANT SELECT,INSERT,UPDATE,DELETE ON photatopower.numbers TO 'app'@'%';
FLUSH PRIVILEGES;

